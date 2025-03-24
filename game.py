import pygame
from math import floor

# Rozdzielczość ekranu
resolution = (1920, 1080)

class Physic:
    def __init__(self, x, y, width, height, acceleration, max_speed):
        self.cord_x = x  # Początkowa współrzędna X
        self.cord_y = y  # Początkowa współrzędna Y
        self.speed_x = 0  # Prędkość w poziomie
        self.speed_y = 0  # Prędkość w pionie
        self.acceleration = acceleration  # Wartość przyspieszenia
        self.max_speed = max_speed  # Maksymalna prędkość
        self.width = width  # Szerokość obiektu
        self.height = height  # Wysokość obiektu
        self.previous_x = x  # Poprzednia współrzędna X (do sprawdzania kolizji)
        self.previous_y = y  # Poprzednia współrzędna Y (do sprawdzania kolizji)
        self.jumping = False  # Czy obiekt skacze
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)  # Obszar kolizji

    def physic_tick(self, beams):
        # Zastosowanie grawitacji: aktualizacja prędkości w pionie oraz pozycji
        self.speed_y += 1  # Symulacja grawitacji
        self.cord_x += self.speed_x  # Zmiana pozycji X
        self.cord_y += self.speed_y  # Zmiana pozycji Y
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)  # Aktualizacja hitboxu

        # Sprawdzanie kolizji z przeszkodami (belkami)
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):
                # Sprawdzenie kolizji z prawej strony
                if self.cord_x + self.width >= beam.cord_x + 1 > self.previous_x + self.width:
                    self.cord_x = self.previous_x
                    self.speed_x = 0
                # Sprawdzenie kolizji z lewej strony
                if self.cord_x <= beam.cord_x + beam.width - 1 < self.previous_x:
                    self.cord_x = self.previous_x
                    self.speed_x = 0
                # Sprawdzenie kolizji z dołu (lądowanie)
                if self.cord_y + self.height >= beam.cord_y + 1 > self.previous_y + self.height:
                    self.cord_y = self.previous_y
                    self.speed_y = 0
                    self.jumping = False  # Przestajemy skakać po lądowaniu
                # Sprawdzenie kolizji z góry
                if self.cord_y <= beam.cord_y + beam.height - 1 < self.previous_y:
                    self.cord_y = self.previous_y
                    self.speed_y = 0

        # Zapisanie poprzednich pozycji dla kolejnego sprawdzenia kolizji
        self.previous_x = self.cord_x
        self.previous_y = self.cord_y


class Button:
    def __init__(self, cord_x, cord_y, file_name):
        self.cord_x = cord_x  # Pozycja X przycisku
        self.cord_y = cord_y  # Pozycja Y przycisku
        # Załadowanie obrazków przycisku (stan normalny i naciśnięty)
        self.button_image = pygame.image.load(f"{file_name}v1.png")
        self.pressed_button_image = pygame.image.load(f"{file_name}v2.png")
        # Hitbox przycisku (obszar interakcji)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.button_image.get_width(),
                                  self.button_image.get_height())

    def tick(self):
        # Sprawdzanie, czy przycisk został kliknięty
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Jeśli lewy przycisk myszy jest wciśnięty
                return True

    def draw(self, window):
        # Rysowanie przycisku na ekranie, zmienia obrazek w zależności od stanu
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.pressed_button_image, (self.cord_x, self.cord_y))  # Obrazek naciśniętego przycisku
        else:
            window.blit(self.button_image, (self.cord_x, self.cord_y))  # Obrazek normalny


class Player(Physic):
    def __init__(self):
        # Załadowanie obrazków dla gracza (stałej pozycji, skoku, chodzenia)
        self.stand_right_img = pygame.image.load("Player/Stand.png")
        self.stand_left_img = pygame.transform.flip(pygame.image.load("Player/Stand.png"), True, False)
        width = self.stand_right_img.get_width()  # Szerokość gracza
        height = self.stand_right_img.get_height()  # Wysokość gracza
        super().__init__(100, 500, width, height, 0.5, 15)  # Wywołanie konstruktora klasy nadrzędnej
        self.jump_right_img = pygame.image.load("Player/Jump.png")
        self.jump_left_img = pygame.transform.flip(pygame.image.load("Player/Jump.png"), True, False)
        # Załadowanie obrazków do chodzenia
        self.walk_right_img = [pygame.image.load(f"Player/Walk v{x}.png") for x in range(1, 5)]
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f"Player/Walk v{x}.png"), True, False) for x in
                              range(1, 5)]
        self.walk_index = 0  # Indeks klatki animacji chodzenia
        self.direction = 1  # Kierunek (1 - prawo, 0 - lewo)

    def tick(self, keys, beams):
        # Aktualizacja fizyki postaci
        self.physic_tick(beams)

        # Ruch postaci w prawo (zwiększanie prędkości X)
        if keys[pygame.K_RIGHT] and self.speed_x < self.max_speed:
            self.speed_x += self.acceleration
        # Ruch postaci w lewo (zmniejszanie prędkości X)
        if keys[pygame.K_LEFT] and self.speed_x > -self.max_speed:
            self.speed_x -= self.acceleration
        # Skok (zmniejszanie prędkości Y)
        if keys[pygame.K_UP] and not self.jumping:
            self.speed_y -= 30
            self.jumping = True

        # Określenie kierunku poruszania się
        if self.speed_x > 0:
            self.direction = 1
        if self.speed_x < 0:
            self.direction = 0

        # Stopniowe zwalnianie, gdy nie są wciśnięte strzałki
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            if self.speed_x > 0:
                self.speed_x -= self.acceleration
            elif self.speed_x < 0:
                self.speed_x += self.acceleration

    def draw(self, window, background_width):
        # Pozycja X gracza na ekranie (centrowanie względem środka ekranu)
        if background_width - resolution[0] / 2 > self.cord_x >= resolution[0] / 2:
            x_screen = resolution[0] / 2
        elif self.cord_x >= background_width - resolution[0] / 2:
            x_screen = self.cord_x - background_width + resolution[0]
        else:
            x_screen = self.cord_x

        # Rysowanie gracza w zależności od stanu (skok, chodzenie, stania)
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
        self.cord_x = x  # Pozycja X belki
        self.cord_y = y  # Pozycja Y belki
        self.width = width  # Szerokość belki
        self.height = height  # Wysokość belki
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.width, self.height)  # Obszar kolizji belki

    def draw(self, window, background_x):
        # Rysowanie belki na ekranie
        pygame.draw.rect(window, (128, 128, 128), (self.cord_x + background_x, self.cord_y, self.width, self.height))


class Background:
    def __init__(self):
        self.cord_x = 0  # Początkowa pozycja X tła
        self.cord_y = 0  # Początkowa pozycja Y tła
        self.image = pygame.image.load("Background/Game.jpg")  # Załadowanie obrazka tła
        self.width = self.image.get_width()  # Szerokość tła

    def tick(self, player):
        # Przemieszczanie tła w zależności od ruchu gracza
        if self.width - resolution[0] / 2 > player.cord_x >= resolution[0] / 2:
            self.cord_x -= player.speed_x
        elif player.cord_x >= self.width - resolution[0] / 2:
            self.cord_x = -self.width + resolution[0]
        else:
            self.cord_x = 0

    def draw(self, window):
        # Rysowanie tła
        window.blit(self.image, (self.cord_x, self.cord_y))