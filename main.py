import pygame
from game import *

pygame.init()
resolution = (1920, 1080)
window = pygame.display.set_mode((1920, 1080))


def level():
    run = True
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
    while run:
        clock += pygame.time.Clock().tick(60)/1000      # max 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        player.tick(keys, beams)

        background.tick(player)

        if back_button.tick():
            main()

        background.draw(window)
        back_button.draw(window)

        player.draw(window,background.width)
        for beam in beams:
            beam.draw(window, background.cord_x)

        pygame.display.update()

def main():
    clock = 0
    run = True
    background = pygame.image.load("Background/Menu.jpg")
    start_button = Button(860,300, "Buttons/start ")
    back_button = Button(860,500, "Buttons/back ")

    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # max 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if start_button.tick():
            level()

        if back_button.tick():
            exit()

        window.blit(background, (0, 0))
        start_button.draw(window)
        back_button.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main()