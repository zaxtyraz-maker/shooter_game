from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("sky.jpeg"),(win_width, win_height))

mixer.init()
mixer.music.load("super.ogg")
mixer.music.play()

font.init()
font1 = font.Font(None, 35)
missed = 0
score = 0

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
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet ("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            missed = missed + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    
pemain = Player("rockett.png", 5, win_height-100, 60, 80, 5)
enemies = sprite.Group()
for i in range(1,6):
    enemy = Enemy("alien.png", randint(80, win_width-80), -50, 60, 70, randint(1,2))
    enemies.add(enemy)
    
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80, win_width-80), -50, 60, 70, randint(1,2))
    asteroids.add(asteroid)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60
run = True
finish = False

num_fire = 0
reload_time = False

fire_sound = mixer.Sound('fire.ogg')
life = 5
from time import time as timer

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                pemain.fire()
    
    if not finish:
        window.blit(background,(0, 0))
        
        text_score = font1.render("Score: "+ str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        
        text_missed = font1.render("Missed: "+ str(missed), 1, (255, 255, 255))
        window.blit(text_missed, (win_width-150, 20))
        
        if life >= 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 120, 0)
        if life == 1:
            life_color = (150, 0, 0)
           
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (350, 10))

        
        pemain.reset() 
        pemain.update()
        
        enemies.draw(window)
        enemies.update()
        
        bullets.draw(window)
        bullets.update()
        
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font1.render('Wait, reload..', 1, (150, 0, 0))
                window.blit(reload_text, (240, 460))
            else:
                num_fire = 0
                reload_time = False

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy("alien.png", randint(80, win_width-80), -50, 60, 70, randint(1,2))
            enemies.add(enemy)
            
        if sprite.spritecollide(pemain, enemies, False) or sprite.spritecollide(pemain, asteroids, False):
            sprite.spritecollide(pemain, enemies, True)
            sprite.spritecollide(pemain, asteroids, True)
            life = life - 1
       
        if life == 0 or missed >= 20:
            finish = True
            font2 = font.Font(None, 100)
            lose = font2.render('YOU LOSE!', True, (180,0,0))
            window.blit(lose, (180, 200))

        if score > 20:
            finish = True
            font3 = font.Font(None, 100)
            win = font3.render("YOU WIN!", True, (180,0,0))
            window.blit(win, (180, 200))
            
        display.update()
        
    else:
        finish = False
        score = 0
        missed = 0
        life = 5
        num_fire = 0
        for peluru in bullets:
            peluru.kill()
        for musuh in enemies:
            musuh.kill()
            
        time.delay(3000)
        for i in range(1,6):
            enemy = Enemy("alien.png", randint(80, win_width-80), -50, 60, 70, randint(1,2))
            enemies.add(enemy)
    clock.tick(FPS)
    