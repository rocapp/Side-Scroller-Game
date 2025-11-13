import pygame
import os


def load_image(filename):
    """Loads an image from the 'images' directory, relative to this file."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return pygame.image.load(os.path.join(base_path, "images", filename))

def load_sound(filename):
    """Loads a sound from the 'sounds' directory, relative to this file."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return pygame.mixer.Sound(os.path.join(base_path, "sounds", filename))



class Assets:
    def __init__(self):
        self.bg = load_image("bg.png").convert()
        self.run = [load_image(str(x) + ".png") for x in range(8, 16)]
        self.jump = [load_image(str(x) + ".png") for x in range(1, 8)]
        self.slide = [
            load_image("S1.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S2.png"),
            load_image("S3.png"),
            load_image("S4.png"),
            load_image("S5.png"),
        ]
        self.fall = load_image("0.png")
        self.saw_rotate = [
            load_image("SAW0.png"),
            load_image("SAW1.png"),
            load_image("SAW2.png"),
            load_image("SAW3.png"),
        ]
        self.spike_img = load_image("spike.png")
        self.bird = load_image("bird.png")
        self.shield = load_image("shield.png")
        self.score_multiplier = load_image("score_multiplier.png")
        self.ground_enemy = load_image("ground_enemy.png")
        self.jump_sound = load_sound("jump.wav")
        self.powerup_sound = load_sound("powerup.wav")
        self.hit_sound = load_sound("hit.wav")

def init_assets():
    return Assets()
