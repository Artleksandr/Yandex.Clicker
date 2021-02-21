import os
import pygame
import random
pygame.font.init()


def load_image(name, ck=None):
    a = os.path.join('data', name)
    try:
        image = pygame.image.load(a).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if ck is not None:
        if ck == -1:
            ck = image.get_at((0, 0))
        image.set_colorkey(ck)
    else:
        image = image.convert_alpha()
    return image


def main():
    size = 400, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Кликер говна')

    all_sprites = pygame.sprite.Group()

    enemy = pygame.sprite.Sprite(all_sprites)
    enemy.image = load_image("creature.png")
    enemy.rect = enemy.image.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and\
                    enemy.rect.collidepoint(pygame.mouse.get_pos()):
                print(screen.get_at((0, 0)))
                pygame.draw.rect(screen, 'black', (enemy.rect[0], enemy.rect[1], enemy.rect[0] + enemy.rect[2],
                                                   enemy.rect[1] + enemy.rect[3]))
                enemy.rect.topleft = random.randint(0, size[0] - 82), random.randint(0, size[1] - 100)
                print('Убил')
                font = pygame.font.SysFont('Helvetica', 28)
                text_surface = font.render('Some Text', False, (255, 255, 255))
                screen.blit(text_surface, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
