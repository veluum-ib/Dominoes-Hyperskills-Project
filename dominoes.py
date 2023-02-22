import random


# Generated dominoes from 1 to 6, all unique even when reversed
def generate_domino_set():
    new_domino_set = []
    for f_num in range(7):
        for s_num in range(f_num, 7):
            new_domino_set.append([f_num, s_num])

    return new_domino_set


def reshuffle():
    random.shuffle(domino_set)
    player_set[:] = domino_set[0:7]
    computer_set[:] = domino_set[7:14]
    stock_set[:] = domino_set[14:28]


def get_double(set):
    snake = [0, 0]
    for domino in set:
        if domino[0] == domino[1]:
            if snake < domino:
                snake = domino
            elif snake > domino:
                continue
            else:
                snake = domino
    return snake


def get_domino_value(domino):
    return domino[0] + domino[1]


def find_initial_status():
    empty_list = [0, 0]
    player_snake = [0, 0]
    computer_snake = [0, 0]

    while player_snake == empty_list and computer_snake == empty_list:
        reshuffle()
        computer_snake = get_double(computer_set)
        player_snake = get_double(player_set)

    player_snake_value = get_domino_value(player_snake)
    computer_snake_value = get_domino_value(computer_snake)

    if player_snake_value > computer_snake_value:
        domino_snake[:] = [player_snake, ]
        player_set.remove(player_snake)
        return status_types[1]
    else:
        domino_snake[:] = [computer_snake, ]
        computer_set.remove(computer_snake)
        return status_types[0]


def print_domino_snake():
    # Debugging
    # domino_snake[:] = stock_set
    if len(domino_snake) > 6:
        for index in range(7):
            if index == 3:
                print("...", end="")
                continue
            if index > 3:
                index = index - 7
            print(f"{domino_snake[index]}", end="")
        return

    for domino in domino_snake:
        print(f"{domino}", end="")


def print_game_status(condition='draw'):
    for _ in range(70):
        print("=", end="")

    print(f"\nStock size: {len(stock_set)}")
    print(f"Computer pieces: {len(computer_set)}\n")

    print_domino_snake()

    print(f"\n\nYour pieces:")
    for domino in player_set:
        domino_num = player_set.index(domino) + 1
        print(f"{domino_num}:{domino}")

    print("\nStatus: ", end="")
    if status == 'player':
        print("It's your turn to make a move. Enter your command.")
    elif status == 'computer':
        print("Computer is about to make a move. Press Enter to continue...")
    else:
        print_game_over(condition)
    return True


def print_game_over(condition):
    print('The game is over. ', end="")

    match condition:
        case 'win':
            print('You won!')

        case 'lose':
            print('The computer won!')
        case 'draw':
            print("it's a draw!")


def is_move_legal(domino_to_play, side_to_attach):
    side_to_play = -1
    if side_to_attach != 0:
        side_to_attach = -1
        side_to_play = 0
    snake_domino = domino_snake[side_to_attach]
    if domino_to_play[side_to_play] != snake_domino[side_to_attach]:
        return False
    return True


def play_domino(from_set, domino_to_play):
    side_to_play = 0 if domino_to_play < 0 else len(domino_snake)
    domino_to_play = from_set[(abs(domino_to_play) - 1)]
    reversed_domino = reverse_domino(domino_to_play)
    passed_domino = [-100, - 100]
    for domino in [reversed_domino, domino_to_play]:
        if is_move_legal(domino, side_to_play):
            passed_domino = domino
    if passed_domino == [-100, -100]:
        return False
    from_set.remove(domino_to_play)
    domino_snake.insert(side_to_play, passed_domino)
    return True


def is_set_empty(passed_set):
    return len(passed_set) == 0


def take_turn(set, domino_to_play):
    global status
    if domino_to_play != 0:
        return play_domino(set, domino_to_play)
    else:
        if is_set_empty(stock_set):
            return True
        set.append(stock_set.pop())
        return True


def reverse_domino(domino):
    return domino[::-1]


def ask_input_for_domino():
    try:
        domino_to_play = int(input())
    except ValueError:
        domino_to_play = -100
    while domino_to_play < -len(player_set) or domino_to_play > len(player_set):
        print("Invalid input. Please try again.")
        try:
            domino_to_play = int(input())
        except ValueError:
            domino_to_play = -100
    return domino_to_play


def is_draw():
    snake_front = domino_snake[0][0]
    snake_end = domino_snake[-1][-1]
    if snake_front != snake_end:
        return False
    ends_are_same = True
    num_appears = 0
    for domino in domino_snake:
        for domino_side in domino:
            if domino_side == snake_front:
                num_appears += 1
    if ends_are_same and num_appears >= 8:
        return True
    return False


def play_computer_domino(set):
    global domino_snake
    score_dict = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    }
    calc_score_in_set(domino_snake, score_dict)
    calc_score_in_set(set, score_dict)

    domino_score_dict = dict()
    for domino in set:
        score = 0
        for side in domino:
            score += score_dict[side]
            domino_score_dict[set.index(domino)] = score
    order_to_play = sorted(domino_score_dict, key=lambda x: domino_score_dict[x], reverse=True)
    order_to_play.append(-1)
    while not take_turn(set, order_to_play.pop(0) + 1):
        pass

def calc_score_in_set(set, score_dict):
    for domino in set:
        for side in domino:
            if side in score_dict.keys():
                score_dict[side] += 1

if __name__ == "__main__":
    domino_set = generate_domino_set()

    stock_set = []
    player_set = []
    computer_set = []
    domino_snake = []
    status_types = ['player', 'computer', 'game_over']
    condition_types = ['win', 'lose', 'draw']

    status = find_initial_status()

    while status != 'game_over':
        if is_set_empty(player_set):
            status = 'game_over'
            print_game_status('win')
            continue
        elif is_set_empty(computer_set):
            status = 'game_over'
            print_game_status('lose')
            continue
        if is_draw():
            status = 'game_over'
            print_game_status()
            continue

        print_game_status()

        if status == 'player':
            selected_domino = ask_input_for_domino()
            while not take_turn(player_set, selected_domino):
                print("Illegal move. Please try again.")
                selected_domino = ask_input_for_domino()
            status = 'computer'
        else:
            input()
            computer_set_len = len(computer_set)
            play_computer_domino(computer_set)
            status = 'player'
