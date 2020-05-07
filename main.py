import pygame
import random
import os

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption("Space Shooter by DXH")


class AIRCRAFT(object):

    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 80
        self.vel = vel
        self.images = [pygame.image.load(os.path.join(os.getcwd(), '_eships_flipped', img)) for img in os.listdir('_eships_flipped')]
        self.current_image = random.choice(self.images)
        self.trigger = False

    def display(self):
        WIN.blit(self.current_image, (self.x, self.y))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.vel

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.vel

        for event in pygame.event.get():

            if event.type == pygame.KEYUP and keys[pygame.K_SPACE]:
                self.trigger = True
                break


class METEOR(object):

    def __init__(self, x, y, velx, vely):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.images = [(pygame.image.load('_eArt/png/meteorSmall.png'), 0), (pygame.image.load('_eArt/png/meteorBig.png'), 1)]
        self.current_image = random.choice(self.images)

        self.sizemeteorSmall = (44, 42)
        self.sizemeteorBig = (136, 111)

        self.current_size = self.sizemeteorSmall if self.current_image[1] == 0 else self.sizemeteorBig

        self.current_image = self.current_image[0]

    def display(self):
        WIN.blit(self.current_image, (self.x, self.y))

        self.x += self.velx

        self.y += self.vely

        if self.y > HEIGHT or self.x > WIDTH or self.x < 0:
            self.x, self.y = random.randrange(0, WIDTH), -100


class BULLET():
    
    def __init__(self, x, y, img):

        self.images = img
        self.current_image = self.images
        self.vel = 50
        self.x = x
        self.y = y
        self.width = 9
        self.height = 33
        self.explode = False

    def shoot(self):
        WIN.blit(self.current_image, (self.x, self.y))
        self.y -= self.vel

class ENEMY(AIRCRAFT):
    
    def __init__(self, x, y, vel):
        super(ENEMY, self).__init__(x, y, vel)
        self.images = [pygame.image.load('_eArt/png/enemyShip.png'), pygame.image.load("_eArt/png/enemyUFO.png")]
        self.current_img = random.choice(self.images)
        self.color_bullet = pygame.image.load('_eArt/png/laserRed.png')
        self.bullet = BULLET(self.x + self.width // 2, self.y, self.color_bullet)
        self.current_size = (98, 50)

        self.bullet.vel = -30

    def reset(self):
        self.y = 0
        self.x = random.randrange(0, WIDTH)
        return random.choice([pygame.image.load('_eArt/png/enemyShip.png'), pygame.image.load("_eArt/png/enemyUFO.png")])

    def display(self):

        WIN.blit(self.current_image, (self.x, self.y))
        self.x += self.vel - 3
        self.y += self.vel

        if self.bullet.y < HEIGHT:
            self.bullet.shoot()
        else:
            self.bullet.x = self.x + self.width // 2
            self.bullet.y = self.y

        if self.y > HEIGHT:
            self.current_img = self.reset()

class GAME(object):

    def __init__(self):
        self.status_game = True
        self.aircraft = AIRCRAFT(random.randrange(100, 700), random.randrange(600, 700), 8)
        self.clock = pygame.time.Clock()
        self.background1 = pygame.image.load('background.png')
        self.background2 = self.background1

        self.background1_y = 0
        self.background2_y = -HEIGHT

        self.listBullet = []

        self.displayBullet = []
        self.speed = 5
        self.FPS = 30
        self.score = 0
        self.mateors = self.initMateors()

        self.enemies = self.initEnemies()
        self.pause = False

    def resetEverything(self):

        self.aircraft = AIRCRAFT(random.randrange(100, 700), random.randrange(600, 700), 8)
        self.background1_y = 0
        self.background2_y = -HEIGHT
        self.listBullet = []
        self.displayBullet = []
        self.speed = 5
        self.FPS = 30
        self.score = 0
        self.mateors = self.initMateors()
        self.pause = False
        self.enemies = self.initEnemies()

    @staticmethod
    def initEnemies():
        return [ENEMY(random.randrange(100, WIDTH), 0, 5) for _ in range(random.choice((2, 3, 5, 7)))]

    @staticmethod
    def initMateors():
        return [METEOR(random.randrange(0, WIDTH), -100, random.choice((0, -10, 10)), 10) for _ in range(random.choice((10, 50, 100)))]

    @staticmethod
    def collison(x1, y1, w1, h1, x2, y2, w2, h2):
        return x1 + w1 >= x2 and y1 + h1 >= y2 and y2 + h2 >= y1 and x2 + w2 >= x1

    @staticmethod
    def displayText(string,  x, y, size, color):
        font = pygame.font.SysFont('comicsans', size)
        text = font.render(string, 1, color)
        WIN.blit(text, (x, y))

    def gameOver(self):
        self.pause = True

        while self.pause:
            WIN.blit(self.background1, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pause = False
                    pygame.quit()
                    self.status_game = False

                if event.type == pygame.KEYDOWN:
                    self.pause = False
                    self.resetEverything()

            self.displayText("GAME OVER", WIDTH // 2 - 200, HEIGHT // 2 - 50, 100, (255, 0, 0))
            self.displayText("Press any key to continue", WIDTH // 2 - 200, HEIGHT // 2 + 150, 50, (255, 0, 0))
            self.displayText(f"Your Score: {str(self.score)}", x= WIDTH // 2 - 100, y=HEIGHT // 2 + 100, size=50, color=(255, 0, 0))
            pygame.display.update()



    def display(self):
        WIN.blit(self.background1, (0, self.background1_y))
        WIN.blit(self.background2, (0, self.background2_y))



        self.background1_y += self.speed
        self.background2_y += self.speed

        if self.background1_y > HEIGHT:
            self.background1_y = - self.background1_y

        if self.background2_y > HEIGHT:
            self.background2_y = -self.background2_y

        self.aircraft.display()

        if self.aircraft.trigger:
            self.listBullet.append((self.aircraft.x + self.aircraft.width // 2, self.aircraft.y - self.aircraft.height // 2))
            self.aircraft.trigger = False

        for enemy in self.enemies:
            enemy.display()

        for enemy in self.enemies[:]:
            for bullet in self.displayBullet[:]:
                if self.collison(bullet.x, bullet.y, bullet.width, bullet.height, enemy.x, enemy.y, *enemy.current_size):
                    bullet.explode = True
                if bullet.explode:
                    self.score += 1
                    WIN.blit(pygame.image.load('_eArt/png/laserGreenShot.png'), (bullet.x, bullet.y))
                    bullet.explode = False
                    try:
                        self.displayBullet.remove(bullet)
                        self.enemies.remove(enemy)
                    except:
                        pass

            if self.collison(enemy.bullet.x, enemy.bullet.y, enemy.bullet.width, enemy.bullet.height, self.aircraft.x, self.aircraft.y, self.aircraft.width, self.aircraft.height) \
                    or self.collison(enemy.x, enemy.y, enemy.width, enemy.height, self.aircraft.x, self.aircraft.y, self.aircraft.width, self.aircraft.height):
                self.gameOver()


        if len(self.enemies) < 1:
            self.enemies = self.initEnemies()

        for bullet in self.listBullet[:]:
            self.displayBullet.append(BULLET(*bullet, pygame.image.load("_eArt/png/laserGreen.png")))

        for mateor in self.mateors:
            mateor.display()

        for bullet in self.displayBullet[:]:
            bullet.shoot()

            if bullet.y < 0:
                try:
                    self.listBullet.pop()
                    self.displayBullet.remove(bullet)
                except:
                    pass


        self.displayText(f"Score: {str(self.score)}", x=WIDTH - 200, y=50, size=50, color=(255, 0, 0))

        for mateor in self.mateors[:]:
            for bullet in self.displayBullet[:]:
                if self.collison(bullet.x, bullet.y, bullet.width, bullet.height, mateor.x, mateor.y, *mateor.current_size):
                    bullet.explode = True

                if bullet.explode:
                    self.score += 1

                    WIN.blit(pygame.image.load('_eArt/png/laserGreenShot.png'), (bullet.x, bullet.y))

                    bullet.explode = False
                    try:
                        self.displayBullet.remove(bullet)
                        self.mateors.remove(mateor)
                    except:
                        pass

            if self.collison(self.aircraft.x, self.aircraft.y, self.aircraft.width, self.aircraft.height, mateor.x, mateor.y, *mateor.current_size):
                self.gameOver()


        if len(self.mateors) < 1:
            self.mateors = self.initMateors()

        pygame.display.flip()

    def run(self):
        while self.status_game:
            self.clock.tick(self.FPS)
            if self.FPS < 120:
                self.FPS += 0.01
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status_game = False

            self.display()


if __name__ == '__main__':
    GAME().run()