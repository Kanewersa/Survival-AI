import pygame

from survival.game_map import GameMap

window_width = 1280
window_height = 720


def draw_game(delta):
    game_map.draw(delta, win)
    pygame.display.update()


def update_game(delta, pressed_keys):
    game_map.update(delta, pressed_keys)
    pass


if __name__ == '__main__':
    pygame.init()

    win = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("AI Project")

    clock = pygame.time.Clock()

    game_map = GameMap(int(window_width/32), int(window_height/32) + 1)

    run = True

    while run:
        # Set the framerate
        ms = clock.tick(60)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        draw_game(ms)
        update_game(ms, keys)
