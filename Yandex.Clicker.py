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
    health = location * 10 + kills // 10
    size = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Кликер говна')
    e = pygame.sprite.Group()
    bg = pygame.sprite.Group()
    locker = pygame.sprite.Group()
    enemy = pygame.sprite.Sprite(e)
    enemy.image = load_image(random.choice(('gopnick1.png', 'gopnick2.png')))
    enemy.rect = enemy.image.get_rect()
    background = pygame.sprite.Sprite(bg)
    background.image = load_image('location1.png'.format(location))
    background.rect = background.image.get_rect()
    enemy.rect.topleft = random.choice(((150, 230), (300, 225)))
    nextlevel = pygame.sprite.Sprite(bg)
    nextlevel.image = load_image('next.png')
    nextlevel.rect = nextlevel.image.get_rect()
    nextlevel.rect.topleft = 600, 60
    lock = pygame.sprite.Sprite(locker)
    lock.image = load_image('lock.png')
    lock.rect = 600, 60
    dmgup = pygame.sprite.Sprite(bg)
    dmgup.image = load_image('dmgup.png')
    dmgup.rect = dmgup.image.get_rect()
    dmgup.rect.topleft = 0, 60

    def summon():
        enemy.image = load_image(random.choice(("gopnick1.png", "gopnick2.png")))
        enemy.rect.topleft = random.choice(((150, 230), (300, 225)))
        return location * 10 + kills // 10
    running = True
    while running:
        bg.draw(screen)
        if kills < 100:
            locker.draw(screen)
        font_health = pygame.font.SysFont('Helvetica', 24)
        font_kills = pygame.font.SysFont('Helvetica', 48)
        balance_surface = font_kills.render('Баланс: ' + str(balance), False, (0, 159, 0))
        kills_surface = font_kills.render('Убийств: ' + str(kills), False, (191, 0, 0))
        health_surface = font_health.render('Здоровье: ' + str(health), False, (255, 255, 255))
        if balance < 250 * 2 ** (damage - 1):
            dmgup_surface = font_health.render(str(250 * 2 ** (damage - 1)), False, (191, 0, 0))
        else:
            dmgup_surface = font_health.render(str(250 * 2 ** (damage - 1)), False, (0, 159, 0))
        screen.blit(dmgup_surface, (dmgup.rect.topleft[0] + (dmgup.rect.width - dmgup_surface.get_rect()[2]) // 2, 96))
        screen.blit(kills_surface, (background.rect.topright[0] - 175 - len(str(kills)) * 22, 0))
        screen.blit(health_surface, (enemy.rect.topleft[0] + (enemy.rect.width - health_surface.get_rect()[2]) // 2,
                                     enemy.rect.topleft[1] - 35))
        screen.blit(balance_surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    if health - damage < 0:
                        health = 0
                    else:
                        health -= damage
                    if health == 0:
                        kills += 1
                        balance += random.randint((location - 1) * 10 + 5, location * 15)
                        health = summon()
                elif nextlevel.rect.collidepoint(pygame.mouse.get_pos()) and kills >= 100:
                    location += 1
                    kills = 0
                    health = summon()
                    if location == 5:
                        bg.remove(nextlevel)
                        bg.remove(lock)
                elif dmgup.rect.collidepoint(pygame.mouse.get_pos()) and balance >= 250 * 2 ** (damage - 1):
                    balance -= 250 * 2 ** (damage - 1)
                    damage += 1
        e.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
