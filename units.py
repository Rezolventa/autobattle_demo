from random import randint

from const import FRAME_RATE


class Unit:
    name = None
    hp = None
    attack = None
    attack_delay = None
    hit_chance = None
    crit_chance = None

    attack_cooldown = None
    target = None
    frame = None
    animation_countdown = 0
    # filter_countdown = 0

    def __init__(self, name, hp, attack , attack_delay, hit_chance, crit_chance):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.attack_delay = attack_delay
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance
        self.set_attack_cooldown()

    def set_attack_cooldown(self):
        self.attack_cooldown = round(FRAME_RATE * self.attack_delay)

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

    def set_animation_countdown(self):
        self.animation_countdown = FRAME_RATE * 0.75

    # def set_filter_countdown(self):
    #     self.filter_countdown = FRAME_RATE * 0.5
