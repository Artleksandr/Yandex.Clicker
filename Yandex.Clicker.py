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
    balance = 0
    size = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Кликер говна')

    all_sprites = pygame.sprite.Group()
    bg = pygame.sprite.Group()

    enemy = pygame.sprite.Sprite(all_sprites)
    enemy.image = load_image("creature.png")
    enemy.rect = enemy.image.get_rect()
    background = pygame.sprite.Sprite(bg)
    background.image = load_image("padick.png")
    background.rect = background.image.get_rect()

    running = True
    while running:
        bg.draw(screen)
        font = pygame.font.SysFont('Helvetica', 48)
        text_surface = font.render(str(balance), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and\
                    enemy.rect.collidepoint(pygame.mouse.get_pos()):
                enemy.rect.topleft = random.randint(0, size[0] - 82), random.randint(0, size[1] - 100)
                balance += 1
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
