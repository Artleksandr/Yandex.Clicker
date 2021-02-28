import os
import pygame
import random

global vex1, vex2, hp1, hp2

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


enemytype = 0


def summon(enemy, location, kills, midbottom):
    if kills > 68 and kills % 69 == 0:
        global enemytype, hp1, hp2
        enemy.image = load_image('creature.png')
        enemy.rect = enemy.image.get_rect()
        enemy.rect.midbottom = midbottom
        enemytype = 69
        return 69
    else:
        enemytype = 0
        if location == 1:
            enemy.image = load_image(random.choice(('gopnick1.png', 'gopnick2.png')))
            enemy.rect = enemy.image.get_rect()
            enemy.rect.topleft = random.choice(((150, 230), (300, 225)))
        elif location == 2:
            enemy.image = load_image('po.png')
            enemy.rect = enemy.image.get_rect()
            enemy.rect.topleft = 465, 278
        elif location == 3:
            enemy.image = load_image(random.choice(('pendos1.png', 'pendos2.png')))
            enemy.rect = enemy.image.get_rect()
            enemy.rect.topleft = random.choice(((535, 230), (300, 225)))
        elif location == 4:
            enemy.image = load_image('snowman.png')
            enemy.rect = enemy.image.get_rect()
            enemy.rect.topleft = random.choice(((650, 200), (300, 200)))
        elif location == 5:
            evoker = random.choice([True, False, False, False])
            if evoker:
                enemytype = 1
                enemy.image = load_image('evoker.png')
                enemy.rect = enemy.image.get_rect()
                enemy.rect.topleft = 325, 150
                hp1 = hp2 = (location * 10 + kills // 10) // 2
            else:
                enemy.image = load_image('vindicator.png')
                enemy.rect = enemy.image.get_rect()
                enemy.rect.topleft = 400, 200
        else:
            enemy.image = load_image('Hootin.png')
            enemy.rect = enemy.image.get_rect()
            enemy.rect.center = 400, 325
            return 5000
        return location * 10 + kills // 10


def save_game(location, kills, crit, balance, damage):
    save = open('data/save_{}'.format(location - 1), 'w', encoding='utf8')
    save.write(str(location) + '\n' + str(kills) + '\n' + str(crit) + '\n' + str(balance) + '\n' + str(damage))
    save.close()


def main():
    global hp1, hp2, vex1, vex2
    hp1 = hp2 = 0
    location = 4
    kills = 100
    crit = 5
    balance = 0
    damage = 10
    check = 0
    vex1red = vex2red = poattacked = enemyred = 0

    size = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Яндекс.Кликер')
    e = pygame.sprite.Group()
    bg = pygame.sprite.Group()
    locker = pygame.sprite.Group()
    vexes = pygame.sprite.Group()
    vex1 = pygame.sprite.Sprite(vexes)
    vex1.image = load_image('vex1.png')
    vex1.rect = vex1.image.get_rect()
    vex1.rect.topleft = 275, 150
    vex2 = pygame.sprite.Sprite(vexes)
    vex2.image = load_image('vex2.png')
    vex2.rect = vex2.image.get_rect()
    vex2.rect.topleft = 400, 150
    enemy = pygame.sprite.Sprite(e)
    background = pygame.sprite.Sprite(bg)
    background.image = load_image('location{}.png'.format(location))
    background.rect = background.image.get_rect()

    health = summon(enemy, location, kills, None)

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
    critup = pygame.sprite.Sprite(bg)
    critup.image = load_image('critup.png')
    critup.rect = critup.image.get_rect()
    critup.rect.topleft = 0, 400

    running = True
    while running:
        bg.draw(screen)
        if kills < 100:
            locker.draw(screen)
        font_health = pygame.font.SysFont('Helvetica', 24)
        font_vexhp = pygame.font.SysFont('Helvetica', 18)
        font_kills = pygame.font.SysFont('Helvetica', 48)
        balance_surface = font_kills.render('Баланс: ' + str(balance), False, (0, 159, 0))
        kills_surface = font_kills.render('Убийств: ' + str(kills), False, (191, 0, 0))
        hp1_surface = font_vexhp.render('Здоровье: ' + str(hp1), False, (255, 255, 255))
        hp2_surface = font_vexhp.render('Здоровье: ' + str(hp2), False, (255, 255, 255))
        if location == 4:
            health_surface = font_health.render('Здоровье: ' + str(health), False, (0, 0, 0))
        elif location == 6:
            health_surface = font_health.render('Здоровье: ' + str(health), False, (0, 0, 191))
        else:
            health_surface = font_health.render('Здоровье: ' + str(health), False, (255, 255, 255))
        if balance < 250 * 2 ** (damage - 1):
            dmgup_surface = font_health.render(str(250 * 2 ** (damage - 1)), False, (191, 0, 0))
        else:
            dmgup_surface = font_health.render(str(250 * 2 ** (damage - 1)), False, (0, 159, 0))
        if balance < 250 * 2 ** (crit - 5):
            critup_surface = font_health.render(str(250 * 2 ** (crit - 5)), False, (191, 0, 0))
        else:
            critup_surface = font_health.render(str(250 * 2 ** (crit - 5)), False, (0, 159, 0))
        dmg_surface = font_health.render(str(damage), False, (0, 0, 191))
        crit_surface = font_health.render(str(crit) + '%', False, (0, 0, 191))
        if hp1 > 0:
            vex1.rect.topleft = 275, 150
            screen.blit(hp1_surface, (vex1.rect[0] + (vex1.rect.width - hp1_surface.get_rect()[2]) // 2,
                                      vex1.rect[1] - 50))
            if vex1red > 0:
                vex1red -= 1
            else:
                vex1.image = load_image('vex1.png')
        elif vex1red > 0:
            vex1red -= 1
        else:
            vex1.rect.topleft = 801, 501
        if hp2 > 0:
            vex2.rect.topleft = 400, 150
            screen.blit(hp2_surface, (vex2.rect[0] + (vex2.rect.width - hp2_surface.get_rect()[2]) // 2,
                                      vex2.rect[1] - 50))
            if vex2red > 0:
                vex2red -= 1
            else:
                vex2.image = load_image('vex2.png')
        elif vex2red > 0:
            vex2red -= 1
        else:
            vex2.rect.topleft = 801, 501
        vexes.draw(screen)
        screen.blit(dmg_surface, (dmgup.rect.topleft[0] + 6, dmgup.rect.topleft[1]))
        screen.blit(crit_surface, (critup.rect.topleft[0] + 6, critup.rect.topleft[1]))
        screen.blit(critup_surface, (critup.rect.topleft[0] + (critup.rect.width - critup_surface.get_rect()[2]) // 2,
                                     436))
        screen.blit(dmgup_surface, (dmgup.rect.topleft[0] + (dmgup.rect.width - dmgup_surface.get_rect()[2]) // 2, 96))
        screen.blit(kills_surface, (background.rect.topright[0] - 175 - len(str(kills)) * 22, 0))
        if health > 0:
            screen.blit(health_surface, (enemy.rect.topleft[0] + (enemy.rect.width - health_surface.get_rect()[2]) // 2,
                                         enemy.rect.topleft[1] - 35))
        screen.blit(balance_surface, (0, 0))
        if poattacked > 0 and location == 2 and enemytype == 0:
            poattacked -= 1
            e.draw(screen)
        elif enemyred > 0 and location == 5 and enemytype != 69:
            enemyred -= 1
            e.draw(screen)
        elif location == 2 and enemytype == 0:
            rectpossaved = enemy.rect.midbottom
            enemy.image = load_image('po.png')
            enemy.rect = enemy.image.get_rect()
            enemy.rect.midbottom = rectpossaved
        elif location == 5 and enemytype != 69:
            if enemytype == 0:
                enemy.image = load_image('vindicator.png')
            else:
                enemy.image = load_image('evoker.png')
        if health <= 0 and enemyred == 0:
            if check == 0:
                check = 1
                kills += 1
                if enemytype <= 1:
                    balance += random.randint((location - 1) * 10 + 5, location * 15)
                else:
                    balance += 690
            if hp1 <= 0 and hp2 <= 0:
                check = 0
                if location != 6:
                    health = summon(enemy, location, kills, enemy.rect.midbottom)
                else:
                    pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hp1 > 0 and (pygame.mouse.get_pos()[0] in range(vex1.rect[0], vex1.rect[0] + vex1.rect[2])) \
                        and (pygame.mouse.get_pos()[1] in range(vex1.rect[1], vex1.rect[1] + vex1.rect[3])):
                    if crit >= random.randint(1, 100):
                        hp1 -= damage * 2
                    else:
                        hp1 -= damage
                    vex1.image = load_image('vex_red1.png')
                    vex1red = 20
                    vexes.draw(screen)
                if hp2 > 0 and (pygame.mouse.get_pos()[0] in range(vex2.rect[0], vex2.rect[0] + vex2.rect[2])) \
                        and (pygame.mouse.get_pos()[1] in range(vex2.rect[1], vex2.rect[1] + vex2.rect[3])):
                    if crit >= random.randint(1, 100):
                        hp2 -= damage * 2
                    else:
                        hp2 -= damage
                    vex2.image = load_image('vex_red2.png')
                    vex2red = 20
                    vexes.draw(screen)
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    if location == 2 and enemytype == 0:
                        poattacked = 50
                        rectpossaved = enemy.rect.midbottom
                        enemy.image = load_image('po_attacked.png')
                        enemy.rect = enemy.image.get_rect()
                        enemy.rect.midbottom = rectpossaved
                    elif location == 5 and health > 0 and enemytype != 69:
                        enemyred = 20
                        if enemytype == 0:
                            enemy.image = load_image('vindicator_red.png')
                        else:
                            enemy.image = load_image('evoker_red.png')
                    if crit >= random.randint(1, 100):
                        health -= damage * 2
                    else:
                        health -= damage
                if location < 6 and nextlevel.rect.collidepoint(pygame.mouse.get_pos()) and kills >= 100:
                    hp1 = hp2 = 0
                    location += 1
                    if location == 6:
                        save_game(location, kills, crit, balance, damage)
                        bg.remove(nextlevel)
                        locker.remove(lock)
                    else:
                        save_game(location, 0, crit, balance, damage)
                    kills = 0
                    health = summon(enemy, location, kills, enemy.rect.midbottom)
                    background.image = load_image('location{}.png'.format(location))
                elif dmgup.rect.collidepoint(pygame.mouse.get_pos()) and balance >= 250 * 2 ** (damage - 1):
                    balance -= 250 * 2 ** (damage - 1)
                    damage += 1
                elif critup.rect.collidepoint(pygame.mouse.get_pos()) and balance >= 250 * 2 ** (crit - 5):
                    balance -= 250 * 2 ** (crit - 5)
                    crit += 1
        if health > 0:
            e.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
