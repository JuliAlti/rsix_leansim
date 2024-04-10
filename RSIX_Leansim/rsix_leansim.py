# Rainbow Six Siege Leaning Simulator v1.0

import pygame
import sys
from pynput import keyboard

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 600  # Increased width
WINDOW_HEIGHT = 150  # Decreased height
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rainbow Six Siege Leaning Simulator")

# Set up fonts
font = pygame.font.SysFont(None, 100)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)  # Gray color for the background rectangle
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)  # Sky blue color for the background

# Function to display leaning direction
def display_character(direction):
    if direction == 'left':
        return '\\'
    elif direction == 'right':
        return '/'
    else:
        return '|'

# Keyboard event listener
class LeaningController:
    def __init__(self):
        self.direction = 'idle'
        self.velocity = 0
        self.last_pressed = None
        self.lever_position = 0
        self.window_width = WINDOW_WIDTH  # Store window width
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'q':
                if self.last_pressed == 'q':
                    self.direction = 'idle'
                    self.last_pressed = None  # Reset last_pressed when returning to idle state
                else:
                    self.direction = 'left'
                    self.last_pressed = 'q'
            elif key.char == 'e':
                if self.last_pressed == 'e':
                    self.direction = 'idle'
                    self.last_pressed = None  # Reset last_pressed when returning to idle state
                else:
                    self.direction = 'right'
                    self.last_pressed = 'e'
            elif key.char == 'a':
                self.velocity = -1
            elif key.char == 'd':
                self.velocity = 1
            elif key.char == 'x':
                print("Exiting program...")
                pygame.quit()
                sys.exit()
        except AttributeError as e:
            print("AttributeError:", e)

    def on_release(self, key):
        try:
            if key.char == 'a' or key.char == 'd':
                self.velocity = 0
        except AttributeError as e:
            print("AttributeError:", e)

    def limit_lever_position(self):
        # Limit leaning position to the edges of the window
        self.lever_position = min(max(self.lever_position, -self.window_width // 2), self.window_width // 2)

    def is_in_front_of_rectangle(self):
        return abs(self.lever_position) < WINDOW_WIDTH // 3.95  # Player is in front of the rectangle if its leaning position is within 1/3.95 of the window width

# Main function
def main():
    controller = LeaningController()

    # Set up lamp parameters
    lamp_radius = 20
    lamp_color = GREEN

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update leaning position based on velocity
        controller.lever_position += controller.velocity * 0.1  # Adjust velocity for speed

        # Limit leaning position within the window boundaries
        controller.limit_lever_position()

        # Check if the player is in front of the rectangle
        if abs(controller.lever_position) < WINDOW_WIDTH // 3.95:
            lamp_color = GREEN
        else:
            lamp_color = RED

        # Clear the window
        window.fill(SKY_BLUE)  # Set background color to sky blue

        # Display the background rectangle
        background_rect = pygame.Rect(WINDOW_WIDTH // 4, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        pygame.draw.rect(window, GRAY, background_rect)

        # Display the leaning bar
        leaning_text = font.render(display_character(controller.direction), True, WHITE)
        leaning_rect = leaning_text.get_rect(center=(WINDOW_WIDTH // 2 + controller.lever_position, WINDOW_HEIGHT // 2))
        window.blit(leaning_text, leaning_rect)

        # Draw the lamp
        lamp_x = WINDOW_WIDTH // 2  # Lamp position in the middle horizontally
        lamp_y = 10  # Lamp position at the top
        pygame.draw.circle(window, lamp_color, (lamp_x, lamp_y), lamp_radius)

        # Update the display
        pygame.display.update()

if __name__ == '__main__':
    main()
