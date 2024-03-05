import os
from typing import List, Tuple
import pygame
from enum import Enum
import collections
import random

WIDTH, HEIGHT = 1920, 1080
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (10, 10, 100)
Green = (10, 200, 10)
Background = (50, 50, 50)
TextBackground = (0, 0, 0)
font_base_size = 540
font_scale = 1.3
TARGET_FPS = 240


# traverse root directory, and list directories as dirs and files as files
def get_sound_paths(path) -> dict[str, List[str]]:
    result = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            dirname = os.path.basename(root)
            fullpath = os.path.abspath(os.path.join(root, file))
            # print(dirname, ": ", fullpath)
            if (file.count(".mp3") > 0):
                if (result.get(dirname)):
                    result[dirname].append(fullpath)
                else:
                    result[dirname] = [fullpath]
    # print(result)
    return result


class LetterStore:
    text: str
    fontFile: str
    fontSize: int
    fontSetting: pygame.Font
    fontSettingBg: pygame.Font
    surface: pygame.Surface
    surfaceBg: pygame.Surface
    soundPaths: list[str]
    soundList: list[pygame.mixer.Sound]

    def __init__(self, text: str, sound_paths: dict[str, List[str]], fontSize=font_base_size, textColor=White, textBackgroundColor=TextBackground, fontFile='freesansbold.ttf'):
        self.text = str.upper(text)  # + " " + text
        self.fontSetting = pygame.font.Font(fontFile, fontSize)
        self.fontSettingBg = pygame.font.Font(fontFile, fontSize)
        self.surface = self.fontSetting.render(self.text, True, textColor)
        self.surfaceBg = self.fontSettingBg.render(self.text, True, textBackgroundColor)
        self.soundPaths = sound_paths[text]
        self.soundList = []
        print(text)
        for path in self.soundPaths:
            print("loading sound:", path)
            self.soundList.append(pygame.mixer.Sound(path))
        self.textBgOffset = [6, 6]

    def blit(self, surface: pygame.Surface, position: List[int]):
        textRectBg = self.surfaceBg.get_rect()
        textRectBg.center = tuple([position[0]+self.textBgOffset[0], position[1]+self.textBgOffset[1]])
        surface.blit(self.surfaceBg, textRectBg)

        textRect = self.surface.get_rect()
        textRect.center = tuple(position)
        surface.blit(self.surface, textRect)
        # print(self.soundPaths)

    def play(self):
        if len(self.soundList) > 0:
            pick = random.randrange(len(self.soundList))
            self.soundList[pick].play(0)


activeLetters = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
                 pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z,]


def create_letters(sound_paths: dict[str, List[str]]):
    return {
        pygame.K_a: LetterStore('a', sound_paths),
        pygame.K_b: LetterStore('b', sound_paths),
        pygame.K_c: LetterStore('c', sound_paths),
        pygame.K_d: LetterStore('d', sound_paths),
        pygame.K_e: LetterStore('e', sound_paths),
        pygame.K_f: LetterStore('f', sound_paths),
        pygame.K_g: LetterStore('g', sound_paths),
        pygame.K_h: LetterStore('h', sound_paths),
        pygame.K_i: LetterStore('i', sound_paths),
        pygame.K_j: LetterStore('j', sound_paths),
        pygame.K_k: LetterStore('k', sound_paths),
        pygame.K_l: LetterStore('l', sound_paths),
        pygame.K_m: LetterStore('m', sound_paths),
        pygame.K_n: LetterStore('n', sound_paths),
        pygame.K_o: LetterStore('o', sound_paths),
        pygame.K_p: LetterStore('p', sound_paths),
        pygame.K_q: LetterStore('q', sound_paths),
        pygame.K_r: LetterStore('r', sound_paths),
        pygame.K_s: LetterStore('s', sound_paths),
        pygame.K_t: LetterStore('t', sound_paths),
        pygame.K_u: LetterStore('u', sound_paths),
        pygame.K_v: LetterStore('v', sound_paths),
        pygame.K_w: LetterStore('w', sound_paths),
        pygame.K_x: LetterStore('x', sound_paths),
        pygame.K_y: LetterStore('y', sound_paths),
        pygame.K_z: LetterStore('z', sound_paths),
    }


# def draw_window(display_surface: pygame.Surface, key_queue: collections.deque, letters):
def draw_window(display_surface: pygame.Surface, current_key: int, letters):
    display_surface.fill(Background)
    if (current_key >= 0):
        letters[current_key].blit(display_surface, [WIDTH // 2, HEIGHT // 2])
    pygame.display.update()


def check_quit(events: List[pygame.Event]):
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True


def key_state(keys_pressed: pygame.key.ScancodeWrapper, key_queue: collections.deque) -> int:
    press_count = 0
    for letter in activeLetters:
        if keys_pressed[letter]:
            press_count = press_count + 1
            if (key_queue.count(letter) == 0):
                key_queue.append(letter)

    if (press_count == 0):
        key_queue.clear()

    if (len(key_queue) > 0):
        return key_queue[0]

    if keys_pressed[pygame.K_ESCAPE]:
        return -1
    return 0


def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    sound_paths = get_sound_paths(os.path.join(".", "Sounds"))
    key_queue = collections.deque()
    pygame.init()
    pygame.mixer.init()
    letters = create_letters(sound_paths)
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Letter Game")
    current_key = -1

    run = True
    clock = pygame.time.Clock()
    no_press = True
    while run:
        clock.tick(TARGET_FPS)
        run = check_quit(pygame.event.get())
        new_key = key_state(pygame.key.get_pressed(), key_queue)

        if new_key > 0:
            current_key = new_key
        elif new_key == -1:
            current_key = -1

        if no_press and len(key_queue) > 0:
            letters[key_queue[0]].play()
        # draw_window(display_surface, key_queue, letters)
        draw_window(display_surface, current_key, letters)

        no_press = len(key_queue) == 0
    pygame.quit()


if __name__ == "__main__":
    main()
