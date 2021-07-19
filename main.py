import sys
import time

start_time = time.time()
sys.stdin = open("sudoku.txt", "r")
sudoku = []
for i in range(9):
    [sudoku.append(int(num)) for num in input().split()]


# returns 2D list of missing numbers for each square, for the given sudoku
def find_missing_square(numbers):
    result = []

    for square_num in range(9):
        cols = square_num % 3
        rows = square_num // 3
        square = []

        for row in range(3 * rows, 3 * rows + 3):
            for col in range(3 * cols, 3 * cols + 3):
                square.append(numbers[9 * row + col])

        missing = []
        for i in range(1, 10):
            if square.count(i) == 0: missing.append(i)

        result.append(missing)

    return result


def find_missing_row(numbers):
    result = []

    for row_num in range(9):
        row = []
        for num in range(9):
            row.append(numbers[9 * row_num + num])

        missing = []
        for i in range(1, 10):
            if row.count(i) == 0: missing.append(i)

        result.append(missing)

    return result


def find_missing_column(numbers):
    result = []

    for col_num in range(9):
        col = []
        for num in range(9):
            col.append(numbers[col_num + 9 * num])

        missing = []
        for i in range(1, 10):
            if col.count(i) == 0: missing.append(i)

        result.append(missing)

    return result


def fill_num(sudoku, n, coord):
    sudoku[coord] = n
    return sudoku

def sudoku_solver(sudoku):
    # Coordinate of the element of a given index is ((index) / 9, (index % 9))
    # There are three conditions to meet for each element: square, column, and row
    # We can represent each 'square' by a combination of modulo and division operations.
    #
    # ex. (first square) -> n/9: 0~2, n%9: 0~2
    #     (second square) -> n/9: 0~2, n%9: 3~5
    #     and so forth...
    #
    # element = [col_num, row_num, square_num, possibilities]
    #
    # col -> i % 9
    # row -> i // 9
    # square -> 3 * (row // 3) + col * 3

    missing_squares = find_missing_square(sudoku)
    missing_rows = find_missing_row(sudoku)
    missing_cols = find_missing_column(sudoku)

    print(missing_squares)
    print(missing_rows)
    print(missing_cols)

    not_found = [] # List of indices of blanks
    not_found_pos = [] # List of possible nums for each blank

    for i in range(81):
        if sudoku[i] == 0:
            col = i % 9
            row = i // 9
            square = 3 * (row // 3) + col // 3
            not_found.append([i, row, col, square])

    for i in not_found:
        col = i[0] % 9
        row = i[0] // 9
        square = 3 * (row // 3) + col // 3

        pos = []
        for num in missing_squares[square]:
            if (missing_rows[row].count(num) != 0) and (missing_cols[col].count(num) != 0):
                pos.append(num)

        not_found_pos.append(pos)

    cnt = 0
    while len(not_found) > 0:
        cnt += 1
        for i in range(len(not_found)):
            print(i, "th loop")
            print("Blanks to fill: ", len(not_found))
            print("no_found_pos", not_found_pos)
            if len(not_found_pos[i]) == 1:

                print("Filling in blank: ", not_found[i][0])
                print("Answer: ", not_found_pos[i][0])
                print("Blanks left: ", len(not_found) - 1)

                sudoku[not_found[i][0]] = not_found_pos[i][0] # Fill the blank with the only possible choice

                for j in range(len(not_found)):
                    is_pos = not_found_pos[j].count(not_found_pos[i][0]) != 0
                    if not_found[j][1] == not_found[i][1] or not_found[j][2] == not_found[i][2] or not_found[j][3] == not_found[i][3]:
                        if is_pos:
                            if i != j:
                                not_found_pos[j].remove(not_found_pos[i][0])

                not_found.pop(i) # Remove index from list
                not_found_pos.pop(i) # Remove choice from list
                break

            elif len(not_found_pos[i]) == 2:
                print("Guessing blank: ", not_found[i][0])
                print("Guess: ", not_found_pos[i][0])
                print("Blanks left: ", len(not_found) - 1)

                sudoku[not_found[i][0]] = not_found_pos[i][0]  # Fill the blank with the only possible choice

                for j in range(len(not_found)):
                    is_pos = not_found_pos[j].count(not_found_pos[i][0]) != 0
                    if not_found[j][1] == not_found[i][1] or not_found[j][2] == not_found[i][2] or not_found[j][3] == \
                            not_found[i][3]:
                        if is_pos:
                            if i != j:
                                not_found_pos[j].remove(not_found_pos[i][0])
                not_found.pop(i)  # Remove index from list
                not_found_pos.pop(i)  # Remove choice from list
                break

        if cnt == 100: break

    print("Sudoku solved!")
    for line_num in range(9):
        print(sudoku[9 * line_num: 9 * line_num + 9])
    print("--- %s seconds ---" % (time.time() - start_time))


sudoku_solver(sudoku)