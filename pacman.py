import pygame, tasks, random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PACMAN_COLOR = (255, 255, 0)
PACMAN_RADIUS = 30
MOVEMENT_SPEED = 10
POINTS = 0
LETTER_SIZE = 20

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loot trial")

# Set up Pac-Man
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_angle = 45  # Initial angle

# Access the json file that contains the words
words = tasks.read_json(f'{tasks.JS_PATH}/words')

# Generate a random index
random_index = random.randint(0, len(words))

# Pick a random word
word = words[f'{random_index}']

# Set up letters
# letters = list(word)

# Set up letters
letters = [{'x': random.randint(0, WIDTH - LETTER_SIZE), 'y': random.randint(0, HEIGHT - LETTER_SIZE)}
           for _ in range(5)]

# Function to check collisions
def check_collisions():
    global pacman_x, pacman_y, POINTS
    for letter in letters:
        if (pacman_x - letter['x']) ** 2 + (pacman_y - letter['y']) ** 2 <= (PACMAN_RADIUS + LETTER_SIZE) ** 2:
            letters.remove(letter)
            POINTS+=1
            return True
    return False


# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Update Pac-Man position dynamically
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_x -= MOVEMENT_SPEED
            elif event.key == pygame.K_RIGHT:
                pacman_x += MOVEMENT_SPEED
            elif event.key == pygame.K_UP:
                pacman_y -= MOVEMENT_SPEED
            elif event.key == pygame.K_DOWN:
                pacman_y += MOVEMENT_SPEED

    # Check collisions
    if check_collisions():
        print(f"Pac-Man picked up a letter! You have {POINTS} points")

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw letters
    for letter in letters:
        pygame.draw.rect(screen, (255, 0, 0), (letter['x'], letter['y'], LETTER_SIZE, LETTER_SIZE))


    # Draw Pac-Man
    pygame.draw.circle(screen, PACMAN_COLOR, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
    pygame.draw.polygon(screen, BACKGROUND_COLOR, [(pacman_x, pacman_y)] + [
        (pacman_x + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate(pacman_angle + angle).x,
         pacman_y + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate(pacman_angle + angle).y)
        for angle in range(-30, 31, 10)
    ])

    # Check if all letters are picked
    if not letters:
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Pac-Man picked up all letters!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)
