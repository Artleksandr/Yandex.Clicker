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
    location = 1
    kills = 0
    balance = 0
    damage = 1
    size = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Кликер говна')
    e = pygame.sprite.Group()
    bg = pygame.sprite.Group()
    enemy = pygame.sprite.Sprite(e)
    enemy.image = load_image(random.choice(("gopnick1.png", "gopnick2.png")))
    enemy.rect = enemy.image.get_rect()
    background = pygame.sprite.Sprite(bg)
    background.image = load_image("location{}.png".format(location))
    background.rect = background.image.get_rect()
    enemy.rect.topleft = random.choice(((150, 230), (300, 225)))

    running = True
    while running:
        bg.draw(screen)
        font = pygame.font.SysFont('Helvetica', 48)
        text_surface = font.render(str(kills), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and\
                    enemy.rect.collidepoint(pygame.mouse.get_pos()):
                enemy.rect.topleft = random.choice(((150, 230), (300, 225)))
                kills += 1
                enemy.image = load_image(random.choice(("gopnick1.png", "gopnick2.png")))
        e.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
