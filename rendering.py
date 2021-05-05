import pygame

from const import WIN_WIDTH, WIN_HEIGHT

pygame.font.init()
default_font = pygame.font.SysFont('serif', 30)
default_color = pygame.Color(255, 0, 0)


def get_scaled_image(image, k):
    loaded = pygame.image.load(image)
    size = loaded.get_size()
    return pygame.transform.scale(loaded, (int(size[0] * k), int(size[1] * k)))


def center_coords_to_left_up(coord_tuple, image):
    size = image.get_size()
    x = coord_tuple[0] - size[0] // 2
    y = coord_tuple[1] - size[1] // 2
    return (x, y)


def get_spot_coords(team, number):
    """
    Возвращает координаты центров позиций спрайтов.
    Первый спрайт посередине, второй сверху, третий снизу.
    """
    sign_x = -1 if team == 'A' else 1
    x = WIN_WIDTH // 2 + sign_x * 150

    sign_y = {1: 0, 2: -1, 3: 1}.get(number)
    y = WIN_HEIGHT // 2 + sign_y * 150

    return (x, y)