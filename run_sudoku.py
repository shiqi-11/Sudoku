import pygame
from sudoku_helper import SudokuHelper, SudokuFrame, Button, Mouse

# Initialize Pygame
pygame.init()
width, height = 500, 600
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")
start_point = (50, 100)  # [x, y]
font = pygame.font.SysFont(None, 40)
sudoku_frame = SudokuFrame()
sudoku_helper = SudokuHelper()
sudoku_helper.generate_puzzle(difficulty='Easy')
mouse = Mouse()
black = pygame.Color('black')

# Create a button
show_solution_button = Button((0, 255, 0), 150, 520, 200, 50, 'Show Solution')
# Create a 'New Game' button
new_game_button = Button((255,255, 255), 0, 0, 110, 30, 'New Game')

# Main loop
running = True
show_solution = False
win = False
selected_cell = None
cell_size = 400 // 9  # Assuming a 400x400 Sudoku board

while running:
    pos = pygame.mouse.get_pos()

    if not win and sudoku_helper.is_solved_correctly():
        win = True
        print("You Wind")
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = mouse.get_clicked_pos(pos, start_point, cell_size)
            if clicked:
                selected_cell = clicked
            if show_solution_button.is_over(pos):
                show_solution = not show_solution
                if win:
                    description = "You Win"
                else:
                    description = "Hide Solution" if show_solution else "Show Solution"
                show_solution_button = Button((0, 255, 0), 150, 520, 200, 50, description)
                print("Button clicked!", show_solution)  # Debugging statement
            if new_game_button.is_over(pos):
                # Reset the board and generate a new puzzle
                sudoku_helper.generate_puzzle(difficulty='Difficult')
                show_solution = False
                win = False  # Reset the win state if you have a win condition

        if event.type == pygame.KEYDOWN:
            if selected_cell and event.unicode.isdigit():
                x, y = selected_cell
                num = int(event.unicode)
                sudoku_helper.board[x][y] = num  # Update the board with the input number

    surface.fill(pygame.Color('white'))  # Clear screen with white background
    welcome_flag = font.render('Start Your Sudoku Conquer', True, black)
    sudoku_frame.draw_sudoku_board(surface, start_point, 400, black)  # Draw frame lines
    surface.blit(welcome_flag, (70, 40))
    show_solution_button.draw(surface, (0, 0, 0))
    new_game_button.draw(surface, (0, 0, 0))  # Draw the 'New Game' button


    # Draw digits
    board = sudoku_helper.puzzle if show_solution else sudoku_helper.board
    for i in range(9):
        for j in range(9):
            digit = board[i][j]
            if digit != 0:  # Assuming 0 represents an empty cell
                text_surface = font.render(str(digit), True, black)
                surface.blit(text_surface, (start_point[0] + j * cell_size + 15, start_point[1] + i * cell_size + 10))

                
    # Highlight selected cell
    if selected_cell:
        pygame.draw.rect(surface, (255, 0, 0), (start_point[0] + selected_cell[1] * cell_size, start_point[1] + selected_cell[0] * cell_size, cell_size, cell_size), 3)

    if win:
        win_message = font.render('You Win!', True, black)
        surface.blit(win_message, (150, 550))  # Adjust position as needed


    pygame.display.flip()

# Quit Pygame
pygame.quit()