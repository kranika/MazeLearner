import pygame as pg
import math, tasks, random

from movement import movement

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 20, 1)
pg.mouse.set_visible(False)

running = True
size = 6
mapa = [[1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1,1, 0, 1, 0, 0, 1,],
        [1, 0, 1, 0, 0, 0,0, 0, 1, 0, 0, 1,],
        [1, 0, 0, 0, 0, 1,1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1]]
posx = posy = rot = 1.5
horizontal_res = 200
vertical_res = int(horizontal_res * 0.75)
frame = pg.Surface([horizontal_res, vertical_res])
mod = 60 / horizontal_res
pg.event.set_grab(1)
wall = pg.image.load('images2.jpeg').convert()
sky = pg.transform.smoothscale(pg.image.load('skybox.jpg').convert(), (12 * horizontal_res, vertical_res))

#my code 
# Set up display
width, height = 800, 600
screen = pg.display.set_mode((width, height))

#screen display title
pg.display.set_caption("Maze Learner")

# custom font 
font = pg.font.Font("mario.ttf", 36)

# word = "KIPUNJI"

#access the json file that contains the words 
words=tasks.read_json('words')

# generate a random index
random_index=random.randint(0,len(words))

#pick a random word 
word=words[f'{random_index}']

text = font.render(word, True, (255, 255, 255))


while running:
    elapsed_time = clock.tick(60) / 1000  # Use a fixed frame rate (60 FPS)

    posx, posy, rot = movement(posx, posy, rot, mapa, 2 * elapsed_time)

    fps = str(round(clock.get_fps(), 1))
    frame.blit(sky, (-math.degrees(rot % (2 * math.pi) * horizontal_res / 60), 0))

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

    for i in range(horizontal_res):  # vision loop
        rot_i = rot + math.radians(i * mod - 30)
        x, y = (posx, posy)
        sin, cos = (0.02 * math.sin(rot_i), 0.02 * math.cos(rot_i))
        n = 0
        while True:  # ray loop
            x, y = (x + cos, y + sin)
            n += 1
            if mapa[int(x)][int(y)] != 0:
                h = vertical_res * (1 / (0.02 * n * math.cos(math.radians(i * mod - 30))))
                xx = x % 1
                if xx < 0.05 or xx > 0.95:
                    xx = y % 1
                resized = pg.transform.scale(wall, (h, h))
                subsurface = pg.Surface.subsurface(resized, (min(int(h) - 1, int(xx * h)), 0, 1, int(h)))
                frame.blit(subsurface, (i, (vertical_res - h) * 0.5))
                break

    upscaled = pg.transform.scale(frame, [800, 600])

    upscaled.blit(font.render(fps, 1, [255, 255, 255]), [0, 0])
    screen.blit(upscaled, (0, 0))

    # my code starts 
    # Clear the screen
    # screen.fill((1, 1, 1))
     # Blit the text onto the screen
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    # Update the display
    # pg.display.flip()

    #my code ends

    pg.display.update()


pg.quit()