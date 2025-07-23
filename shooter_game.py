from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")


window = display.set_mode((700,500))
display.set_caption("Shooter game")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


lost = 0 #количество пропущенных врагов
score = 0 #количество убитых врагов
hp = 3 #кол-во хп

font.init()

font2 = font.SysFont('Comic Sans MS', 35)
font_obj = font.SysFont('Comic Sans MS', 70)
lose_text = font_obj.render('GAME OVER!', True, (255,0,0))
win_text = font_obj.render('YOU WON', True, (101, 243, 41))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys  [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.x = randint(80,420)
            self.rect.y = 0
            lost = lost +  1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
bullets = sprite.Group()




finish = False
run = True

ship = Player('rocket.png', 5, 400, 80, 100, 7)
monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80,420), -40, 80, 50, randint(1,2))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80,420), -40, 80, 50, randint(1,2))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and finish == False:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire > 4 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if not finish:
        window.blit(background,(0,0))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка', True, (150, 0, 0))
                window.blit(reload, (250,400))
            else:
                num_fire = 0
                rel_time = False


        kabooms = sprite.groupcollide(monsters, bullets, True, True)
        for boom in kabooms:
            score += 1
            new_monster = Enemy('ufo.png', randint(80,420), -40, 80, 50, randint(1,2))
            monsters.add(new_monster)

        crushing = sprite.groupcollide(asteroids, bullets, True, True)
        for crush in crushing:
            new_asteroid = Enemy('asteroid.png', randint(80,420), -40, 80, 50, randint(1,2))
            asteroids.add(new_asteroid)
        
        if sprite.spritecollide(ship, asteroids, True):
            hp -= 1


        text_lose = font2.render("Lost: " + str(lost), True, (243, 41, 41))
        window.blit(text_lose, (10, 50))
        text_score = font2.render("Score: " + str(score), True, (101, 243, 41))
        window.blit(text_score, (10, 20))
        life_score = font2.render('HP: '+ str(hp), True, (255, 165, 0))
        window.blit(life_score, (10,90))



        if sprite.spritecollide(ship, monsters, False) or hp < 1:
            window.blit(lose_text, (200, 200))
            finish = True
        if score > 9:
            window.blit(win_text, (200, 200))
            finish = True

    display.update()
    time.delay(10)






