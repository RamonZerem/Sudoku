import json
import os
import time
import random
from copy import deepcopy

import sudoku_alg


def load_sudoku_puzzles(file_path):
    """Loads Sudoku puzzles from a file."""
    with open(file_path, 'r') as file:
        puzzles = json.load(file)  # Deserialize JSON back to Python object
    return puzzles


def main():
    for file in os.listdir('tests'):
        if file.endswith('.json'):
            boards = load_sudoku_puzzles(f'tests/{file}')
            # count the number of puzzles
            n = len(boards)
            print(f"Testing {file}")
        for func in [sudoku_alg.solve_with_mrv, sudoku_alg.solve_with_lcv, sudoku_alg.solve_backtrack]:
            if func == sudoku_alg.solve_backtrack and file == 'hard_20_sudoku_puzzles_16_16.json':
                print(f"Skipping {func.__name__} for {file}")
                continue
            sudoku_alg.solve_backtrack = func
            final_time = 0
            print(f"Testing {func.__name__}")
            # Time the solving process
            backtrack_counter = 0
            for board in boards:
                start_time = time.time()
                solved, cur_backtrack_counter = func(deepcopy(board), 0)
                if not solved:
                    print("Failed to solve a board!")
                backtrack_counter += cur_backtrack_counter
                end_time = time.time()
                elapsed_time = end_time - start_time
                final_time += elapsed_time

            print(f"Average time per board: {final_time / n:.4f} seconds")
            print(f"Average backtracks per board: {backtrack_counter / n:.4f}")
            print()


if __name__ == "__main__":
    main()
