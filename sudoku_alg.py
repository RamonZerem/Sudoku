import math


def print_board(board):
    '''Prints the board'''
    size = len(board)
    sqrt_size = int(math.sqrt(size))
    boardString = ""
    for i in range(size):
        for j in range(size):
            boardString += str(board[i][j]) + " "
            if (j+1)%sqrt_size == 0 and j != 0 and (j+1) != size:
                boardString += "| "

            if j == size-1:
                boardString += "\n"

            if j == size-1 and (i+1)%sqrt_size == 0 and (i+1) != size:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)


def find_empty (board):
    '''Finds an empty cell and returns its position as a tuple'''
    for i in range (len(board)):
        for j in range (len(board)):
            if board[i][j] == 0:
                return i,j


def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool'''
    size = len(board)
    sqrt_size = int(math.sqrt(size))
    for i in range(size):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  #make sure it isn't the same number we're checking for by comparing coords
            return False

    for j in range(size):
        if board[pos[0]][j] == num and (pos[0], j) != pos:  #Same row but not same number
            return False

    start_i = pos[0] - pos[0] % sqrt_size #ex. 5-5%3 = 3 and thats where the grid starts
    start_j = pos[1] - pos[1] % sqrt_size
    for i in range(sqrt_size):
        for j in range(sqrt_size):  #adds i and j as needed to go from start of grid to where we need to be
            if board[start_i + i][start_j + j] == num and (start_i + i, start_j + j) != pos:
                return False
    return True


def solve_backtrack(board, backtrack_counter=0):
    '''Solves the Sudoku board via the backtracking algorithm'''
    empty = find_empty(board)
    if not empty:  # no empty spots are left so the board is solved
        return True, backtrack_counter

    for nums in range(len(board)):
        if valid(board, empty, nums+1):
            board[empty[0]][empty[1]] = nums+1

            solved, backtrack_counter = solve_backtrack(board, backtrack_counter)  # recursive step
            if solved:
                return True, backtrack_counter
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
            backtrack_counter += 1
    return False, backtrack_counter


def find_empty_mrv(board):
    '''Finds the empty cell with the fewest valid values remaining'''
    min_options = float('inf')
    best_cell = None
    size = len(board)

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                # Count the number of valid values for this cell
                options = sum(1 for num in range(1, size+1) if valid(board, (i, j), num))
                if options < min_options:
                    min_options = options
                    best_cell = (i, j)

    return best_cell


def solve_with_mrv(board, backtrack_counter=0):
    '''Solves the Sudoku board using backtracking with MRV heuristic and counts backtracks'''
    empty = find_empty_mrv(board)
    if not empty:
        return True, backtrack_counter

    row, col = empty
    for num in range(1, len(board)+1):
        if valid(board, (row, col), num):
            board[row][col] = num
            solved, backtrack_counter = solve_with_mrv(board, backtrack_counter)
            if solved:
                return True, backtrack_counter
            board[row][col] = 0
            backtrack_counter += 1  # Increment the counter on backtrack

    return False, backtrack_counter


def find_empty_lcv(board):
    '''Finds the empty cell with the fewest valid values remaining'''
    min_options = float('inf')
    best_cell = None
    lcv_counts = {}

    size = len(board)

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                options = [num for num in range(1, size + 1) if valid(board, (i, j), num)]
                num_options = len(options)

                if num_options < min_options:
                    min_options = num_options
                    best_cell = (i, j)
                    lcv_counts = {num: sum(1 for ni in range(size) for nj in range(size)
                                           if (ni, nj) != best_cell and board[ni][nj] == 0 and
                                           valid(board, (ni, nj), num))
                                  for num in options}

    # Sort options by least constraining value
    if best_cell:
        best_cell_options = sorted(lcv_counts.items(), key=lambda item: item[1])
        return best_cell, [num for num, _ in best_cell_options]

    return best_cell, []


def solve_with_lcv(board, backtrack_counter=0):
    '''Solves the Sudoku board using backtracking with MRV and LCV heuristics and counts backtracks'''
    empty, lcv_options = find_empty_lcv(board)
    if not empty:
        return True, backtrack_counter

    row, col = empty
    for num in lcv_options:  # Use LCV sorted options
        if valid(board, (row, col), num):
            board[row][col] = num
            solved, backtrack_counter = solve_with_lcv(board, backtrack_counter)
            if solved:
                return True, backtrack_counter
            board[row][col] = 0  # Backtrack
            backtrack_counter += 1  # Increment the counter on backtrack

    return False, backtrack_counter