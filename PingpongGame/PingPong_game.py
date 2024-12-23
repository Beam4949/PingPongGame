from pygame import *
import time as timer
from random import randint, choice
window_width = int(750)
window_height = int(500)
window = display.set_mode((window_width, window_height))
display.set_caption('A space game')

bg = transform.scale(image.load('galaxy.jpg'), (window_width, window_height))

class Character(sprite.Sprite):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed, hp):
        sprite.Sprite.__init__(self)
        self.hp = hp
        self.filename = filename
        self.image = transform.scale(image.load(filename), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def draw(self):
        #draw.rect(window, (255, 0, 0), self.rect)
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Ball(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed_x, speed_y):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, 0, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):  # player1.hp -= 1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y >= window_height - 50:
            self.speed_y *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1
        if self.rect.x <= -50:
            self.rect.x = window_width/2 - 25
            self.rect.y = window_height/2 - 25
            player1.hp -= 1
        if self.rect.x >= window_width:
            self.rect.x = window_width/2 - 25
            self.rect.y = window_height/2 - 25
            player2.hp -= 1

class Bullet(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed, damage):
        self.damage = damage
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed, 0)
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= -50 and self.rect.x >= window_width:
            self.kill()

class Enemy(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed, hp):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed, hp)
        self.shoottime = timer.time()
        self.Boss = False
        self.BombBoss = False
        self.isCreateBomb = True
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 650:
            player1.hp -= 1
            self.rect.y = 0
            self.rect.x = randint(0, 425)

class Power(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.bg_image = Surface((size_x, size_y))
        self.bg_image.fill((255, 0, 0))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = pos_x
        self.bg_rect.y = pos_y

        self.value = 1
        self.max_value = 500
        self.max_width = size_x - 8
        self.max_height = size_y - 8
        self.gauge = int(self.value / self.max_value * (size_x - 6))
        self.value_image = Surface((self.gauge, size_y - 6))
        self.value_image.fill((255, 255, 0))
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = pos_x + 3
        self.value_rect.y = pos_y + 3

        self.lastUpdateTime = timer.time()
    def updateValue(self):
        a = 1
        if timer.time() - self.lastUpdateTime >= 0.01 and self.value <= self.max_value:
            self.value += a
            self.gauge = int(self.value / self.max_value * self.max_width)
            self.value_image = Surface((self.gauge, self.max_height))
            self.value_image.fill((255, 255, 0))
            self.lastUpdateTime = timer.time()

    def draw(self):
        self.updateValue()
        window.blit(self.bg_image, (self.bg_rect.x, self.bg_rect.y))
        window.blit(self.value_image, (self.value_rect.x, self.value_rect.y))

class Bar(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.bar_image = Surface((size_x, size_y))
        self.bar_image.fill((100, 255, 100))
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.x = pos_x
        self.bar_rect.y = pos_y

    def draw(self):
        window.blit(self.bar_image, (self.bar_rect.x, self.bar_rect.y))

player1 = Character('blue_lightsaber.png', 40, 100, 10, window_height/2 - 50, 3, 999)
player1_power = Power(200, 20, 13, 50)
player1_bar1 = Bar(2, 25, 28, 50)
player1_bar2 = Bar(2, 25, 52, 50)
player1_bar3 = Bar(2, 25, 208, 50)
player2 = Character('red_lightsaber.png', 40, 100, window_width - 45, window_height/2 - 50, 3, 999)
player2_power = Power(200, 20, 530, 50)
player2_bar1 = Bar(2, 25, 548, 50)
player2_bar2 = Bar(2, 25, 572, 50)
player2_bar3 = Bar(2, 25, 725, 50)
ball = Ball('bomb.png', 50, 50, window_width/2 - 25, window_height/2 - 25, -2, 2)
damage_small = 1
damage_medium = 3
damage_super = 10
bullet_speed_small = 3
bullet_speed_medium = 5
bullet_speed_super = 10

bullet_group = sprite.Group()
enemy_group = sprite.Group()
enemy_bullet_group = sprite.Group()
# treasure = Character('treasure.png', 50, 50, 700, 400, 0)

font.init()
text = font.Font(None, 45)
small_text = font.Font(None, 20)
# mixer.init()
# mixer.music.load('jungles.ogg')
#mixer.music.play()

clock = time.Clock()
fps = 60
game = True
finish = False
isWin_1 = False
isWin_2 = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    clock.tick(fps)
    display.update()
    window.blit(bg, (0, 0))
    # treasure.draw()
    
    hp_box_1 = text.render('Player 1 hp:' + str(player1.hp), True, (70, 70, 255))
    window.blit(hp_box_1, (10, 10))
    hp_box_2 = text.render('Player 2 hp:' + str(player2.hp), True, (255, 70, 70))
    window.blit(hp_box_2, (window_width - 220, 10))
    power_box_1 = text.render('Power:' + str(player1_power.value), True, (150, 150, 255))
    window.blit(power_box_1, (10, 80))
    power_box_2 = text.render('Power:' + str(player2_power.value), True, (255, 150, 70))
    window.blit(power_box_2, (window_width - 220, 80))
    
    if finish == False:
        player1.draw()
        player1_power.draw()
        player1_bar1.draw()
        player1_bar2.draw()
        player1_bar3.draw()
        player2.draw()
        player2_power.draw()
        player2_bar1.draw()
        player2_bar2.draw()
        player2_bar3.draw()
        ball.draw()
        ball.update()
        # for enemy in enemy_group:

        bullet_group.draw(window)
        bullet_group.update()
        # enemy_bullet_group.draw(window)
        # enemy_bullet_group.update()
        # enemy_group.draw(window)
        # enemy_group.update()

        # for enemy in enemy_list:
        #     enemy.move()
        #     enemy.draw()
        # charge power 10 pps

        keys = key.get_pressed()
        if (keys[K_w] and player1.rect.y > 0):
            player1.rect.y -= player1.speed
        if (keys[K_s] and player1.rect.y < window_height - player1.size_y):
            player1.rect.y += player1.speed
        if (keys[K_UP] and player2.rect.y > 0):
            player2.rect.y -= player2.speed
        if (keys[K_DOWN] and player2.rect.y < window_height - player2.size_y):
            player2.rect.y += player2.speed

        if (keys[K_SPACE] and player1_power.value >= 40 and player1_power.value <= 100):
            bullet_group.add(Bullet('troll_bullet.png', 25, 25, player1.rect.x + 40, player1.rect.y + 20, bullet_speed_small, damage_small))
            player1_power.value = 0
        if (keys[K_SPACE] and player1_power.value > 100 and player1_power.value <= 500):
            bullet_group.add(Bullet('troll_bullet.png', 50, 50, player1.rect.x + 40, player1.rect.y + 20, bullet_speed_medium, damage_medium))
            player1_power.value = 0
        if (keys[K_SPACE] and player1_power.value > 500):
            bullet_group.add(Bullet('troll_bullet.png', 100, 100, player1.rect.x + 40, player1.rect.y, bullet_speed_super, damage_super))
            player1_power.value = 0

        if (keys[K_RETURN] and player2_power.value >= 40 and player2_power.value <= 100):
            bullet_group.add(Bullet('troll_bullet.png', 25, 25, player2.rect.x - 50, player2.rect.y + 20, bullet_speed_small*-1, damage_small))
            player2_power.value = 0
        if (keys[K_RETURN] and player2_power.value > 100 and player2_power.value <= 500):
            bullet_group.add(Bullet('troll_bullet.png', 50, 50, player2.rect.x - 50, player2.rect.y + 20, bullet_speed_medium*-1, damage_medium))
            player2_power.value = 0
        if (keys[K_RETURN] and player2_power.value > 500):
            bullet_group.add(Bullet('troll_bullet.png', 100, 100, player2.rect.x - 100, player2.rect.y, bullet_speed_super*-1, damage_super))
            player2_power.value = 0

        collided_bullet_list = sprite.spritecollide(player1, bullet_group, True)
        for bullet in collided_bullet_list:
            player1.hp -= bullet.damage

        collided_bullet_list = sprite.spritecollide(player2, bullet_group, True)
        for bullet in collided_bullet_list:
            player2.hp -= bullet.damage

        # collide_list = sprite.spritecollide(player1, enemy_bullet_group, True)
        # for collide in collide_list:
        #     player1.hp -= 1

        isCollide = sprite.collide_rect(player1, ball)
        if isCollide == True:
            ball.speed_x *= -1

        isCollide = sprite.collide_rect(player2, ball)
        if isCollide == True:
            ball.speed_x *= -1

        if player1.hp <= 0:
            isWin_2 = True
            finish = True

        if player2.hp <= 0:
            isWin_1 = True
            finish = True
            
    else:
        if isWin_1 == True:
            win_1 = text.render('Player 1 won', True, (255, 255, 0))
            window.blit(win_1, (205, 280))    
        if isWin_2 == True:
            win_2 = text.render('Player 2 won', True, (255, 255, 0))
            window.blit(win_2, (205, 280))
    

    