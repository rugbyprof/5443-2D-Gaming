import random
import math
from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import math as pymath


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def distance(p1, p2):
    if isinstance(p1, tuple):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)
    else:
        v1 = pymath.Vector2(p1)
        v2 = pymath.Vector2(p2)
        return v1.distance_to(v2)


def direction(v1, v2):
    dot = v1.dot(v2)
    mag1 = v1.magnitude()
    mag2 = v2.magnitude()
    cos_angle = dot / (mag1 * mag2)
    angle = math.degrees(math.acos(cos_angle))
    return angle


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)
