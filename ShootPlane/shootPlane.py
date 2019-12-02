# import module
import pygame
import random
from os import path

######################################## Basic parameter configuration #################################

# get the paths of picture library and sound library
img = path.join(path.dirname(__file__), "assets")
sound = path.join(path.dirname(__file__), "sounds")

# define the size of the game window, the player's health bar, and the speed of the game
width = 500
height = 600
barLength = 100
barHeight = 10
fps = 30

# define RGB parameters for white, black, red, green, blue, and yellow
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# initialize the pygame module and sound effects, create a game window
# name the game window, and create a track time object
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooting Plane")
pygame.mixer.init()
clock = pygame.time.Clock()

######################################## Load Picture #################################

# load the background image in the game while shooting the meteorites
background = pygame.image.load(path.join(img, "starfield.png")).convert()
background = pygame.transform.scale(background, (width, height), screen)

# load the image of the plane
plane = pygame.image.load(path.join(img, "player.png"))

# load the images of the meteorites
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png',
    'meteorBrown_med1.png',
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]
for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img, image)))

# load the images of explosion for meteorites and plane
explosion = {}
explosion["large"] = []
explosion["small"] = []
explosion["player"] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img_explo = pygame.image.load(path.join(img, filename)).convert()
    img_explo.set_colorkey(black)

    img_large = pygame.transform.scale(img_explo, (75, 75))
    explosion['large'].append(img_large)

    img_small = pygame.transform.scale(img_explo, (32, 32))
    explosion["small"].append(img_small)

    filename = 'sonicExplosion0{}.png'.format(i)
    img_player = pygame.image.load(path.join(img, filename)).convert()
    img_player.set_colorkey(black)
    explosion["player"].append(img_player)

######################################## Load Sound #################################

# load missile launch sounds
shootingSound = pygame.mixer.Sound(path.join(sound, "pew.wav"))

# load meteorites explosion sound
exploSound = []
for sounds in ['expl3.wav', 'expl6.wav']:
    exploSound.append(pygame.mixer.Sound(path.join(sound, sounds)))

# load plane explosion sound
player_die_sound = pygame.mixer.Sound(path.join(sound, 'rumble1.ogg'))

####################################### Function #######################################


# set text property function
# define text parameters:
# surf: screen
# text: the content you want to write on the screen
# size: font size
# x, y: the position of text
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font("arial"), size)
    text_surf = font.render(text, True, white)
    text_area = text_surf.get_rect()
    text_area.midtop = (x, y)
    surf.blit(text_surf, text_area)


# Game initial interface and ready to start interface functions
def start():
    global screen
    # load the initial interface background image of the game
    main_picture = pygame.image.load(path.join(img, "main.png")).convert()
    main_picture = pygame.transform.scale(main_picture, (width, height), screen)
    screen.blit(main_picture, (0, 0))
    # load the background music of the game's initial interface
    pygame.mixer.music.load(path.join(sound, "menu.ogg"))
    # loop
    pygame.mixer.music.play(-1)
    # detect player action events
    while True:
        pygame.display.update()
        draw_text(screen, "Press [ENTER] To Begin", 30, width / 2, height / 2)
        draw_text(screen, "or [Q] To Quit", 30, width / 2, (height / 2) + 40)
        draw_text(screen, "[A] LEFT  [S] DOWN  [D] RIGHT  [W] UP", 30, width/2, (height / 2) + 80)
        draw_text(screen, "[Space] Fire", 30, width/2, (height / 2) + 120)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Enter the next page")
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                quit()
    # load the ready sound
    ready = pygame.mixer.Sound(path.join(sound, "getready.ogg"))
    ready.play()
    # load the background and text for the ready interface
    screen.fill(black)
    draw_text(screen, "GET READY!", 40, width/2, height/2)
    while True:
        pygame.display.update()
        event = pygame.event.poll()
        pygame.time.wait(2000)
        break
    pygame.mixer.music.stop()


# set the player health bar property function
# define living bar parameters:
# surf: screen
# x, y: the position of the living bar
# pct: the volume of the living bar
def draw_living_bar(surf, x, y, pct):
    pct = max(pct, 0)
    fill = (pct / 100) * barLength
    bar_outline = pygame.Rect(x, y, barLength, barHeight)
    bar_area = pygame.Rect(x, y, fill, barHeight)
    pygame.draw.rect(surf, white, bar_outline, 3)
    pygame.draw.rect(surf, green, bar_area)


# set player life property function
# define the lives parameters:
# surf: screen
# x, y: the position of lives
# image: the image of plane
def draw_lives(surf, x, y, lives, image):
    plane_img = image.convert()
    plane_img = pygame.transform.scale(plane_img, (20, 20))
    plane_img.set_colorkey(black)
    for i in range(lives):
        plane_rect = plane_img.get_rect()
        plane_rect.x = x + 30 * i
        plane_rect.y = y
        surf.blit(plane_img, plane_rect)


# set player function
# define the player parameters:
# surf: screen
# image: the image of plane
# center, bottom: set the position of the plane
def draw_player(surf, image, center, bottom):
    player_img = pygame.transform.scale(image.convert(), (40, 30))
    player_img.set_colorkey(white)
    player_rect = player_img.get_rect()
    player_rect.centerx = center
    player_rect.y = bottom
    surf.blit(player_img, player_rect)


# after the game over, the animation where background scrolls down
def game_over(score, length=-936):
    global screen
    while True:
            screen.blit(background, (0, length))
            length += 2
            if length >= -168:
                length = -936

            draw_text(screen, "Game Over", 50, width / 2, (height / 2) - 40)
            draw_text(screen, "Score: "+str(score), 50, width / 2, height / 2)
            draw_text(screen, "Press [ESC] To Quit", 30, width / 2, (height / 2)+40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            pygame.display.update()

####################################### Class #########################################


# create the plane class
class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img, "player.png"))
        self.image = pygame.transform.scale(self.image.convert(), (40, 30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = height - 5
        self.width = 40
        self.height = 30
        self.speed = 10
        self.lives = 3
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # time out for hide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width/2
            self.rect.bottom = height - 5
        # make the plane static in the screen by default
        # when we want to check whether there is an event to be handled
        # key_pressed will give back a list of keys which happen to be pressed down at that moment
        # Direction control: A control left, D control right, W control up, S control down
        # A + W control upper left, A + S control lower left, D + W control upper right, D + S control lower right
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            if self.rect.top >= self.speed + 30:
                self.rect.top -= self.speed
            else:
                self.rect.top = 30
        if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            if self.rect.bottom <= height - 5 - self.speed:
                self.rect.bottom += self.speed
            else:
                self.rect.bottom = height - 5
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            if self.rect.left >= self.speed:
                self.rect.left -= self.speed
            else:
                self.rect.left = 0
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            if self.rect.right <= width - self.speed:
                self.rect.right += self.speed
            else:
                self.rect.right = width
        # shoot bullets by holding space bar
        if key_pressed[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        # use the shoot_delay to set the interval between bullets
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # tell the bullets where to spawn
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shootingSound.play()

    # after the plane is destroyed, it will hide for some time
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width/2, height + 100)


# create the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img, "laserRed16.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        # place the bullet according to the position of the plane
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        # spawn in front of the plane
        self.rect.y += self.speedy
        # if the bullet are out of the boundary, kill the sprite
        if self.rect.bottom < 0:
            self.kill()


# create the lava class
class Lava(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images).convert()
        self.image_original.set_colorkey(black)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        # randomize the speed of meteorites
        self.speedy = random.randint(5, 20)
        self.speedx = random.randint(-3, 3)
        # the rotated speed of the meteorites
        self.rotation = 0
        self.rotation_speed = random.randint(-10, 10)
        # time when the rotation happens
        self.last_update = pygame.time.get_ticks()
        self.delay = 50
        self.radius = int(self.rect.width*.90/2)

    # add the rotation effect to meteorites
    def rotate(self):
        now = pygame.time.get_ticks()
        # use the delay to set the interval of rotation changes
        if now - self.last_update > self.delay:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # if the meteorite are out of the boundary, reset position of the meteorite
        if self.rect.top > height or self.rect.left > width or self.rect.right < 0:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speedy = random.randint(5, 20)
            self.speedx = random.randint(-3, 3)


# create the explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.delay = 75

    def update(self):
        now = pygame.time.get_ticks()
        # use delay to set the intervals between occurrence of the explosion images
        # which can make the explosion animation Smoother
        if now - self.last_update > self.delay:
            self.last_update = now
            self.frame += 1
            # if we have gone through all explosion images, kill the sprite
            if self.frame == len(explosion[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

######################################## Game Entry Function ###############################################


def run():
    start()
    # play the music which means the start of the game
    pygame.mixer.music.load(path.join(sound, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
    # play the sound in an endless loop
    pygame.mixer.music.play(-1)
    # group all the sprites together for ease to update
    myPlane = Plane()
    all_sprites.add(myPlane)

    score = 0
    # draw scores on the screen
    draw_text(screen, str(score), 30, width/2, 10)
    # draw the living bar on the screen
    draw_living_bar(screen, 5, 5, 100)
    # draw the lives on the screen
    draw_lives(screen, width-30*3, 5, 3, plane)
    # draw the plane on the screen
    draw_player(screen, plane, width/2, height-35)

    # add the lava into the group
    for i in range(8):
        lava_element = Lava()
        all_sprites.add(lava_element)
        lavas.add(lava_element)

    # a parameter that can let the background scroll
    temp = -936
    while True:
        # this will make the loop run at the same speed all the time
        clock.tick(fps)
        # gets all the events which have occurred until now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # update
        all_sprites.update()

        # collision detection between meteorites and bullets the plane spawns
        hits = pygame.sprite.groupcollide(lavas, bullets, True, True)
        for hit in hits:
            # if the bullet hits, the score will increase
            score += 70 - hit.radius
            random.choice(exploSound).play()
            # then meteorites will explore
            expl = Explosion(hit.rect.center, "large")
            all_sprites.add(expl)
            lava_element = Lava()
            all_sprites.add(lava_element)
            lavas.add(lava_element)

        # collision detection between meteorites and the plane
        hits = pygame.sprite.spritecollide(myPlane, lavas, True, pygame.sprite.collide_circle)
        for hit in hits:
            # if the meteorites hit the plane, the shield will reduce
            myPlane.shield -= hit.radius*2
            # if the meteorites hit the plane, the meteorites will explore
            expl = Explosion(hit.rect.center, "small")
            all_sprites.add(expl)
            lava_element = Lava()
            all_sprites.add(lava_element)
            lavas.add(lava_element)
            # if the shield is 0, the lives will minus 1 and reset the shield
            # the plane will explore
            if myPlane.shield <= 0:
                player_die_sound.play()
                planeDeath = Explosion(myPlane.rect.center, "player")
                all_sprites.add(planeDeath)
                myPlane.hide()
                myPlane.lives -= 1
                myPlane.shield = 100

        # if the plane died and its live is 0, we will end the game
        if myPlane.lives == 0:
            game_over(score)

        # let the background scroll
        screen.fill(black)
        screen.blit(background, (0, temp))
        temp += 2
        if temp >= -168:
            temp = -936

        all_sprites.draw(screen)

        # draw the current shield of plane on the screen
        draw_living_bar(screen, 5, 5, myPlane.shield)
        # draw the current lives of plane on the screen
        draw_lives(screen, width-30*3, 5, myPlane.lives, plane)
        # draw the current score of plane on the screen
        draw_text(screen, str(score), 30, width/2, 10)

        # done after drawing everything to the screen
        pygame.display.flip()

    pygame.quit()


# Because this is a game programming, I can not add some test code to get the result which can show whether it is right
# You can run the programming and play it
# I think user experience is the best test case
if __name__ == '__main__':
    # spawn a group that can add all sprites to make update ease
    all_sprites = pygame.sprite.Group()
    # spawn a group of lava
    lavas = pygame.sprite.Group()
    # spawn a group of bullet
    bullets = pygame.sprite.Group()
    # the background image
    background = pygame.image.load(path.join(img, "starfield.png")).convert()
    # start the game
    run()
