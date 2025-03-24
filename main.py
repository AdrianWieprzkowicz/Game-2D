from game import *

# Inicjalizacja Pygame
pygame.init()
resolution = (1920, 1080)
window = pygame.display.set_mode(resolution)

# Funkcja do wyświetlania pauzy
def display_pause(window):
    pause_image = pygame.font.Font.render(pygame.font.SysFont("", 150), "Pause", True, (0, 0, 0))
    window.blit(pause_image, (820, 300))

# Funkcja odpowiedzialna za level (poziom gry)
def level():
    run = True
    pause = False
    player = Player()
    background = Background()
    back_button = Button(1600, 50, "Buttons/back ")
    clock = 0
    beams = [
        Beam(10, 890, 3980, 10),
        Beam(1100, 740, 200, 150),
        Beam(2500, 740, 200, 150),
        Beam(1600, 540, 400, 50),
        Beam(0, 0, 10, 900),
        Beam(3990, 0, 10, 900)
    ]

    # Główna pętla poziomu
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # max 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause  # Pauzowanie gry

        keys = pygame.key.get_pressed()

        # Pauza
        if pause:
            display_pause(window)
            pygame.display.update()
            continue

        # Update gracza
        player.tick(keys, beams)
        background.tick(player)

        # Przycisk powrotu do menu
        if back_button.tick():
            main()

        # Rysowanie elementów na ekranie
        background.draw(window)
        back_button.draw(window)
        player.draw(window, background.width)
        for beam in beams:
            beam.draw(window, background.cord_x)

        pygame.display.update()

# Funkcja menu głównego
def main():
    run = True
    clock = 0
    background = pygame.image.load("Background/Menu.jpg")
    start_button = Button(860, 300, "Buttons/start ")
    back_button = Button(860, 500, "Buttons/back ")

    # Główna pętla menu
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # max 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Start gry
        if start_button.tick():
            level()

        # Powrót z gry
        if back_button.tick():
            exit()

        # Rysowanie menu
        window.blit(background, (0, 0))
        start_button.draw(window)
        back_button.draw(window)

        pygame.display.update()

if __name__ == "__main__":
    main()