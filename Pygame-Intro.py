import pygame as pg

pg.init()


DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption('Tic-Tac-Toe')
clock = pg.time.Clock()

Clickable_Areas = {1: pg.Rect(10, 10, 90, 90),
                   2: pg.Rect(110, 10, 90, 90),
                   3: pg.Rect(210, 10, 90, 90),
                   4: pg.Rect(10, 110, 90, 90),
                   5: pg.Rect(110, 110, 90, 90),
                   6: pg.Rect(210, 110, 90, 90),
                   7: pg.Rect(10, 210, 90, 90),
                   8: pg.Rect(110, 210, 90, 90),
                   9: pg.Rect(210, 210, 90, 90),
                   }
Cross = pg.image.load('Cross.png')
Cross = pg.transform.scale(Cross, (80, 80))
Circle = pg.image.load('Circle.png')
Circle = pg.transform.scale(Circle, (80, 80))

crashed = False
cell_vals = []
while not crashed:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True

        screen.fill(WHITE)
        pg.draw.line(screen, BLACK, [100, 10], [100, 290], 5)
        pg.draw.line(screen, BLACK, [200, 10], [200, 290], 5)
        pg.draw.line(screen, BLACK, [10, 100], [290, 100], 5)
        pg.draw.line(screen, BLACK, [10, 200], [290, 200], 5)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button.
                # Check if the rect collides with the mouse pos.
                for area in Clickable_Areas:
                    if Clickable_Areas[area].collidepoint(pg.mouse.get_pos()):
                        cell_vals.append(area)
                        print(f'{area} clicked.')
    if not cell_vals == []:
        for area in cell_vals:
            screen.blit(Cross, Clickable_Areas[area])
            break
        screen.fill(WHITE)
        font = pg.font.Font('Roboto-Regular.ttf', 45)
        TextSurf = font.render('You Won!!', True, GREEN)
        TextRect = TextSurf.get_rect()
        TextRect.center = (150, 150)
        screen.blit(TextSurf, TextRect)
    pg.display.update()
    clock.tick(60)
pg.quit()
quit()
