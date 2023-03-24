import pygame
import sys
from value_setting import setting
# 数据
mov_l = False
mov_r = False
mov_u = False
mov_d = False
# 子弹 敌人
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
# 窗口初始化
pygame.init()
screen_image = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Plane')
# 图像初始化
ship_image = pygame.image.load('game_image/Raiden_MKII_1.png')
bullet_image = pygame.image.load('game_image/bullet.png')
alien_image = pygame.image.load('game_image/alien.png')
screen_rect = screen_image.get_rect()
ship_rect = ship_image.get_rect()
bullet_rect = bullet_image.get_rect()
ship_rect.center = screen_rect.center
#自定义事件
MYEVENT1 = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENT1, 1000)
clock = pygame.time.Clock()

# 程序循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # 移动控制
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_LEFT:
                mov_l = True
            if event.key == pygame.K_RIGHT:
                mov_r = True
            if event.key == pygame.K_UP:
                mov_u = True
            if event.key == pygame.K_DOWN:
                mov_d = True
            if event.key == pygame.K_z:
                new_bullet = pygame.sprite.Sprite()
                new_bullet.image = bullet_image
                new_bullet.rect = new_bullet.image.get_rect()
                new_bullet.rect.midbottom = ship_rect.midtop
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mov_l = False
            if event.key == pygame.K_RIGHT:
                mov_r = False
            if event.key == pygame.K_UP:
                mov_u = False
            if event.key == pygame.K_DOWN:
                mov_d = False
    if mov_l and ship_rect.left > 0:
        ship_rect.x -= setting.ship_speed
    if mov_r and ship_rect.right < screen_rect.right:
        ship_rect.x += setting.ship_speed
    if mov_u and ship_rect.top > 0:
        ship_rect.y -= setting.ship_speed
    if mov_d and ship_rect.bottom < screen_rect.bottom:
        ship_rect.y += setting.ship_speed


    # 图形绘制
    screen_image.fill(setting.black)
    screen_image.blit(ship_image, ship_rect)
    for each in bullets:
        each.rect.y -= 8
        bullets.draw(screen_image)
        if each.rect.y < 0:
            bullets.remove(each)
    pygame.display.flip()
    pygame.time.wait(10)
