import pygame

from const import WIN_WIDTH, WIN_HEIGHT, FRAME_RATE
from frame import BattleFrame
from units import Unit

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("auto battle")


player = Unit("player", "player", 0, 450, 15, 1.40, 0.80, 0.15)
enemy1 = Unit("AI-1", "zombie", 1, 100, 25, 2, 0.80, 0.05)
enemy2 = Unit("AI-2", "zombie", 2, 100, 23, 2.2, 0.80, 0.05)
enemy3 = Unit("AI-3", "zombie", 3, 100, 45, 4, 0.80, 0.05)

frame = BattleFrame()
frame.add_unit("A", player)
frame.add_unit("B", enemy1)
frame.add_unit("B", enemy2)
frame.add_unit("B", enemy3)
frame.win = win
frame.start()


def main_loop():
    run = True
    while run:
        clock.tick(FRAME_RATE)

        win.fill((0, 0, 0))

        frame.render_all()
        frame.handle_tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()


if __name__ == "__main__":
    main_loop()
