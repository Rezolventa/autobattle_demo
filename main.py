from random import randint

import pygame

from const import WIN_WIDTH, WIN_HEIGHT, FRAME_RATE
from frame import BattleFrame

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('auto battle')


class Unit:
    name = None
    hp = None
    attack = None
    attack_delay = None
    hit_chance = None
    crit_chance = None
    busy = None
    target = None
    frame = None
    status = None
    animation_countdown = 0
    filter_countdown = 0

    STATUS_IDLE = 'idle'
    STATUS_ATTACK = 'attack'

    def __init__(self, name, hp, attack , attack_delay, hit_chance, crit_chance):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.attack_delay = attack_delay
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance
        self.status = self.STATUS_IDLE
        self.set_busy()

    def set_busy(self):
        self.busy = round(FRAME_RATE * self.attack_delay)

    def set_target(self):
        # выбрать рандомную цель из другой команды
        if self in self.frame.teamA:
            if len(self.frame.teamB):
                self.target = self.frame.teamB[randint(0, len(self.frame.teamB) - 1)]
                print(self.name, 'targets', self.target.name)
            else:
                self.target = None
        else:
            if len(self.frame.teamA):
                self.target  = self.frame.teamA[randint(0, len(self.frame.teamA) - 1)]
                print(self.name, 'targets', self.target.name)
            else:
                self.target = None

    def set_status(self, status):
        self.status = status

        if status == self.STATUS_ATTACK:
            self.animation_countdown = FRAME_RATE * 0.5  # полсекунды
        else:
            self.animation_countdown = 0

    def take_hit(self, damage):
        pass

    def attack(self):
        pass

player = Unit('player', 450, 15, 1.40, 0.80, 0.15)
enemy1 = Unit('AI-1', 100, 25, 2, 0.80, 0.05)
enemy2 = Unit('AI-2', 100, 23, 2.2, 0.80, 0.05)
enemy3 = Unit('AI-3', 100, 45, 4, 0.80, 0.05)

frame = BattleFrame()
frame.add_unit('A', player)
frame.add_unit('B', enemy1)
frame.add_unit('B', enemy2)
frame.add_unit('B', enemy3)
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

if __name__ == '__main__':
    main_loop()
