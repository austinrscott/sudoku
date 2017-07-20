import json
import threading
import time

from board import Board


def solve_one(board, move_list=[]):
    if board.complete:
        return move_list
    elif not board.legal:
        return []
    else:
        for pv_group in board.blanks_by_pv:
            for xy, pv in pv_group:
                for value in pv:
                    b = Board(board.string)
                    b[xy] = value
                    solution = solve_one(board=b, move_list=[*move_list, (xy, value)])
                    if solution:
                        return solution
        return []


def set_xy_in_board_string(string, xy, value):
    new_string = list(string)
    new_string[Board.xy_to_idx(xy)] = value
    return "".join(new_string)


solved_boards = []
boards_to_check = ['0' * 81]
children_of = {}
parents_of = {}


def find_children(board_string):
    board = Board(board_string)
    children = []
    if board.complete:
        solved_boards.append(board_string)
        print(len(solved_boards), 'solved boards,', len(children_of), 'visited')
    else:
        for move in board.all_legal_moves:
            new_board = set_xy_in_board_string(board_string, *move)
            if new_board not in children_of.keys() and new_board not in boards_to_check:
                boards_to_check.append(new_board)
                children.append(new_board)
    return children


def solve_all():
    while boards_to_check:
        cur_board = boards_to_check.pop(0)
        cb_children = find_children(cur_board)
        for child in cb_children:
            if child not in parents_of.keys():
                parents_of[child] = [cur_board]
            else:
                parents_of[child].append(cur_board)
        children_of[cur_board] = cb_children


if __name__ == "__main__":
    solver = threading.Thread(target=solve_all)
    print("Solver is now beginning.")
    solver.start()
    while solver.is_alive():
        time.sleep(5)
        print("{} boards visited. {} boards in queue. {} complete boards found.".format(
            len(children_of), len(boards_to_check), len(solved_boards)
        ))
    print("Solver is finished. Now dumping solutions and graphs...")
    with open('children_of.txt', 'w') as outfile:
        json.dump(children_of, outfile)
    with open('parents_of.txt', 'w') as outfile:
        json.dump(parents_of, outfile)
    with open('solutions.txt', 'w') as outfile:
        json.dump(solved_boards, outfile)
    print("Done.")
