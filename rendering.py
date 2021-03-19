import pygame

def get_scaled_image(image, k):
    loaded = pygame.image.load(image)
    size = loaded.get_size()
    return pygame.transform.scale(loaded, (int(size[0] * k), int(size[1] * k)))


def center_coords_to_left_up(coord_tuple, image):
    size = image.get_size()
    x = coord_tuple[0] - size[0] // 2
    y = coord_tuple[1] - size[1] // 2
    return (x, y)