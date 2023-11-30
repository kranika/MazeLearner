pg.draw.circle(screen, PACMAN_COLOR, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
    pg.draw.polygon(screen, BACKGROUND_COLOR, [(pacman_x, pacman_y)] + [
        (pacman_x + PACMAN_RADIUS * pg.math.Vector2(1, 0).rotate(pacman_angle + angle).x,
         pacman_y + PACMAN_RADIUS * pg.math.Vector2(1, 0).rotate(pacman_angle + angle).y)
        for angle in range(-30, 31, 10)
    ])
