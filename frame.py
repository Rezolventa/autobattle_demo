import pygame

from rendering import get_scaled_image, center_coords_to_left_up, get_spot_coords


class BattleFrame:
    """Сущность-окно, внутри которого отрисовывается автобой"""
    teamA = []  # команда игрока
    teamB = []  # команда ИИ

    zombie_1 = get_scaled_image('sprites/zombie_1.png', 4)
    zombie_1_attack = get_scaled_image('sprites/zombie_1_attack.png', 4)

    win = None
    # filter = None

    def start(self):
        for obj in self.teamA + self.teamB:
            obj.set_target()

    def render_all(self):
        i = 0
        # отображаем только живых
        for obj in self.teamA:
            i += 1
            if obj.hp > 0:
                pygame.draw.circle(self.win, (255, 155, 0), get_spot_coords('A', i), 35)

        i = 0
        for obj in self.teamB:
            i += 1
            if obj.hp > 0:
                # special_flags = pygame.BLEND_RGBA_SUB if obj.filter_countdown > 0 else None
                if obj.animation_countdown > 0:
                    coords = center_coords_to_left_up(get_spot_coords('B', i), self.zombie_1_attack)
                    # self.filter.blit(self.zombie_1_attack, coords)
                    # self.win.blit(self.filter, (0, 0))
                    self.win.blit(self.zombie_1_attack, coords)
                else:
                    coords = center_coords_to_left_up(get_spot_coords('B', i), self.zombie_1)
                    self.win.blit(self.zombie_1, coords)

    def add_unit(self, team, unit):
        if team == 'A':
            self.teamA.append(unit)
        elif team == 'B':
            self.teamB.append(unit)
        unit.frame = self

    def handle_tick(self):
        self.handle_team(self.teamA, self.teamB)
        self.handle_team(self.teamB, self.teamA)

    def handle_team(self, creature_list_1, creature_list_2):
        for obj in creature_list_1:
            if obj.attack_cooldown == 0:
                # кулдаун атаки закончился, накручиваем
                obj.set_attack_cooldown()
                # меняем статус для анимации
                obj.set_animation_countdown()
                # если предыдущая цель есть и жива, продолжаем ее атаковать
                if obj.target:
                    # снимаем у цели хп
                    obj.target.hp -= obj.attack
                    print(obj.name, 'attacks', obj.target.name, 'for', obj.attack, '({} left)'.format(obj.target.hp))

                    # включаем фильтр попадания
                    # obj.target.set_filter_countdown()

                    # обрабатываем последствия
                    if not obj.target.hp > 0:
                        print(obj.name, 'dies!')
                        creature_list_2.remove(obj.target)
                        obj.set_target()

                # иначе выбираем новую
                else:
                    obj.set_target()

            else:
                # снимаем тик
                obj.attack_cooldown -= 1

            obj.animation_countdown -= 1
