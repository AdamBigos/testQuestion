import pygame
from config import game_window


def tile_coordinates(row_number):
    x = []
    for i in range(row_number):
        for j in range(4):
            x.append([125 + j * 120, 160 + i * 55])
    return x


def word_coordinates(row_number):
    x = []
    for i in range(row_number):
        for j in range(4):
            x.append([182 + j * 120, 173 + i * 55])
    return x


def possible_choices():
    x = ['a', 'b', 'c', 'd']
    y = ['1', '2', '3', '4']
    combine = []
    for i in y:
        for j in x:
            combine.append(j + i)
    return combine


# text display function
def draw_text(text, font_size, text_color, bg_color, x, y, position):
    font = pygame.font.Font(None, font_size)
    text_obj = font.render(text, True, text_color, bg_color)
    text_position = text_obj.get_rect()
    if position == "center":
        text_position.midtop = (x, y)
    else:
        text_position.topleft = (x, y)
    game_window.blit(text_obj, text_position)
    # helpful thing to position text elements should be deleted in final game
    return [text_obj.get_width(), text_obj.get_height()]
