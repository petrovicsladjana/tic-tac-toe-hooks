#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import logging
import platform
import time
from os import system

logging.basicConfig(
    filename='tictactoe.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    logger.debug('Board evaluated with score=%s', score)
    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state


def game_over(state):
    over = wins(state, HUMAN) or wins(state, COMP)
    if over:
        logger.info('Game over state detected')
    return over


def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    return [x, y] in empty_cells(board)


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        logger.info('Move accepted: player=%s position=(%s,%s)', player, x, y)
        return True
    else:
        logger.warning('Move rejected: player=%s position=(%s,%s)', player, x, y)
        return False


def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        logger.info('AI turn skipped because board is full or game is over')
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    logger.info('AI selected move (%s,%s) at depth=%s', x, y, depth)
    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        logger.info('Human turn skipped because board is full or game is over')
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            logger.info('Human entered move key=%s', move)
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            logger.error('Program interrupted by user during human_turn')
            print('Bye')
            exit()
        except (KeyError, ValueError):
            logger.warning('Invalid human input encountered')
            print('Bad choice')


def main():
    logger.info('Game started')
    clean()
    h_choice = ''
    c_choice = ''
    first = ''

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
            logger.info('Human selected symbol=%s', h_choice)
        except (EOFError, KeyboardInterrupt):
            logger.error('Program interrupted during symbol selection')
            print('Bye')
            exit()
        except (KeyError, ValueError):
            logger.warning('Invalid symbol choice entered')
            print('Bad choice')

    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
            logger.info('First player selection=%s', first)
        except (EOFError, KeyboardInterrupt):
            logger.error('Program interrupted during first-player selection')
            print('Bye')
            exit()
        except (KeyError, ValueError):
            logger.warning('Invalid first-player input')
            print('Bad choice')

    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
        logger.info('Game finished with HUMAN victory')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
        logger.info('Game finished with COMP victory')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')
        logger.info('Game finished with draw')

    exit()


if __name__ == '__main__':
    main()
