# Copyright 2023 Elijah Gordon (NitrixXero) <nitrixxero@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pygame
import random

black = (0, 0, 0)


def initialize_characters():
    return [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'ァ', 'ア', 'ィ', 'イ', 'ゥ', 'ウ', 'ェ', 'エ', 'ォ',
        'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ',
        'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ', 'セ',
        'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ヂ', 'ッ', 'ツ',
        'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ',
        'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ',
        'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ',
        'ム', 'メ', 'モ', 'ャ', 'ヤ', 'ュ', 'ユ', 'ョ', 'ヨ',
        'ラ', 'リ', 'ル', 'レ', 'ロ', 'ヮ', 'ワ', 'ヰ', 'ヱ',
        'ヲ', 'ン', 'ヴ', 'ヵ', 'ヶ', 'ヷ', 'ヸ', 'ヹ', 'ヺ',
        '・', 'ー', 'ヽ', 'ヾ'
    ]


def load_font(font_path, size):
    return pygame.font.Font(font_path, size)


def initialize_display():
    pygame.display.set_caption('Matorikkusu')
    return pygame.display.set_mode((1080, 1920), pygame.RESIZABLE)


class Matorikkusu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.chars = initialize_characters()
        self.char_size = 36
        self.line_length = random.randint(10, 20)
        self.line = [random.choice(self.chars) for _ in range(self.line_length)]
        self.vertical_step = 10
        self.alpha = 255
        self.trail_length = 4
        self.trail = []

    def draw(self, screen):
        if self.y < 1920:
            self.y += self.vertical_step * (self.line_length / 20)
            distance_to_bottom = 1920 - self.y
            fade_range = 200

            if distance_to_bottom < fade_range:
                self.alpha = int((distance_to_bottom / fade_range) * 255)

            self.trail.append((self.x, self.y))

            if len(self.trail) > self.trail_length:
                self.trail.pop(0)

            for i in range(self.line_length):
                if random.random() < 0.02:
                    self.line[i] = random.choice(self.chars)

        else:
            self.y = -40 * random.randrange(1, 5)
            self.alpha = 255
            self.trail = []

        char_font = load_font('font/MS Mincho.ttf', self.char_size)

        for i, char in enumerate(self.line):
            char_surface = char_font.render(char, True, self.color)
            fade_distance = 1920 - self.y - i * 30
            if fade_distance < 0:
                fade_distance = 0
            fade_alpha = int((1 - fade_distance / 1920) * self.alpha)
            char_surface.set_alpha(fade_alpha)
            screen.blit(char_surface, (self.x, self.y + i * 30))

            for j, trail_pos in enumerate(reversed(self.trail)):
                trail_alpha = int((1 - j / self.trail_length) * fade_alpha)
                trail_surface = char_font.render(char, True, self.color)
                trail_surface.set_alpha(trail_alpha)
                screen.blit(trail_surface, (trail_pos[0], trail_pos[1] + i * 30))

    def set_color(self, color):
        self.color = color

    def decrease_speed(self):
        self.vertical_step = max(self.vertical_step - 5, 5)

    def increase_speed(self):
        self.vertical_step = min(self.vertical_step + 5, 100)


def change_color(key):
    colors = {
        pygame.K_b: (0, 0, 255),
        pygame.K_c: (0, 255, 255),
        pygame.K_d: (110, 75, 38),
        pygame.K_e: (255, 121, 77),
        pygame.K_f: (246, 74, 138),
        pygame.K_g: (0, 255, 0),
        pygame.K_h: (223, 115, 255),
        pygame.K_r: (255, 0, 0),
        pygame.K_w: (255, 255, 255),
        pygame.K_y: (255, 255, 0),
        pygame.K_m: (255, 0, 255),
        pygame.K_o: (128, 128, 0),
        pygame.K_t: (0, 128, 128),
    }
    if key in colors:
        return colors[key]
    else:
        return None


def main():
    pygame.init()

    custom_font = load_font('font/MS Mincho.ttf', 24)

    window = initialize_display()

    icon = pygame.image.load('icon/icon.png')
    pygame.display.set_icon(icon)

    pygame.mixer.init()

    audio = pygame.mixer.Sound('audio/audio.wav')
    audio.play(-1)

    music_muted = False

    matrix_symbols = [Matorikkusu(x, random.randint(0, 1920)) for x in range(0, 1080, 30)]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    for symbol in matrix_symbols:
                        symbol.decrease_speed()
                elif event.key == pygame.K_RIGHT:
                    for symbol in matrix_symbols:
                        symbol.increase_speed()
                elif event.key == pygame.K_p:
                    pygame.mixer.pause()
                    music_muted = True
                elif event.key == pygame.K_u:
                    pygame.mixer.unpause()
                    music_muted = False
                else:
                    new_color = change_color(event.key)
                    if new_color:
                        for symbol in matrix_symbols:
                            symbol.set_color(new_color)

        window.fill(black)

        for symbol in matrix_symbols:
            symbol.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.stop()
    pygame.quit()


if __name__ == "__main__":
        main()
