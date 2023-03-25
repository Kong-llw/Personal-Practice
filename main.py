import pygame
import sys
import random
from value_setting import setting
# 数据
mov_lrud = [False, False, False, False]
ship_num = setting.NumOfShip
score = 0
high_score = 0
level = 1
k_point = setting.killing_point
refresh_interval = setting.alien_refresh_interval
pygame.mixer.init()
pygame.mixer.music.load('music/maou_loop_bgm_cyber33.ogg')
pygame.mixer.music.set_volume(0.5)
# 初始化单位
ship = pygame.sprite.Sprite()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
# 窗口初始化
pygame.init()
screen_image = pygame.display.set_mode(setting.ScreenSize[0])
pygame.display.set_caption('Plane')
# 图像初始化
ship.image = pygame.image.load('game_image/Raiden_MKII_1.png')
bullet_image = pygame.image.load('game_image/bullet.png')
alien_image = pygame.image.load('game_image/alien.png')
screen_rect = screen_image.get_rect()
ship.rect = ship.image.get_rect()
bullet_rect = bullet_image.get_rect()
ship.rect.midbottom = screen_rect.midbottom
    # 统计数据
        #分数
score_font = pygame.font.SysFont(None, 24)
score_image = score_font.render('Score  '+str(score), True, setting.white, setting.black)
score_rect = score_image.get_rect()
score_rect.top = 20
score_rect.left = 20
        #级别
level_font = pygame.font.SysFont(None, 24)
level_image = level_font.render('Level  '+str(level), True, setting.white, setting.black)
level_rect = level_image.get_rect()
level_rect.top = 20
level_rect.right = screen_rect.right - 20
# 自定义事件
AddAlien = pygame.USEREVENT + 1
Hasten = pygame.USEREVENT + 2
pygame.time.set_timer(AddAlien, refresh_interval)
pygame.time.set_timer(Hasten, setting.Speedup_interval)
clock = pygame.time.Clock()
# 按钮
    # 重启
button_rect = pygame.Rect(0, 0, 100, 30)
button_rect.center = screen_rect.center
text_font = pygame.font.SysFont(None, 24)
text_image = text_font.render('Restart', True, setting.white, setting.red)
text_rect = text_image.get_rect()
text_rect.center = button_rect.center
# 函数

# 重启飞船


def restart_ship():
    ship.rect.midbottom = screen_rect.midbottom
def game_restart():
    aliens.empty()
    bullets.empty()
    restart_ship()
    pygame.mixer.music.play(-1)

def shot():
    new_bullet = pygame.sprite.Sprite()
    new_bullet.image = bullet_image
    new_bullet.rect = bullet_image.get_rect()
    new_bullet.rect.midbottom = ship.rect.midtop
    bullets.add(new_bullet)

def m_detect(event,mov_lrud):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            mov_lrud[0] = True
        if event.key == pygame.K_RIGHT:
            mov_lrud[1] = True
        if event.key == pygame.K_UP:
            mov_lrud[2] = True
        if event.key == pygame.K_DOWN:
            mov_lrud[3] = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            mov_lrud[0] = False
        if event.key == pygame.K_RIGHT:
            mov_lrud[1] = False
        if event.key == pygame.K_UP:
            mov_lrud[2] = False
        if event.key == pygame.K_DOWN:
            mov_lrud[3] = False

def move(mov_lrud):
    if mov_lrud[0] and ship.rect.left > 0:
        ship.rect.x -= setting.ShipSpeed
    if mov_lrud[1] and ship.rect.right < screen_rect.right:
        ship.rect.x += setting.ShipSpeed
    if mov_lrud[2] and ship.rect.top > 0:
        ship.rect.y -= setting.ShipSpeed
    if mov_lrud[3] and ship.rect.bottom < screen_rect.bottom:
        ship.rect.y += setting.ShipSpeed

def add_alien():
    pos = random.randint(50, 750)
    new_alien = pygame.sprite.Sprite()
    new_alien.image = alien_image
    new_alien.rect = alien_image.get_rect()
    new_alien.rect.midbottom = (pos, 0)
    aliens.add(new_alien)

pygame.mixer.music.play(-1)
# 程序循环
while True:
    clock.tick(60)
    # 事件检测
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sys.exit()
        # 鼠标按键
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(m_pos):
                ship_num = setting.NumOfShip
                refresh_interval = setting.alien_refresh_interval
                pygame.time.set_timer(AddAlien, refresh_interval)
                score = 0
                level = 1
                mov_lrud = [False, False, False, False]
                game_restart()
                pygame.mouse.set_visible(False)
        # 正常循环
        if ship_num > 0:
            # 添加敌人
            if event.type == Hasten and refresh_interval > 200:
                refresh_interval -= 100
                level += 1
                pygame.time.set_timer(AddAlien, refresh_interval)
            if event.type == AddAlien:
                add_alien()
            # 移动控制
            m_detect(event, mov_lrud)
            # 射击
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                shot()
    if ship_num > 0:
        # 限制移动区域 移动
        move(mov_lrud)

        # 图形绘制
        screen_image.fill(setting.black)
        screen_image.blit(ship.image, ship.rect)

        score_image = score_font.render('Score  ' + str(score), True, setting.white, setting.black)
        screen_image.blit(score_image, score_rect)
        level_image = level_font.render('Level  ' + str(level), True, setting.white, setting.black)
        screen_image.blit(level_image, level_rect)
        # 子弹
        for each in bullets:
            each.rect.y -= setting.BulletSpeed
            if each.rect.y < 0:
                bullets.remove(each)
        bullets.draw(screen_image)
        # 敌人
        for i in aliens:
            i.rect.y += setting.AlienSpeed
            if i .rect.y > 600:
                aliens.remove(i)
        aliens.draw(screen_image)
        # 备用机
        for i in range(ship_num - 1):
            screen_image.blit(ship.image, (i*(ship.rect.width + 10), screen_rect.bottom - ship.rect.height))

        # 碰撞
        hit = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if hit:
            for i in hit.values():
                score += k_point * len(i)
        if high_score < score:
            high_score = score
        if pygame.sprite.spritecollideany(ship, aliens):
            ship_num -= 1
            if ship_num:
                mov_lrud = [False, False, False, False]
                restart_ship()
            else:
                pygame.draw.rect(screen_image, setting.red, button_rect)
                screen_image.blit(text_image, text_rect)
                pygame.mouse.set_visible(True)
                pygame.mixer.music.pause()
        pygame.display.flip()


