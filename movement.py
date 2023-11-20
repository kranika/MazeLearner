import math
import pygame as pg

def movement(posx, posy, rot, mapa, elapsed_time):
    if pg.mouse.get_focused():
        p_mouse = pg.mouse.get_rel()
        rot = rot + min(max((p_mouse[0]) / 200, -0.2), 0.2)

    pressed_keys = pg.key.get_pressed()
    x, y = posx, posy

    forward = (pressed_keys[pg.K_UP] or pressed_keys[ord('w')]) - (pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')])
    sideways = (pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]) - (
                pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')])

    if forward * sideways != 0:
        forward, sideways = forward * 0.7, sideways * 0.7

    x += elapsed_time * (forward * math.cos(rot) + sideways * math.sin(rot))
    y += elapsed_time * (forward * math.sin(rot) - sideways * math.cos(rot))

    if (mapa[int(x - 0.3)][int(y - 0.3)] == 0
            and mapa[int(x + 0.3)][int(y + 0.3)] == 0
            and mapa[int(x + 0.3)][int(y - 0.3)] == 0
            and mapa[int(x - 0.3)][int(y + 0.3)] == 0):
        return x, y, rot
    else:
        return posx, posy, rot