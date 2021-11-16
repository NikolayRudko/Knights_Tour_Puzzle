def input_size_desk():
    while True:
        try:
            x, y = map(int, input("Enter your board dimensions:").split())
            if x < 1 or y < 1:
                raise ValueError
            return x, y
        except ValueError:
            print('Invalid dimensions!')


def input_game_mod():
    while True:
        game_mode = input('Do you want to try the puzzle? (y/n):')
        if game_mode == 'y' or game_mode == 'n':
            return game_mode
        else:
            print('Invalid dimensions!')


def input_starting_position(size_x, size_y):
    while True:
        try:
            x, y = map(int, input("Enter the knight's starting position:").split())
            if not 1 <= x <= size_x or not 1 <= y <= size_y:
                raise ValueError
            return x - 1, y - 1
        except ValueError:
            print('Invalid position!')


def create_field(x, y):
    return [['_' * len(str(y * x)) for _ in range(x)] for _ in range(y)]


def draw_field(field, size_y, size_x):
    length_cell = len(str(size_y * size_x))
    length_cell_column = len(str(size_y))
    separator_line = '-' * (size_x * (length_cell + 1) + 3)
    number_space = "{:{width}}".format('', width=length_cell_column)
    separator = number_space + separator_line
    print(separator)
    for i, val in reversed(list(enumerate(field))):
        line = ' '.join(val)
        number_row = "{:>{width}}".format(str(i + 1), width=length_cell_column)
        print(f'{number_row}| {line} |')
    print(separator)
    numbers = ' '.join(["{:>{width}}".format(str(i + 1), width=length_cell) for i in range(size_x)])
    print(f'{number_space}  {numbers}')


def get_movies(x, y):
    return [[x + 1, y + 2], [x - 1, y + 2], [x + 1, y - 2], [x - 1, y - 2],
            [x + 2, y - 1], [x + 2, y + 1], [x - 2, y - 1], [x - 2, y + 1]]


def check_possible_moves(field_x, field_y, knight_x, knight_y, way):
    possible_directions = get_movies(knight_x, knight_y)
    possible_moves = []
    for x, y in possible_directions:
        if 0 <= x < field_x and 0 <= y < field_y and not [x, y] in way:
            cell = numbers_possible_moves(field_x, field_y, x, y, way)
            possible_moves.append([[x, y], cell])
    return sorted(possible_moves, key=lambda move: move[1], reverse=True)


def numbers_possible_moves(field_x, field_y, knight_x, knight_y, way):
    possible_directions = get_movies(knight_x, knight_y)
    moves = 0
    for x, y in possible_directions:
        if 0 <= x < field_x and 0 <= y < field_y and not [x, y] in way:
            moves += 1
    return moves


def is_can_win(field_x, field_y, knight_x, knight_y):
    way = []
    return len(ai_solution(field_x, field_y, knight_x, knight_y, way)) == field_x * field_y


def make_move(way, field_x, field_y, knight_x, knight_y):
    length_knight_cell = len(str(field_x * field_y))

    way.append([knight_x, knight_y])
    possible_moves = check_possible_moves(field_x, field_y, knight_x, knight_y, way)
    mask_field = create_field(field_x, field_y)

    for move in possible_moves:
        number_moves = move[1]
        x, y = move[0]
        mask_field[y][x] = "{:>{width}}".format(str(number_moves), width=length_knight_cell)

    for position in way:
        _x, _y = position
        if position == way[-1]:
            mask_field[_y][_x] = "{:>{width}}".format('X', width=length_knight_cell)
        else:
            mask_field[_y][_x] = "{:>{width}}".format('*', width=length_knight_cell)

    draw_field(mask_field, field_y, field_x)


def check_move(possible_moves, message="Enter your next move:"):
    moves = [move[0] for move in possible_moves]
    try:
        x, y = map(int, input(message).split())
        x, y = x - 1, y - 1
        if not [x, y] in moves:
            raise ValueError
        return x, y
    except ValueError:
        return check_move(possible_moves, message="Invalid move! Enter your next move")


def player_game(field_x, field_y, knight_x, knight_y):
    way = []
    make_move(way, field_x, field_y, knight_x, knight_y)
    possible_moves = check_possible_moves(field_x, field_y, knight_x, knight_y, way)
    while possible_moves:
        next_move_x, next_move_y = check_move(possible_moves)
        make_move(way, field_x, field_y, next_move_x, next_move_y)
        possible_moves = check_possible_moves(field_x, field_y, next_move_x, next_move_y, way)
    count_squares = len(way)
    if count_squares == field_y * field_x:
        print('What a great tour! Congratulations!')
    else:
        print(f'No more possible moves!\nYour knight visited {count_squares} squares!')


def ai_game(field_x, field_y, knight_x, knight_y):
    way = []
    result_way = ai_solution(field_x, field_y, knight_x, knight_y, way)
    mask_field = create_ai_mask(field_x, field_y, result_way)
    print("\nHere's the solution!")
    draw_field(mask_field, field_y, field_x)


def create_ai_mask(field_x, field_y, way):
    mask_field = create_field(field_x, field_y)
    for index, val in enumerate(way):
        x, y = val
        number_move = "{:>{width}}".format(str(index + 1), width=len(str(field_x * field_y)))
        mask_field[y][x] = number_move
    return mask_field


def ai_solution(field_x, field_y, knight_x, knight_y, way):
    my_way = way[:]
    my_way.append([knight_x, knight_y])
    possible_moves = check_possible_moves(field_x, field_y, knight_x, knight_y, my_way)

    if len(my_way) == field_y * field_x:
        return my_way
    else:
        if possible_moves:
            for move in possible_moves:
                x, y = move[0]
                temp_way = ai_solution(field_x, field_y, x, y, my_way)
                if temp_way != my_way:
                    return temp_way
    return way


def game():
    field_x, field_y = input_size_desk()
    knight_x, knight_y = input_starting_position(field_x, field_y)
    game_mode = input_game_mod()

    if is_can_win(field_x, field_y, knight_x, knight_y):
        if game_mode == 'y':
            player_game(field_x, field_y, knight_x, knight_y)
        elif game_mode == 'n':
            ai_game(field_x, field_y, knight_x, knight_y)
    else:
        print('No solution exists!')


game()