import pygame as pg, tasks, random, time ,sys

pg.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PACMAN_COLOR = (255, 255, 0)
PACMAN_RADIUS = 30
MOVEMENT_SPEED = 10
POINTS = 0
LETTER_SIZE = 50
SWITCH_DELAY = 3000  #ms

# Set up display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Loot trial")

# Set up Pac-Man
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_angle = 45  # Initial angle

# Access the json file that contains the words
words = tasks.read_json(f'{tasks.JS_PATH}/words')

# Generate a random index
random_index = random.randint(0, len(words))

# Pick a random word
word = words[f'{random_index}']
word_meaning=tasks.defineWord(word)

# Set up letters
split_word = list(word)
print(split_word)

# Set up letters
# Set up letters
letters = [{'x': random.randint(0, WIDTH - LETTER_SIZE), 'y': random.randint(0, HEIGHT - LETTER_SIZE), 'letter': letter}
           for letter in split_word]


# Function to check collisions
def check_collisions():
    global pacman_x, pacman_y, POINTS
    for letter_info in letters:
        letter_x, letter_y = letter_info['x'], letter_info['y']
        if (pacman_x - letter_x) ** 2 + (pacman_y - letter_y) ** 2 <= (PACMAN_RADIUS + LETTER_SIZE) ** 2:
            letters.remove(letter_info)
            POINTS+=1
            return letter_info['letter']
    return None

# Game loop
clock = pg.time.Clock()
switch_time = pg.time.get_ticks()  # Initial time for text switch
switched = False  # Flag to check if text has been switched

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Update Pac-Man position dynamically
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                pacman_x -= MOVEMENT_SPEED
            elif event.key == pg.K_RIGHT:
                pacman_x += MOVEMENT_SPEED
            elif event.key == pg.K_UP:
                pacman_y -= MOVEMENT_SPEED
            elif event.key == pg.K_DOWN:
                pacman_y += MOVEMENT_SPEED

    # Check collisions
    collected_letter= check_collisions()
    if collected_letter:
        print(f"You've picked up {collected_letter}! You have {POINTS} points")

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw letters
    for letter_info in letters:
        letter_x, letter_y, letter = letter_info['x'], letter_info['y'], letter_info['letter']
        font = pg.font.Font(None, LETTER_SIZE)
        text = font.render(letter, True, (255, 0, 0))
        screen.blit(text, (letter_x, letter_y))

    # Draw Pac-Man
    pg.draw.circle(screen, PACMAN_COLOR, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
    pg.draw.polygon(screen, BACKGROUND_COLOR, [(pacman_x, pacman_y)] + [
        (pacman_x + PACMAN_RADIUS * pg.math.Vector2(1, 0).rotate(pacman_angle + angle).x,
         pacman_y + PACMAN_RADIUS * pg.math.Vector2(1, 0).rotate(pacman_angle + angle).y)
        for angle in range(-30, 31, 10)
    ])

    # Check if all letters are picked
    if not letters:
        font = pg.font.SysFont("Arial", 36)
        word_text = font.render(f"Good job. You found {word.upper()}", True, (255, 255, 255))
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - word_text.get_height() // 2))

    #    the meaning and word texts are clashing
    # a fix should be found first befire uncommenting this 

        # meaning_text = font.render(f"{word_meaning}", True, (255, 255, 255))
        # screen.blit(meaning_text, (WIDTH // 2 - meaning_text.get_width() // 2, HEIGHT // 2 - meaning_text.get_height() // 2))

    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(10)
