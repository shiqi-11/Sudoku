import pygame
import random
import copy


class SudokuFrame:
    def draw_sudoku_board(self, surface, start_point, board_size, color):
        block_size = board_size // 9  # Size of each cell
        thick_line = 3  # Thickness for outer border and 3x3 block lines
        thin_line = 1  # Thickness for internal lines of 3x3 blocks

        # Draw the outer border
        for y in range(10):
            start_y = start_point[1] + y * block_size
            if y % 3 == 0:
                pygame.draw.line(surface, color, (start_point[0], start_y), (start_point[0] + board_size, start_y),
                                 thick_line)
            else:
                pygame.draw.line(surface, color, (start_point[0], start_y), (start_point[0] + board_size, start_y),
                                 thin_line)

        for x in range(10):
            start_x = start_point[0] + x * block_size
            if x % 3 == 0:
                pygame.draw.line(surface, color, (start_x, start_point[1]), (start_x, start_point[1] + board_size),
                                 thick_line)
            else:
                pygame.draw.line(surface, color, (start_x, start_point[1]), (start_x, start_point[1] + board_size),
                                 thin_line)

class SudokuHelper:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.puzzle = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_diagonal_boxes()
        self.solve_sudoku()
        self.shuffle_board()

    def fill_diagonal_boxes(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        num = 1
        for i in range(3):
            for j in range(3):
                while self.check_used_in_box(row, col, num):
                    num = random.randint(1, 9)
                self.board[row + i][col + j] = num

    def check_used_in_box(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if self.board[row + i][col + j] == num:
                    return True
        return False

    def shuffle_board(self):
        self.swap_rows_and_columns()
        self.swap_numbers()

    def swap_rows_and_columns(self):
        for _ in range(5):  # Perform 5 random swaps
            block = random.randint(0, 2)
            row1 = block * 3 + random.randint(0, 2)
            row2 = block * 3 + random.randint(0, 2)
            self.board[row1], self.board[row2] = self.board[row2], self.board[row1]

            col1 = block * 3 + random.randint(0, 2)
            col2 = block * 3 + random.randint(0, 2)
            for i in range(9):
                self.board[i][col1], self.board[i][col2] = self.board[i][col2], self.board[i][col1]

    def swap_numbers(self):
        for _ in range(5):  # Perform 5 random number swaps
            num1, num2 = random.sample(range(1, 10), 2)
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == num1:
                        self.board[i][j] = num2
                    elif self.board[i][j] == num2:
                        self.board[i][j] = num1

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, pos):
        # Check row
        for i in range(9):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve_sudoku(self):
        find = self.find_empty()
        if not find:
            return True
        row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0

        return False

    def generate_puzzle(self, difficulty='easy'):
        self.solve_sudoku()
        self.puzzle = copy.deepcopy(self.board)  # Create a deep copy
        print(self.puzzle)
        if difficulty == 'easy':
            iterations = 30
        elif difficulty == 'medium':
            iterations = 40
        else:  # hard
            iterations = 50

        while iterations > 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if self.board[x][y] != 0:
                self.board[x][y] = 0
                iterations -= 1
        print(self.puzzle)
    # def print_board(self):
    #     for i in range(len(self.board)):
    #         if i % 3 == 0 and i != 0:
    #             print("- - - - - - - - - - - -")
    #
    #         for j in range(len(self.board[0])):
    #             if j % 3 == 0 and j != 0:
    #                 print(" | ", end="")
    #
    #             if j == 8:
    #                 print(self.board[i][j])
    #             else:
    #                 print(str(self.board[i][j]) + " ", end="")
    #
    def is_solved_correctly(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 or self.board[i][j] != self.puzzle[i][j]:
                    return False
        return True

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 30)
            text = font.render(self.text, True, (0, 0, 0))
            surface.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

class Mouse:
    def get_clicked_pos(self, pos, start_point, cell_size):
        x, y = pos
        row = (y - start_point[1]) // cell_size
        col = (x - start_point[0]) // cell_size
        if 0 <= row < 9 and 0 <= col < 9:
            return row, col
        return None

sudoku_helper = SudokuHelper()
sudoku_helper.generate_puzzle(difficulty='hard')











