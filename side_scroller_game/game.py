import pygame
from pygame.locals import *
import random
from .assets import init_assets
from .player import Player
from .obstacles import Saw, Spike, Bird, GroundEnemy
from .powerups import Shield, ScoreMultiplier


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.W, self.H = 800, 437
        self.win = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Side Scroller")
        self.assets = init_assets()
        self.player = Player(200, 313, 64, 64, self.assets)
        self.bgX = 0
        self.bgX2 = self.assets.bg.get_width()
        self.clock = pygame.time.Clock()
        self.speed = 30
        self.score = 0
        self.obstacles = []
        self.powerups = []
        self.pause = 0
        self.fallSpeed = 0
        self.score_multiplier_timer = 0
        self.font = pygame.font.SysFont("comicsans", 30)

    def run(self):
        self.main_menu()
        pygame.time.set_timer(USEREVENT + 1, 500)
        pygame.time.set_timer(USEREVENT + 2, 3000)
        pygame.time.set_timer(USEREVENT + 3, 10000)
        run = True
        while run:
            self.update_score()
            self.handle_collisions()
            self.move_background()
            run = self.handle_events()
            self.handle_input()
            self.redraw_window()
            self.clock.tick(self.speed)
        pygame.quit()

    def main_menu(self):
        run = True
        while run:
            self.win.blit(self.assets.bg, (0, 0))
            large_font = pygame.font.SysFont("comicsans", 80)
            title = large_font.render("Side Scroller", 1, (255, 255, 255))
            self.win.blit(title, (self.W / 2 - title.get_width() / 2, 150))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            button_width = 200
            button_height = 50
            start_button_x = self.W / 2 - button_width / 2
            start_button_y = 250
            quit_button_x = self.W / 2 - button_width / 2
            quit_button_y = 320

            if start_button_x + button_width > mouse[0] > start_button_x and start_button_y + button_height > mouse[1] > start_button_y:
                pygame.draw.rect(self.win, (0, 255, 0), (start_button_x,
                                 start_button_y, button_width, button_height))
                if click[0] == 1:
                    run = False
            else:
                pygame.draw.rect(self.win, (0, 200, 0), (start_button_x,
                                 start_button_y, button_width, button_height))

            if quit_button_x + button_width > mouse[0] > quit_button_x and quit_button_y + button_height > mouse[1] > quit_button_y:
                pygame.draw.rect(self.win, (255, 0, 0), (quit_button_x,
                                 quit_button_y, button_width, button_height))
                if click[0] == 1:
                    pygame.quit()
                    exit()
            else:
                pygame.draw.rect(self.win, (200, 0, 0), (quit_button_x,
                                 quit_button_y, button_width, button_height))

            small_font = pygame.font.SysFont("comicsans", 30)
            start_text = small_font.render("Start Game", 1, (255, 255, 255))
            quit_text = small_font.render("Quit", 1, (255, 255, 255))
            self.win.blit(start_text, (start_button_x + (button_width / 2 - start_text.get_width() / 2),
                          start_button_y + (button_height / 2 - start_text.get_height() / 2)))
            self.win.blit(quit_text, (quit_button_x + (button_width / 2 - quit_text.get_width() / 2),
                          quit_button_y + (button_height / 2 - quit_text.get_height() / 2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

    def update_score(self):
        if self.pause > 0:
            self.pause += 1
            if self.pause > self.fallSpeed * 2:
                self.end_screen()

        if self.player.score_multiplier:
            self.score = (self.speed // 10 - 3) * 2
            self.score_multiplier_timer -= 1
            if self.score_multiplier_timer <= 0:
                self.player.score_multiplier = False
        else:
            self.score = self.speed // 10 - 3

    def handle_collisions(self):
        for obstacle in self.obstacles:
            if obstacle.collide(self.player.hitbox):
                if self.player.shield:
                    self.obstacles.pop(self.obstacles.index(obstacle))
                    self.player.shield = False
                else:
                    self.player.falling = True
                    self.assets.hit_sound.play(loops=2, maxtime=500)
                    if self.pause == 0:
                        self.pause = 1
                        self.fallSpeed = self.speed
            if obstacle.x < -64:
                self.obstacles.pop(self.obstacles.index(obstacle))
            else:
                obstacle.x -= 1.4

        for powerup in self.powerups:
            if powerup.collide(self.player.hitbox):
                self.assets.powerup_sound.play()
                if isinstance(powerup, Shield):
                    self.player.shield = True
                elif isinstance(powerup, ScoreMultiplier):
                    self.player.score_multiplier = True
                    self.score_multiplier_timer = 300
                self.powerups.pop(self.powerups.index(powerup))
            if powerup.x < -64:
                self.powerups.pop(self.powerups.index(powerup))
            else:
                powerup.x -= 1.4

    def move_background(self):
        self.bgX -= 1.4
        self.bgX2 -= 1.4
        if self.bgX < self.assets.bg.get_width() * -1:
            self.bgX = self.assets.bg.get_width()
        if self.bgX2 < self.assets.bg.get_width() * -1:
            self.bgX2 = self.assets.bg.get_width()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == USEREVENT + 1:
                self.speed += 1
            if event.type == USEREVENT + 2:
                self.create_obstacle()
            if event.type == USEREVENT + 3:
                self.create_powerup()
        return True

    def create_powerup(self):
        r = random.randrange(0, 2)
        if r == 0:
            self.powerups.append(Shield(810, 280, 32, 32, self.assets))
        else:
            self.powerups.append(ScoreMultiplier(
                810, 280, 32, 32, self.assets))

    def create_obstacle(self):
        r = random.randrange(0, 4)
        if r == 0:
            self.obstacles.append(Saw(810, 310, 64, 64, self.assets))
        elif r == 1:
            self.obstacles.append(Spike(810, 0, 48, 310, self.assets))
        elif r == 2:
            self.obstacles.append(Bird(810, 250, 32, 32, self.assets))
        else:
            self.obstacles.append(GroundEnemy(810, 313, 32, 32, self.assets))

    def handle_input(self):
        if not self.player.falling:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not self.player.jumping:
                    self.player.start_jump()
            elif keys[pygame.K_DOWN]:
                if not (self.player.sliding):
                    self.player.sliding = True
            if keys[pygame.K_p]:
                self.pause_screen()

    def pause_screen(self):
        run = True
        while run:
            self.win.blit(self.assets.bg, (0, 0))
            large_font = pygame.font.SysFont("comicsans", 80)
            title = large_font.render("Paused", 1, (255, 255, 255))
            self.win.blit(title, (self.W / 2 - title.get_width() / 2, 150))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            button_width = 200
            button_height = 50
            resume_button_x = self.W / 2 - button_width / 2
            resume_button_y = 250
            quit_button_x = self.W / 2 - button_width / 2
            quit_button_y = 320

            if resume_button_x + button_width > mouse[0] > resume_button_x and resume_button_y + button_height > mouse[1] > resume_button_y:
                pygame.draw.rect(self.win, (0, 255, 0), (resume_button_x,
                                 resume_button_y, button_width, button_height))
                if click[0] == 1:
                    run = False
            else:
                pygame.draw.rect(self.win, (0, 200, 0), (resume_button_x,
                                 resume_button_y, button_width, button_height))

            if quit_button_x + button_width > mouse[0] > quit_button_x and quit_button_y + button_height > mouse[1] > quit_button_y:
                pygame.draw.rect(self.win, (255, 0, 0), (quit_button_x,
                                 quit_button_y, button_width, button_height))
                if click[0] == 1:
                    pygame.quit()
                    exit()
            else:
                pygame.draw.rect(self.win, (200, 0, 0), (quit_button_x,
                                 quit_button_y, button_width, button_height))

            small_font = pygame.font.SysFont("comicsans", 30)
            resume_text = small_font.render("Resume", 1, (255, 255, 255))
            quit_text = small_font.render("Quit", 1, (255, 255, 255))
            self.win.blit(resume_text, (resume_button_x + (button_width / 2 - resume_text.get_width() / 2),
                          resume_button_y + (button_height / 2 - resume_text.get_height() / 2)))
            self.win.blit(quit_text, (quit_button_x + (button_width / 2 - quit_text.get_width() / 2),
                          quit_button_y + (button_height / 2 - quit_text.get_height() / 2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

    def redraw_window(self):
        self.win.blit(self.assets.bg, (self.bgX, 0))
        self.win.blit(self.assets.bg, (self.bgX2, 0))
        text = self.font.render(
            "Score: " + str(self.score), 1, (255, 255, 255))
        self.player.draw(self.win)
        for obstacle in self.obstacles:
            obstacle.draw(self.win)
        for powerup in self.powerups:
            powerup.draw(self.win)

        if self.player.shield:
            self.win.blit(self.assets.shield, (650, 10))

        if self.player.score_multiplier:
            self.win.blit(self.assets.score_multiplier, (600, 10))

        self.win.blit(text, (700, 10))
        pygame.display.update()

    def end_screen(self):
        self.pause = 0
        self.speed = 30
        self.obstacles = []
        self.player.reset()
        run = True
        while run:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False
            self.win.blit(self.assets.bg, (0, 0))
            large_font = pygame.font.SysFont("comicsans", 80)
            last_score = large_font.render(
                "Best Score: " + str(self.update_file()), 1, (255, 255, 255))
            current_score = large_font.render(
                "Score: " + str(self.score), 1, (255, 255, 255))
            self.win.blit(last_score, (self.W / 2 -
                          last_score.get_width() / 2, 150))
            self.win.blit(current_score, (self.W / 2 -
                          current_score.get_width() / 2, 240))
            pygame.display.update()
        self.score = 0

    def update_file(self):
        try:
            with open("scores.txt", "r") as f:
                last = int(f.read())
        except (FileNotFoundError, ValueError):
            last = 0
        if last < self.score:
            with open("scores.txt", "w") as f:
                f.write(str(self.score))
            return self.score
        return last
