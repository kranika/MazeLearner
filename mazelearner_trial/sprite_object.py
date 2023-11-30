import pygame as pg
from settings import *
import os
from collections import deque
from random import choice
from random import randint
from map import *


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images


class Letter(AnimatedSprite):
    def __init__(self, game, pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180, char='A'):
        path = f'resources/sprites/letters/{char}.png'
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.float_speed = 0.03
        self.char = char  # Add this line to set the 'char' attribute

    def update(self):
        self.check_animation_time()
        self.float()

    def float(self):
        self.y += self.float_speed
    
    def get_char(self):
        return self.char

    def draw(self):
        self.game.screen.blit(self.image, (self.screen_x - self.sprite_half_width, self.y))


class FloatingLettersHandler:
    def __init__(self, game):
        self.game = game
        self.word = ""
        self.letters = [Letter(game, pos=self.get_letter_position(char), char=char) for char in self.word]

    def update(self):
        for letter in self.letters:
            letter.update()
            if letter.y > HEIGHT:
                letter.y = 0

    def get_letter_position(self, char):
        # Get coordinates of the corresponding maze value
        maze_coordinates = [(i, j) for j, row in enumerate(mini_map) for i, value in enumerate(row) if value == char]

        # Choose a random position from the available coordinates
        chosen_position = choice(maze_coordinates)

        # Calculate the position in pixels based on maze coordinates and TILE_SIZE
        pixel_position = (chosen_position[0] * TILE_SIZE + TILE_SIZE // 2, chosen_position[1] * TILE_SIZE + TILE_SIZE // 2)

        return pixel_position

# class FloatingLettersHandler:
#     def __init__(self, game):
#         self.game = game
#         self.word = "M"
#         self.letters = [Letter(game, pos=self.get_letter_position(char), char=char) for char in self.word]

#     def update(self):
#         for letter in self.letters:
#             position = self.get_letter_position(letter.get_char())
#             if position:
#                 letter.y = position[1]
#                 letter.update()
#                 if letter.y > HEIGHT:
#                     letter.y = 0

#     def get_letter_position(self, char):
#         # Get coordinates of the corresponding maze value
#         maze_coordinates = [(i, j) for j, row in enumerate(mini_map) for i, value in enumerate(row) if value == char]

#         if maze_coordinates:
#             # Choose a random position from the available coordinates
#             chosen_position = choice(maze_coordinates)

#             # Calculate the position in pixels based on maze coordinates and TILE_SIZE
#             pixel_position = (chosen_position[0] * TILE_SIZE, chosen_position[1] * TILE_SIZE)

#             # Set a random Y-coordinate within a certain range to create variation
#             pixel_position = (pixel_position[0], pixel_position[1] + randint(-20, 20))

#             return pixel_position
#         else:
#             return None  # Handle the case when there are no coordinates for the letter