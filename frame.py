import pygame

from const import WIN_WIDTH, WIN_HEIGHT
from rendering import get_scaled_image, center_coords_to_left_up


class BattleFrame:
    """Сущность-окно, внутри которого отрисовывается автобой"""
    teamA = []  # команда игрока
    teamB = []  # команда ИИ

    zombie_1 = get_scaled_image('sprites/zombie_1.png', 4)
    zombie_1_attack = get_scaled_image('sprites/zombie_1_attack.png', 4)

    win = None

    def start(self):
        for obj in self.teamA + self.teamB:
            obj.set_target()

    def render_all(self):
        i = 0
        # отображаем только живых
        for obj in self.teamA:
            i += 1
            if obj.hp > 0:
                pygame.draw.circle(self.win, (255, 155, 0), self.get_spot_coords('A', i), 35)

        i = 0
        for obj in self.teamB:
            i += 1
            if obj.hp > 0:
                if obj.status == obj.STATUS_ATTACK:
                    coords = center_coords_to_left_up(self.get_spot_coords('B', i), self.zombie_1_attack)
                    self.win.blit(self.zombie_1_attack, coords)
                else:
                    coords = center_coords_to_left_up(self.get_spot_coords('B', i), self.zombie_1)
                    self.win.blit(self.zombie_1, coords)

    # отдельно - работа с координатами
    def get_spot_coords(self, team, number):
        """
        Возвращает координаты центров позиций спрайтов.
        Первый спрайт посередине, второй сверху, третий снизу.
        """
        sign_x = -1 if team == 'A' else 1
        x = WIN_WIDTH // 2 + sign_x * 150

        sign_y = {1: 0, 2: -1, 3: 1}.get(number)
        y = WIN_HEIGHT // 2 + sign_y * 150

        return (x, y)

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
            if obj.busy == 0:
                # кулдаун атаки закончился, накручиваем
                obj.set_busy()
                # меняем статус для анимации
                obj.set_status(obj.STATUS_ATTACK)
                # если предыдущая цель есть и жива, продолжаем ее атаковать
                if obj.target:
                    # снимаем у цели хп
                    obj.target.hp -= obj.attack  # TODO: обработчик obj.apply_damage?
                    print(obj.name, 'attacks', obj.target.name, 'for', obj.attack, '({} left)'.format(obj.target.hp))

                    # обрабатываем последствия
                    if not obj.target.hp > 0:
                        creature_list_2.remove(obj.target)
                        obj.set_target()


                # иначе выбираем новую
                else:
                    obj.set_target()

            else:
                # снимаем тик
                obj.busy -= 1

            obj.animation_countdown -= 1
            if obj.animation_countdown == 0:
                obj.set_status(obj.STATUS_IDLE)