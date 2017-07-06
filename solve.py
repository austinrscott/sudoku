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
