import pygame

pygame.init()
width, height = 900, 900
surface = pygame.display.set_mode((width, height))
# Create a surface for the button
button_surface = pygame.Surface((50, 50))

# Draw the button's text and border on the surface
pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 100, 50))
pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 98, 48))
pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 98, 1), 2)
# Create a pygame.Rect object that represents the button's boundaries
button_rect = pygame.Rect(0, 0, 100, 50)

# Create a pygame.event.MOUSEBUTTONDOWN event handler that checks if the mouse is clicked inside the button's boundaries
def on_mouse_button_down(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos):
        print("Button clicked!")

# Call the pygame.display.update() function to display the button on the screen
pygame.display.update()

# Start the main loop
while True:
    # Get events from the event queue
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()

        # Check for the mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function
            on_mouse_button_down(event)

    # Update the game state

    # Draw the game screen
    pygame.display.update()