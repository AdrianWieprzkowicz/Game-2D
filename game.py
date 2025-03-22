import pygame
from math import floor

resolution = (1920, 1080)

class Physic:
    def __init__(self, x, y, width,  height, acceleration, max_speed):
        self.cord_x = x  # współrzędna x
        self.cord_y = y  # współrzędna y
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.width = width  # szerokość gracza
        self.height = height  # wysokość gracza
        self.previous_x = x
        self.previous_y = y
        self.jumping = False    # czy postać skacze
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)

    def physic_tick(self, beams):
        self.speed_y += 1
        self.cord_x += self.speed_x
        self.cord_y += self.speed_y
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):
                if self.cord_x + self.width >= beam.cord_x + 1 > self.previous_x + self.width:  # sprawdza czy kolizja występuje z prawej strony postaci
                    self.cord_x = self.previous_x
                    self.speed_x = 0
                if self.cord_x <= beam.cord_x + beam.width - 1 < self.previous_x:      #sprawdza czy kolizja występuje z lewej strony postaci
                    self.cord_x = self.previous_x
                    self.speed_x = 0
                if self.cord_y + self.height >= beam.cord_y + 1 > self.previous_y + self.height:
                    self.cord_y = self.previous_y
                    self.speed_y = 0
                    self.jumping = False
                if self.cord_y <= beam.cord_x + beam.width - 1 < self.previous_y:
                    self.cord_y = self.previous_y
                    self.speed_y = 0

        self.previous_x = self.cord_x
        self.previous_y = self.cord_y

class Button:
    def __init__(self, cord_x, cord_y, file_name):
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.button_image = pygame.image.load(f"{file_name}v1.png")
        self.pressed_button_image = pygame.image.load(f"{file_name}v2.png")
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.button_image.get_width(), self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.pressed_button_image, (self.cord_x, self.cord_y))
        else:
            window.blit(self.button_image,(self.cord_x, self.cord_y))


class Player(Physic):
    def __init__(self):
        self.stand_right_img = pygame.image.load("Player/Stand.png")
        self.stand_left_img = pygame.transform.flip(pygame.image.load("Player/Stand.png"), True, False)
        width = self.stand_right_img.get_width()    # szerokość gracza
        height = self.stand_right_img.get_height()     # wysokość gracza
        super().__init__(100,500, width, height, 0.5, 15)
        self.jump_right_img = pygame.image.load("Player/Jump.png")
        self.jump_left_img = pygame.transform.flip(pygame.image.load("Player/Jump.png"), True, False)
        self.walk_right_img = [pygame.image.load(f"Player/Walk v{x}.png") for x in range(1,5)]
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f"Player/Walk v{x}.png"), True, False) for x in range(1,5)]
        self.walk_index = 0
        self.direction = 1


    def tick(self, keys, beams):     # wykonuje się raz na jedno powtórzenie pętli while
        self.physic_tick(beams)
        if keys[pygame.K_RIGHT] and self.speed_x < self.max_speed:
            self.speed_x += self.acceleration
        if keys[pygame.K_LEFT] and self.speed_x > self.max_speed * -1:
            self.speed_x -= self.acceleration
        if keys[pygame.K_UP] and self.jumping is False:
            self.speed_y -= 30
            self.jumping = True
        if self.speed_x > 0:
            self.direction = 1
        if self.speed_x < 0:
            self.direction = 0
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            if self.speed_x > 0:
                self.speed_x -= self.acceleration
            elif self.speed_x < 0:
                self.speed_x += self.acceleration

    def draw(self, window, background_width):
        if background_width - resolution[0]/2 > self.cord_x >= resolution[0]/2:
            x_screen = resolution[0]/2
        elif self.cord_x >= background_width - resolution[0]/2:
            x_screen = self.cord_x - background_width + resolution[0]
        else:
            x_screen = self.cord_x

        if self.jumping:
            if self.direction == 1:
                window.blit(self.jump_right_img, (x_screen, self.cord_y))
            elif self.direction == 0:
                window.blit(self.jump_left_img, (x_screen, self.cord_y))
        elif self.speed_x != 0:
            if self.direction == 1:
                window.blit(self.walk_right_img[floor(self.walk_index)], (x_screen, self.cord_y))
            if self.direction == 0:
                window.blit(self.walk_left_img[floor(self.walk_index)], (x_screen, self.cord_y))
            self.walk_index += 0.2
            if self.walk_index > 4:
                self.walk_index = 0
        else:
            if self.direction == 1:
                window.blit(self.stand_right_img, (x_screen, self.cord_y))
            if self.direction == 0:
                window.blit(self.stand_left_img, (x_screen, self.cord_y))

class Beam:
    def __init__(self, x, y, width, height):
        self.cord_x = x
        self.cord_y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)

    def draw(self, window, bacground_x):
        pygame.draw.rect(window, (128, 128, 128), (self.cord_x + bacground_x, self.cord_y, self.width, self.height))

class Background:
    def __init__(self):
        self.cord_x = 0
        self.cord_y = 0
        self.image = pygame.image.load("Background/Game.jpg")
        self.width = self.image.get_width()

    def tick(self, player):
        if self.width - resolution[0]/2 > player.cord_x >= resolution[0]/2:
            self.cord_x -= player.speed_x
        elif player.cord_x >= self.width - resolution[0]/2:
            self.cord_x = - self.width + resolution[0]
        else:
            self.cord_x = 0

    def draw(self, window):
        window.blit(self.image, (self.cord_x, self.cord_y))