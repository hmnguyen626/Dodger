# Hieu Nguyen -- hmnguyen626@gmail.com
# This is a demo game I have created with the use of Pygame.
# Concept of the game is the player dodge objects by moving the human character or hiding behind objects like
# trees and rocks.  Note that the trees can be burnt by fireballs and the human stepping on the fire can also
# kill the player.  The longer the player last, the higher the score.

import pygame
import random
import scripts.SuperColor as sColor

# Variables
# Our game size
DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600
TEXTCOLOR = (255,255,255)

# FPS Rate
FPS = 30

# Default player position
playerX = (DISPLAY_WIDTH * 0.5)
playerY = (DISPLAY_HEIGHT * 0.5)

# Arrow boundary and position
arrowYBoundaryTop = (DISPLAY_HEIGHT - (DISPLAY_HEIGHT + 40))
arrowYBoundaryBottom = (DISPLAY_HEIGHT + 40)
arrowX = (DISPLAY_WIDTH * 0.5)

# Fireball boundary and position
fireballY = (DISPLAY_HEIGHT * 0.5)
fireballXBoundaryLeft = (DISPLAY_WIDTH - (DISPLAY_WIDTH + 40))
fireballXBoundaryRight = (DISPLAY_WIDTH + 40)

# Assets list
human_die_north = []
human_die_south = []
human_images_idle = []
human_images_left = []
human_images_right = []
human_images_down = []
human_images_up = []
human_images_topright = []
human_images_topleft = []
human_images_bottomright = []
human_images_bottomleft = []
arrow_images_idle = []
arrow_images_left = []
arrow_images_right = []
arrow_images_down = []
arrow_images_up = []
fireball_left = []
fireball_right = []
fireball_die = []
coin_spin = []
terrain_objects = []
flame = []

# Player speed
PSPEED = 3

# Max object counts
arrow_counter = 0
arrow_limit = 2
fireball_counter = 0
fireball_limit = 1
coin_counter = 0
coin_limit = 2
terrain_counter = 0
terrain_limit = 15

# Init pygame modules
pygame.init()
# Initializing font
fontName = pygame.font.match_font('arial')

# Sound loading and playback
pygame.mixer.init()

# Background
background = pygame.image.load("imgs/background/background.png")
collect_coin = pygame.mixer.Sound('sound/Mario Coin.wav')

# Setting up environment
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Dodger!")
clock = pygame.time.Clock()

# Game condition
alive = True

# Starting variable
game_over = True

# Font size
font = pygame.font.Font(None, 48)

# Sprite Groups
player_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
terrain_objects_group = pygame.sprite.Group()


# Method to load image
def load_image(name):
    image = pygame.image.load(name)
    return image


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_game_texts(surf, text, fontSize, x, y):
    font = pygame.font.Font(fontName, fontSize)
    textSurf = font.render(text, True, sColor.Color.Black)
    textRect = textSurf.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurf, textRect)


# Method to load all our assets
def load_assets():
    # ARROW --------------------------------
    # Loading images into list -- according to direction
    arrow_images_idle.append(load_image('imgs/arrow/arrow_down_0.png'))
    arrow_images_left.append(load_image('imgs/arrow/arrow_left_0.png'))
    arrow_images_left.append(load_image('imgs/arrow/arrow_left_1.png'))
    arrow_images_left.append(load_image('imgs/arrow/arrow_left_2.png'))
    arrow_images_left.append(load_image('imgs/arrow/arrow_left_3.png'))
    arrow_images_right.append(load_image('imgs/arrow/arrow_right_0.png'))
    arrow_images_right.append(load_image('imgs/arrow/arrow_right_1.png'))
    arrow_images_right.append(load_image('imgs/arrow/arrow_right_2.png'))
    arrow_images_right.append(load_image('imgs/arrow/arrow_right_3.png'))
    arrow_images_down.append(load_image('imgs/arrow/arrow_down_0.png'))
    arrow_images_down.append(load_image('imgs/arrow/arrow_down_1.png'))
    arrow_images_down.append(load_image('imgs/arrow/arrow_down_2.png'))
    arrow_images_down.append(load_image('imgs/arrow/arrow_down_3.png'))
    arrow_images_up.append(load_image('imgs/arrow/arrow_up_0.png'))
    arrow_images_up.append(load_image('imgs/arrow/arrow_up_1.png'))
    arrow_images_up.append(load_image('imgs/arrow/arrow_up_2.png'))
    arrow_images_up.append(load_image('imgs/arrow/arrow_up_3.png'))

    # HUMAN --------------------------------
    # Loading images into list -- according to direction
    human_images_idle.append(load_image('imgs/human/man_idle_0.png'))
    human_images_left.append(load_image('imgs/human/man_move_left_0.png'))
    human_images_left.append(load_image('imgs/human/man_move_left_1.png'))
    human_images_left.append(load_image('imgs/human/man_move_left_2.png'))
    human_images_left.append(load_image('imgs/human/man_move_left_3.png'))
    human_images_left.append(load_image('imgs/human/man_move_left_4.png'))
    human_images_right.append(load_image('imgs/human/man_move_right_0.png'))
    human_images_right.append(load_image('imgs/human/man_move_right_1.png'))
    human_images_right.append(load_image('imgs/human/man_move_right_2.png'))
    human_images_right.append(load_image('imgs/human/man_move_right_3.png'))
    human_images_right.append(load_image('imgs/human/man_move_right_4.png'))
    human_images_down.append(load_image('imgs/human/man_move_down_0.png'))
    human_images_down.append(load_image('imgs/human/man_move_down_1.png'))
    human_images_down.append(load_image('imgs/human/man_move_down_2.png'))
    human_images_down.append(load_image('imgs/human/man_move_down_3.png'))
    human_images_down.append(load_image('imgs/human/man_move_down_4.png'))
    human_images_up.append(load_image('imgs/human/man_move_up_0.png'))
    human_images_up.append(load_image('imgs/human/man_move_up_1.png'))
    human_images_up.append(load_image('imgs/human/man_move_up_2.png'))
    human_images_up.append(load_image('imgs/human/man_move_up_3.png'))
    human_images_up.append(load_image('imgs/human/man_move_up_4.png'))
    human_images_topright.append(load_image('imgs/human/man_move_topright_0.png'))
    human_images_topright.append(load_image('imgs/human/man_move_topright_1.png'))
    human_images_topright.append(load_image('imgs/human/man_move_topright_2.png'))
    human_images_topright.append(load_image('imgs/human/man_move_topright_3.png'))
    human_images_topright.append(load_image('imgs/human/man_move_topright_4.png'))
    human_images_topleft.append(load_image('imgs/human/man_move_topleft_0.png'))
    human_images_topleft.append(load_image('imgs/human/man_move_topleft_1.png'))
    human_images_topleft.append(load_image('imgs/human/man_move_topleft_2.png'))
    human_images_topleft.append(load_image('imgs/human/man_move_topleft_3.png'))
    human_images_topleft.append(load_image('imgs/human/man_move_topleft_4.png'))
    human_images_bottomright.append(load_image('imgs/human/man_move_bottomright_0.png'))
    human_images_bottomright.append(load_image('imgs/human/man_move_bottomright_1.png'))
    human_images_bottomright.append(load_image('imgs/human/man_move_bottomright_2.png'))
    human_images_bottomright.append(load_image('imgs/human/man_move_bottomright_3.png'))
    human_images_bottomright.append(load_image('imgs/human/man_move_bottomright_4.png'))
    human_images_bottomleft.append(load_image('imgs/human/man_move_bottomleft_0.png'))
    human_images_bottomleft.append(load_image('imgs/human/man_move_bottomleft_1.png'))
    human_images_bottomleft.append(load_image('imgs/human/man_move_bottomleft_2.png'))
    human_images_bottomleft.append(load_image('imgs/human/man_move_bottomleft_3.png'))
    human_images_bottomleft.append(load_image('imgs/human/man_move_bottomleft_4.png'))
    human_die_north.append(load_image('imgs/human/dead_looking_north_0.png'))
    human_die_north.append(load_image('imgs/human/dead_looking_north_1.png'))
    human_die_north.append(load_image('imgs/human/dead_looking_north_2.png'))
    human_die_south.append(load_image('imgs/human/dead_looking_south_0.png'))
    human_die_south.append(load_image('imgs/human/dead_looking_south_1.png'))
    human_die_south.append(load_image('imgs/human/dead_looking_south_2.png'))

    # Fireball --------------------------------
    # Loading images into list -- according to direction and hit
    fireball_left.append(load_image('imgs/fireball/fireball_left_01.png'))
    fireball_left.append(load_image('imgs/fireball/fireball_left_02.png'))
    fireball_left.append(load_image('imgs/fireball/fireball_left_03.png'))
    fireball_left.append(load_image('imgs/fireball/fireball_left_04.png'))
    fireball_left.append(load_image('imgs/fireball/fireball_left_05.png'))
    fireball_right.append(load_image('imgs/fireball/fireball_right_01.png'))
    fireball_right.append(load_image('imgs/fireball/fireball_right_02.png'))
    fireball_right.append(load_image('imgs/fireball/fireball_right_03.png'))
    fireball_right.append(load_image('imgs/fireball/fireball_right_04.png'))
    fireball_right.append(load_image('imgs/fireball/fireball_right_05.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_01.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_02.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_03.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_04.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_05.png'))
    fireball_die.append(load_image('imgs/fireball/fireball_die_06.png'))

    # Coin --------------------------------
    # Loading images into list
    coin_spin.append(load_image('imgs/coin/coin_01.png'))
    coin_spin.append(load_image('imgs/coin/coin_02.png'))
    coin_spin.append(load_image('imgs/coin/coin_03.png'))
    coin_spin.append(load_image('imgs/coin/coin_04.png'))
    coin_spin.append(load_image('imgs/coin/coin_05.png'))
    coin_spin.append(load_image('imgs/coin/coin_06.png'))
    coin_spin.append(load_image('imgs/coin/coin_07.png'))
    coin_spin.append(load_image('imgs/coin/coin_08.png'))

    # Terrain Objects ----------------------
    # Loading images into list
    terrain_objects.append(load_image('imgs/terrain objects/bushy_tree.png'))
    # terrain_objects.append(load_image('imgs/terrain objects/many_trees.png'))
    terrain_objects.append(load_image('imgs/terrain objects/pointy_tree.png'))
    terrain_objects.append(load_image('imgs/terrain objects/rock_large.png'))
    terrain_objects.append(load_image('imgs/terrain objects/rock_wide.png'))

    # Flame ---------------------------------
    # Loading images into list
    flame.append(load_image('imgs/flame/flame_01.png'))
    flame.append(load_image('imgs/flame/flame_02.png'))
    flame.append(load_image('imgs/flame/flame_03.png'))
    flame.append(load_image('imgs/flame/flame_04.png'))
    flame.append(load_image('imgs/flame/flame_05.png'))
    flame.append(load_image('imgs/flame/flame_06.png'))
    flame.append(load_image('imgs/flame/flame_07.png'))

    # Music and sounds
    pygame.mixer.music.load('sound/background_music.ogg')


def show_gameover_screen():
    pygame.mixer.music.stop()
    screen.blit(background, (0,0))
    draw_game_texts(screen, "DODGER", 144, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 4)
    draw_game_texts(screen, "Arrow keys to move", 44, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    draw_game_texts(screen, "Press the ESC key to begin...", 25, DISPLAY_WIDTH /2 , DISPLAY_HEIGHT * 3 / 4)
    draw_game_texts(screen, "Music and image assets, credited to opengameart.org", 25, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 7 / 8)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(playerX, playerY, 25, 25)

        # Logical index and counter
        self.index = 0
        self.counter = 0
        self.counterDie = 0
        self.speedx = 0
        self.speedy = 0
        self.score = 0

        # Time to live variables
        self.time = 2
        self.start_ticks = 0

        # Our default image
        self.image = human_images_idle[self.index]

        # Alive logical
        self.alive = True

    def update(self):
        # Sets our speed back to 0, so it doesnt loop infinitely for movement
        self.speedx = 0
        self.speedy = 0

        key = pygame.key.get_pressed()
        # Player controls/Movement
        if self.alive:
            self.score += 1

            if key[pygame.K_LEFT]:
                # Iterate through our image list, and update our movement
                self.image = human_images_left[self.counter]
                self.counter = (self.counter + 1) % len(human_images_left)
                self.speedx = -PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedx = 7

            if key[pygame.K_RIGHT]:
                # Iterate through our image list, and update our movement
                self.image = human_images_right[self.counter]
                self.counter = (self.counter + 1) % len(human_images_right)
                self.speedx = PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedx = -7

            if key[pygame.K_UP]:
                # Iterate through our image list, and update our movement
                self.image = human_images_up[self.counter]
                self.counter = (self.counter + 1) % len(human_images_up)
                self.speedy = -PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = 7

            if key[pygame.K_DOWN]:
                # Iterate through our image list, and update our movement
                self.image = human_images_down[self.counter]
                self.counter = (self.counter + 1) % len(human_images_down)
                self.speedy = PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = -7

            # Corner movements
            if key[pygame.K_UP] and key[pygame.K_RIGHT]:
                self.image = human_images_topright[self.counter]
                self.counter = (self.counter + 1) % len(human_images_up)
                self.speedy = -PSPEED
                self.speedx = PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = 7
                    self.speedx = -7

            if key[pygame.K_UP] and key[pygame.K_LEFT]:
                self.image = human_images_topleft[self.counter]
                self.counter = (self.counter + 1) % len(human_images_up)
                self.speedy = -PSPEED
                self.speedx = -PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = 7
                    self.speedx = 7

            if key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
                self.image = human_images_bottomright[self.counter]
                self.counter = (self.counter + 1) % len(human_images_down)
                self.speedy = PSPEED
                self.speedx = PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = -7
                    self.speedx = -7

            if key[pygame.K_DOWN] and key[pygame.K_LEFT]:
                self.image = human_images_bottomleft[self.counter]
                self.counter = (self.counter + 1) % len(human_images_down)
                self.speedy = PSPEED
                self.speedx = -PSPEED

                # Collision detection against solid objects
                if player_solid_object_collision(terrain_objects_group):
                    self.speedy = -7
                    self.speedx = 7

            # Update our sprite's position
            self.rect.x += self.speedx
            # xPosition logic and boundary
            if self.rect.x < 20:
                self.rect.x = 21
            if self.rect.x > 765:
                self.rect.x = 760
            self.rect.y += self.speedy
            # yPosition logic and boundary
            if self.rect.y < 15:
                self.rect.y = 16
            if self.rect.y > 555:
                self.rect.y = 550
        # Object dies
        else:
            while self.counterDie < len(human_die_north):
                self.image = human_die_north[self.counterDie]
                self.counterDie += 1


# Arrow sprite
class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Our index
        self.counterImage = 0
        self.random = random.randrange(0,10)
        self.alive = True
        self.isDestructive = False

        # Arrow location starting logic
        if self.random > 5:
            arrowY = arrowYBoundaryTop
            arrowX = random.randrange(17, 780)
        else:
            arrowY = arrowYBoundaryBottom
            arrowX = random.randrange(17, 780)

        # Our image
        self.image = arrow_images_idle[self.counterImage]
        self.rect = pygame.Rect(arrowX, arrowY, 25, 25)
        self.speedy = random.randrange(3, 10)

    # Animate and update position
    def animate_direction(self, direction, speed):
        self.image = direction[self.counterImage]
        self.counterImage = (self.counterImage + 1) % len(direction)
        self.rect.y += speed

    def animate_death(self):
        if self.random > 5:
            self.rect.y = arrowYBoundaryTop
            self.rect.x = random.randrange(17, 780)

            # Reset direction and lives again
            self.alive = True
        else:
            self.rect.y = arrowYBoundaryBottom
            self.rect.x = random.randrange(16, 586)

            # Reset direction and lives again
            self.alive = True

    def update(self):
        # Image update
        if self.alive:
            # Self.random calculates direction, if > 5, then moves east, else west
            if self.random > 5:
                self.animate_direction(arrow_images_down, self.speedy)
            else:
                self.animate_direction(arrow_images_up, -self.speedy)
        else:
            self.animate_death()

        # If Fireball is outside of screen, then dies
        if self.random > 5:
            if self.rect.y > arrowYBoundaryBottom:
                self.alive = False
        else:
            if self.rect.y < arrowYBoundaryTop:
                self.alive = False


# Fireball Sprite
class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Our index
        self.counterImage = 0
        self.counterDie = 0
        self.random = random.randrange(0,10)
        self.alive = True
        self.isDestructive = True

        # Fireball location starting logic
        if self.random > 5:
            fireballY = random.randrange(16,586)
            fireballX = fireballXBoundaryLeft
        else:
            fireballY = random.randrange(16, 586)
            fireballX = fireballXBoundaryRight

        # Our default Image
        self.image = fireball_right[self.counterImage]
        self.rect = pygame.Rect(fireballX, fireballY, 35,35)
        self.speedx = random.randrange(3, 10)

    # Animate and update position
    def animate_direction(self, direction, speed):
        self.image = direction[self.counterImage]
        self.counterImage = (self.counterImage + 1) % len(direction)
        self.rect.x += speed

    # Animate death and gives new position
    def animate_death(self):
        self.image = fireball_die[self.counterDie]
        self.counterDie = (self.counterDie + 1) % len(fireball_die)

        if self.random > 5:
            if self.counterDie == len(fireball_die) - 1:
                self.rect.y = random.randrange(16, 586)
                self.rect.x = fireballXBoundaryLeft - 35

                # Reset direction and lives again
                self.alive = True
        else:
            if self.counterDie == len(fireball_die) - 1:
                self.rect.y = random.randrange(16, 586)
                self.rect.x = fireballXBoundaryRight

                # Reset direction and lives again
                self.alive = True

    def update(self):
        # Image update
        if self.alive:
            # Self.random calculates direction, if > 5, then moves east, else west
            if self.random > 5:
                self.animate_direction(fireball_right, self.speedx)
            else:
                self.animate_direction(fireball_left, -self.speedx)
        # Fireball is not alive
        else:
            self.animate_death()

        # If Fireball is outside of screen, then dies
        if self.random > 5:
            if self.rect.x > fireballXBoundaryRight:
                self.alive = False
        else:
            if self.rect.x < fireballXBoundaryLeft:
                self.alive = False


# Coin Sprite
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Attributes
        self.counterImage = 0
        self.timeToLive = 15
        self.start_ticks = pygame.time.get_ticks()

        self.x = random.randrange(25,775)
        self.y = random.randrange(25,575)

        # Our default Image
        self.image = coin_spin[self.counterImage]
        self.rect = pygame.Rect(self.x, self.y, 25, 25)


    def animate(self):
        self.image = coin_spin[self.counterImage]
        self.counterImage = (self.counterImage + 1) % len(coin_spin)

    def update(self):
        self.animate()

        # If coin last longer than 15 seconds then, dies
        #seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        #if seconds > self.timeToLive:
         #   self.kill()


        # If player touches coin, then he gets an extra 100 score
        if pygame.sprite.collide_mask(Player_1, self):
            collect_coin.play()
            Player_1.score += 100
            self.x = random.randrange(25, 775)
            self.y = random.randrange(25, 575)
            self.rect = pygame.Rect(self.x, self.y, 25, 25)


# Terrain Objects
class Terrain_Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Attributes
        self.index = random.randrange(0,3)
        self.counterImage = 0

        self.x = random.randrange(25, 675)
        self.y = random.randrange(25, 500)

        self.onFire = False
        self.isTree = False

        # Our default Image
        self.image = terrain_objects[self.index]
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    # Animate and update position
    def animate(self, image):
        self.image = image[self.counterImage]
        self.counterImage = (self.counterImage + 1) % len(image)

    def isItTree(self):
        if self.index == 0 or self.index == 1:
            self.isTree = True

    def update(self):
        # Checks if tree
        self.isItTree()

        if self.onFire:
            self.animate(flame)

# Player collision wi
# th moving objects against spriteGroups()
def player_moving_object_collision(spriteGroup):
    for object in spriteGroup:
        if pygame.sprite.collide_rect(Player_1, object):
            # Makes it so the arrow animation is on playerX and playerY coords for realism
            object.rect.y = Player_1.rect.y
            object.rect.x = Player_1.rect.x

            # Forces arrow to call death animation and reposition
            object.alive = False

            # Forces player to call death animation and stop movement
            Player_1.alive = False
            # Gets player current time of death to do logic for display death and then game over screen
            Player_1.start_ticks = pygame.time.get_ticks()

            break


def player_solid_object_collision(spriteGroup):
    for object in spriteGroup:
        if pygame.sprite.collide_mask(Player_1, object):
            # If player steps on fire, then dies
            if object.onFire:
                # Gets player current time of death to do logic for display death and then game over screen
                Player_1.start_ticks = pygame.time.get_ticks()
                Player_1.alive = False

            return True


def object_to_object_collision(spriteGroup1,spriteGroup2):
    for object1 in spriteGroup1:
        for object2 in spriteGroup2:
            if pygame.sprite.collide_rect(object1, object2):
                # Forces arrow/fireball to call death animation and reposition
                if not object2.onFire:
                    object1.alive = False

                    # Makes it so the arrow/fireball animation is on X and Y coords for realism
                    object1.rect.y = object2.rect.y
                    object1.rect.x = object2.rect.x

                if object2.isTree and object1.isDestructive:
                    object2.onFire = True

                break


# Game Loop
while True:
    # Loading screen
    if game_over:
        show_gameover_screen()
        # Game Setup
        arrows = []
        fireballs = []
        coins = []
        terrain_items = []
        load_assets()

        # Creating our player
        Player_1 = Player()

        # Music
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        # Max object counts
        arrow_counter = 0
        arrow_limit = 2
        fireball_counter = 0
        fireball_limit = 1
        coin_counter = 0
        coin_limit = 2
        terrain_counter = 0
        terrain_limit = 15

        # Empty groups
        player_group.empty()
        arrow_group.empty()
        fireball_group.empty()
        coin_group.empty()
        terrain_objects_group .empty()

        game_over = False

    # Add our player
    player_group.add(Player_1)

    # Wait to show death animation, then game over
    if Player_1.alive == False:
        seconds = (pygame.time.get_ticks() - Player_1.start_ticks) / 1000
        print(seconds)
        if seconds > Player_1.time:
            game_over = True

    #while alive:
        # Grabbing all events in game such as key and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If player wants to voluntarily quit
            alive = False  # Set our 'alive' logic to false to end loop
            game_over = True
            alive = True
        print(event)

    # Arrow object spawner
    if arrow_counter <= arrow_limit:
        # increment logical counter
        arrow_counter += 1

        # new arrow
        new_arrow = Arrow()
        arrow_group.add(new_arrow)

    # Fireball object spawner
    if fireball_counter <= fireball_limit:
        # increment logical counter
        fireball_counter += 1

        # new arrow
        new_fireball = Fireball()
        fireball_group.add(new_fireball)

    # Coin object spawner
    if coin_counter <= coin_limit:
        # incremental logical counter
        coin_counter += 1

        # new coin
        new_coin = Coin()
        coin_group.add(new_coin)

    # Terrain object spawner
    if terrain_counter <= terrain_limit:
        # incremental logical counter
        terrain_counter += 1

        # new coin
        new_terrain_object = Terrain_Object()
        terrain_objects_group.add(new_terrain_object)

    # Arrow to terrain objects collision
    object_to_object_collision(arrow_group, terrain_objects_group)

    # Fireball to terrain objects collision
    object_to_object_collision(fireball_group, terrain_objects_group)

    # Collision detection for fireball
    player_moving_object_collision(fireball_group)

    # Collision detection for arrow
    player_moving_object_collision(arrow_group)

    # Cast our background
    screen.blit(background, (0, 0))

    # Update our sprites
    terrain_objects_group.draw(screen)
    terrain_objects_group.update()
    player_group.update()
    player_group.draw(screen)
    fireball_group.update()
    fireball_group.draw(screen)
    arrow_group.update()
    arrow_group.draw(screen)
    coin_group.update()
    coin_group.draw(screen)

    # Our score
    drawText('Score: %s' % (Player_1.score), font, screen, 15, 10)

    # Quick sketch of levels and how difficulty can be implemented.
    # Code can be modified to a cleaner version later.
    if Player_1.score > 100 and Player_1.score  < 199:
        arrow_limit = 2
        fireball_limit = 2
    if Player_1.score > 200 and Player_1.score  < 299:
        arrow_limit = 5
        fireball_limit = 2
    if Player_1.score > 300 and Player_1.score  < 399:
        arrow_limit = 6
        fireball_limit = 2
    if Player_1.score > 400 and Player_1.score  < 499:
        arrow_limit = 7
        fireball_limit = 2
    if Player_1.score > 500 and Player_1.score  < 599:
        arrow_limit = 10
        fireball_limit = 3
    if Player_1.score > 600 and Player_1.score  < 699:
        arrow_limit = 12
        fireball_limit = 3
    if Player_1.score > 700 and Player_1.score  < 799:
        arrow_limit = 15
        fireball_limit = 4
    if Player_1.score > 800 and Player_1.score  < 899:
        arrow_limit = 20
        fireball_limit = 4
    if Player_1.score > 900 and Player_1.score  < 999:
        arrow_limit = 30
        fireball_limit = 4
    if Player_1.score > 1000 and Player_1.score  < 1199:
        arrow_limit = 40
        fireball_limit = 4
    if Player_1.score > 1200 and Player_1.score  < 1499:
        arrow_limit = 45
        fireball_limit = 6
    if Player_1.score > 1500 and Player_1.score  < 1999:
        arrow_limit = 55
        fireball_limit = 7
    if Player_1.score > 2000 and Player_1.score  < 2001:
        arrow_limit = 100
        fireball_limit = 10

    # Screen update
    pygame.display.flip()

    # Frames per second
    clock.tick(FPS)

