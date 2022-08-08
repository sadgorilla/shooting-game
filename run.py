### ---------------------------------------
### ------ SETUP

import sys, random, pygame as pg
from pygame.locals import *

pg.init()



### ---------------------------------------
### ------ VARIABLES

light_green = pg.Color(204, 255, 153)
orange = pg.Color(255, 100, 0)
red = pg.Color(255, 0, 0)
gray = pg.Color(152,152,152)
black = pg.Color(0,0,0)

clock = pg.time.Clock()

screen_size = screen_width, screen_height = 1000, 500
screen = pg.display.set_mode(screen_size)
screen_rect = screen.get_rect()

pg.display.set_caption("swag")

score = 0

time_since_shot = 0
primed = False


### ---------------------------------------
### ------ TEXT

font_big = pg.font.SysFont("garamond", 30, True, False)
font_smol = pg.font.SysFont("garamond", 20, False, False)

text_death = font_big.render("YOU DIED", True, black)
text_death_pos = text_death.get_rect()

text_respawn = font_smol.render("r to respawn", True, black)
text_respawn_pos = text_respawn.get_rect()

text_death_pos.center = screen_rect.center
text_death_pos.centery -= 40

text_respawn_pos.center = screen_rect.center
text_respawn_pos.centery -= 10

text_score = font_smol.render(f"score: {score}", True, black)
text_score_rect = text_score.get_rect()

text_score_rect.centerx = screen_rect.centerx
text_score_rect.centery = 15



### ---------------------------------------
### ------ CLASSES
		
class Lucian:
	surface = pg.image.load("./images/lucian-40px.jpg")
	rect = surface.get_rect()
	speed = [4, 0]
	alive = True

	def up_move(self):
		self.speed = [0, -4]

	def down_move(self):
	   	self.speed = [0, 4]

	def left_move(self):
		self.speed = [-4, 0]

	def right_move(self):
		self.speed = [4, 0]

	def shoot(self, first):
		new_bullet = Bullet(self)
		bullet_set.add(new_bullet)
		global primed, time_since_shot
		if first == True:
			time_since_shot = 0
			primed = True
		else:
			primed = False
		print("shoot")


class Bullet:
	def __init__(self, lucian):
		surface = pg.Surface((12,6))
		
		rect = surface.get_rect()
		rect.top = lucian.rect.center[1]
		rect.left = lucian.rect.right

		self.surface = surface
		self.rect = rect
		self.speed = [14, 0]
		self.state = True


class Mine:
	def __init__(self):
		surface = pg.Surface((20,20))
		surface.fill(red)

		rect = surface.get_rect()
		rect.top = random.randint(10, screen_height-30)
		rect.left = screen_width

		self.surface = surface
		self.rect = rect
		self.speed = [-3, 0]
		self.state = True

	def spawn():
		front_mine = Mine()
		mine_set.add(front_mine)

		back_mine = Mine()
		back_mine.rect.left = screen_width + 180
		back_mine.rect.top = front_mine.rect.top
		mine_set.add(back_mine)


class Explosion:
	def __init__(self, mine):
		surface = pg.Surface((50,50))
		surface.fill(light_green)

		rect = surface.get_rect()
		rect.center = mine.rect.center

		self.surface = surface
		self.rect = rect
		self.center = (25,25)
		self.radius = 25


def check_contact(bullet_obj, mine_obj):
	bullet = bullet_obj.rect
	mine = mine_obj.rect

	return ((mine.right > bullet.right > mine.left) and \
		((mine.top < bullet.bottom < mine.bottom) or (mine.top < bullet.top < mine.bottom)))


## DEFINING EVENT

custom = pg.event.custom_type()
my_event = pg.event.Event(custom) # can remove this line, and set arg to 'custom'
pg.time.set_timer(my_event, 2500)





lucian = Lucian()

bullet_set = set()
mine_set = set()
explosion_set = set()





time_between_shots = 0





### ----------------
### GAME LOOP 

run = True
while run:
	clock.tick(60)
	time_since_shot += clock.get_time()

	print(primed, time_since_shot)

	if primed is True and time_since_shot > 175:
		lucian.shoot(False)



	text_score = font_smol.render(f"score: {score}", True, black)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()

		if event.type == custom and lucian.alive:
			Mine.spawn()

		if event.type == pg.KEYDOWN:
			key = event.key
			if key == K_ESCAPE:
				sys.exit()

			elif key == K_UP:
				lucian.up_move()
			elif key == K_DOWN:
				lucian.down_move()
			elif key == K_RIGHT:
				lucian.right_move()
			elif key == K_LEFT:
				lucian.left_move()

			elif key == K_r and not lucian.alive:
				lucian.alive = True
				lucian.rect = lucian.surface.get_rect()
				lucian.speed = [4,0]
				score = 0

			elif key == K_SPACE and time_since_shot > 600:
				print("hi")
				lucian.shoot(True)




	lucian.rect = lucian.rect.move(lucian.speed)


	for bullet in bullet_set:
		if bullet.rect.left > screen_width:
			bullet.state = False
			continue
		bullet.rect = bullet.rect.move(bullet.speed)

	bullet_set = {bullet for bullet in bullet_set if bullet.state is True}


	for mine in mine_set:
		if mine.rect.right < 0:
			mine.state = False
			continue
		mine.rect = mine.rect.move(mine.speed)

	mine_set = {mine for mine in mine_set if mine.state is True}


	# MINES AND BULLETS HAVE BEEN MOVED, THOSE OFFSCREEN REMOVED

	for bullet in bullet_set:
		for mine in mine_set:
			contact = check_contact(bullet, mine)
			# print(contact)
			if contact:
				bullet.state = False
				mine.state = False
				print(mine.rect.center)
				explosion_set.add(Explosion(mine))
				score += 1
	bullet_set = {bullet for bullet in bullet_set if bullet.state is True}
	mine_set = {mine for mine in mine_set if mine.state is True}


	for explosion in explosion_set:
		explosion.surface.fill(light_green)
		explosion.radius -= 0.7
		pg.draw.circle(explosion.surface, orange, explosion.center, explosion.radius)

	explosion_set = {explosion for explosion in explosion_set if explosion.radius > 0}



	## LUCIAN DEATH

	if lucian.rect.right > screen_width or lucian.rect.left < 0 or \
		lucian.rect.bottom > screen_height or lucian.rect.top < 0:
		lucian.alive = False
		bullet_set.clear()
		mine_set.clear()
		explosion_set.clear()


	## PRINTING IMAGES TO SCREEN

	if lucian.alive:
		screen.fill(light_green)

		for explosion in explosion_set:
			screen.blit(explosion.surface, explosion.rect)

		for bullet in bullet_set:
			screen.blit(bullet.surface, bullet.rect)

		for mine in mine_set:
			screen.blit(mine.surface, mine.rect)

		screen.blit(lucian.surface, lucian.rect)

		
	else:
		screen.fill(gray)
		screen.blit(text_death, text_death_pos)
		screen.blit(text_respawn, text_respawn_pos)

	screen.blit(text_score, text_score_rect)
	pg.display.flip()