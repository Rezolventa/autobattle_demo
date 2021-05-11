from random import randint

from const import FRAME_RATE
from rendering import get_scaled_image


class Unit:
    attack_cooldown = None
    target = None
    frame = None
    animation_countdown = 0
    filter_countdown = 0

    def __init__(
        self,
        name, unit_type, tier,  # классификация
        hp, attack, attack_delay, hit_chance, crit_chance  # боевые статы
    ):
        self.name = name
        self.unit_type = unit_type
        self.tier = tier
        self.hp = hp
        self.attack = attack
        self.attack_delay = attack_delay
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance
        self.set_attack_cooldown()

        # спрайты
        self.image_idle = get_scaled_image('sprites/{}_{}.png'.format(self.unit_type, self.tier), 4)
        self.image_attack = get_scaled_image('sprites/{}_{}_attack.png'.format(self.unit_type, self.tier), 4)
        self.image_hit = get_scaled_image('sprites/{}_hit.png'.format(self.unit_type), 4)

    def set_attack_cooldown(self):
        """Накручивает кулдаун атаки (в фреймах)"""
        # TODO: reset_attack_cooldown больше подходит?
        self.attack_cooldown = round(FRAME_RATE * self.attack_delay)

    def set_target(self):
        # выбрать рандомную цель из другой команды
        if self in self.frame.teamA:
            if len(self.frame.teamB):
                self.target = self.frame.teamB[randint(0, len(self.frame.teamB) - 1)].unit
                print(self.name, 'targets', self.target.name)
            else:
                self.target = None
        else:
            if len(self.frame.teamA):
                self.target = self.frame.teamA[randint(0, len(self.frame.teamA) - 1)].unit
                print(self.name, 'targets', self.target.name)
            else:
                self.target = None

    def set_target_from(self, team):
        if len(team):
            self.target = team[randint(0, len(team) - 1)].unit
            print(self.name, 'targets', self.target.name)
        else:
            self.target = None

    def set_animation_countdown(self):
        self.animation_countdown = FRAME_RATE * 0.5

    def set_filter_countdown(self):
        self.filter_countdown = FRAME_RATE * 0.3
