#Создай собственный Шутер!
from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)

font.init()
font1 = font.Font(None, 36)

game = True
clock = time.Clock()
fps = 60
speed = 10
lost = 0
shooted = 0
goal = 25
max_lost = 15
finish = False
bullets = sprite.Group()
lose = font1.render(
            "YOU LOSE :(" , True, (180,0,0)
        )
win = font1.render(
            "YOU WIN! :)" , True, (255,215,0)
        )

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): 
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 10, 10, 10)
        bullets.add(bullet)
            

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 505:
            self.rect.y = 0
            self.rect.x = randint(1, 550)
            self.speed = randint(1, 5)
            lost = lost + 1
    

class Bullet(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 350, 430, 65, 65, 10)
ufos = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', randint(1, 550), 10, 50, 50, randint(1, 4))
    ufos.add(ufo)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_e:
                fire_sound.play()
                player.fire()
    if not finish:
        collides = sprite.groupcollide(ufos, bullets, True, True)
        window.blit(background,(0, 0))
        text_lost = font1.render(
            "Пропущено:" + str(lost), 1, (255, 255, 255)
        )
        text_shooted = font1.render(
            "Сбито врагов:" + str(shooted), 1, (255, 255, 255)
        )

        for c in collides:
            shooted += 1
            ufo = Enemy('ufo.png', randint(1, 550), 10, 50, 50, randint(1, 4))
            ufos.add(ufo)
        if sprite.spritecollide(player, ufos, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            display.update()
            time.delay(3000)
            game = False
        if shooted >= goal:
            finish = True
            window.blit(win, (200,200))
            display.update()
            time.delay(3000)
            game = False
        window.blit(text_lost, (10, 50))
        window.blit(text_shooted, (10, 20))
        player.update()
        player.reset()
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
        display.update()
    clock.tick(fps)