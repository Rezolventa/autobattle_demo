from rendering import get_scaled_image, center_coords_to_left_up, get_spot_coords


class FrameSlot:
    pos = None
    unit = None
    team = None

    def __init__(self, pos, unit, team):
        self.pos = pos
        self.unit = unit
        self.team = team


class BattleFrame:
    """Сущность-окно, внутри которого отрисовывается автобой"""
    teamA = []  # команда игрока
    teamB = []  # команда ИИ

    sprites = {
        'zombie_1': get_scaled_image('sprites/zombie_1.png', 4),
        'zombie_1_attack': get_scaled_image('sprites/zombie_1_attack.png', 4),
        'zombie_hit': get_scaled_image('sprites/zombie_hit.png', 4),
        'player': get_scaled_image('sprites/player.png', 4),  # +0, +50, +50 color
        'player_attack': get_scaled_image('sprites/player_attack.png', 4),
        'player_hit': get_scaled_image('sprites/player_hit.png', 4)
    }

    win = None

    def start(self):
        # распределяем таргеты
        # for slot in self.teamA + self.teamB:
        #     slot.obj.set_target()
        for slot in self.teamA:
            slot.unit.set_target_from(self.teamB)
        for slot in self.teamB:
            slot.unit.set_target_from(self.teamA)

    def render_all(self):
        # отображаем только живых
        for slot in self.teamA:
            unit = slot.unit
            if unit.hp > 0:
                if unit.filter_countdown > 0:
                    the_sprite = self.sprites.get('player_hit')
                elif unit.animation_countdown > 0:
                    the_sprite = self.sprites.get('player_attack')
                else:
                    the_sprite = self.sprites.get('player')

                coords = center_coords_to_left_up(get_spot_coords('A', slot.pos), the_sprite)
                self.win.blit(the_sprite, coords)

        for slot in self.teamB:
            unit = slot.unit
            if unit.hp > 0:
                if unit.filter_countdown > 0:
                    the_sprite = self.sprites.get('zombie_hit')
                elif unit.animation_countdown > 0:
                    the_sprite = self.sprites.get('zombie_1_attack')
                else:
                    the_sprite = self.sprites.get('zombie_1')

                coords = center_coords_to_left_up(get_spot_coords('B', slot.pos), the_sprite)
                self.win.blit(the_sprite, coords)

    def add_unit(self, team, unit):
        if team == 'A':
            self.teamA.append(FrameSlot(len(self.teamA) + 1, unit, self.teamA))
        elif team == 'B':
            self.teamB.append(FrameSlot(len(self.teamB) + 1, unit, self.teamB))
        unit.frame = self

    def handle_tick(self):
        self.handle_team(self.teamA, self.teamB)
        self.handle_team(self.teamB, self.teamA)

    def handle_team(self, creature_list_1, creature_list_2):
        for slot in creature_list_1:
            unit = slot.unit
            if unit.attack_cooldown == 0:
                # кулдаун атаки закончился, накручиваем
                unit.set_attack_cooldown()
                # меняем статус для анимации
                unit.set_animation_countdown()
                # unit.set_animation(action='attack')
                # если предыдущая цель есть и жива, продолжаем ее атаковать
                if unit.target:
                    # снимаем у цели хп
                    unit.target.hp -= unit.attack
                    print(unit.name, 'attacks', unit.target.name, 'for', unit.attack, '({} left)'.format(unit.target.hp))

                    if unit.target.hp > 0:
                        # включаем фильтр попадания
                        unit.target.set_filter_countdown()
                    else:
                        # обрабатываем смерть юнита
                        print(unit.target.name, 'dies!')
                        # creature_list_2.remove(unit.target)
                        for slot in creature_list_2:
                            if slot.unit == unit.target:
                                creature_list_2.remove(slot)
                        # unit.set_target()
                        unit.set_target_from(creature_list_2)

                # иначе выбираем новую
                else:
                    unit.set_target()

            else:
                # снимаем тик атаки
                unit.attack_cooldown -= 1

            # уменьшаем тики "анимаций"
            unit.animation_countdown -= 1
            unit.filter_countdown -= 1
