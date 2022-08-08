### ---------------------------------------
### ------ SETUP

import sys, random, math, pygame as pg
import classes
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



#

def check_contact(bullet_obj, mine_obj):
	bullet = bullet_obj.rect
	mine = mine_obj.rect

	return ((mine.right > bullet.right > mine.left) and \
		((mine.top < bullet.bottom < mine.bottom) or (mine.top < bullet.top < mine.bottom)))


## DEFINING EVENT

custom = pg.event.custom_type()
my_event = pg.event.Event(custom) # can remove this line, and set arg to 'custom'
pg.time.set_timer(my_event, 2500)




# get speed of bullet

def get_speed(x_diff, y_diff):
	# x_diff positive -- shoot right (positive speed)
	# x_diff negative -- shoot left (negative speed)
	
	# y_diff positive -- shoot down (positive)
	# y_diff negative -- shoot up (negative)
	
	diffs_squared = (x_diff**2) / (y_diff**2)
	
	y = math.sqrt(100 / (1 + diffs_squared))
	
	if y_diff < 0:
		y = -y
	
	x = (x_diff / y_diff) * y
	return [x,y]






lucian = classes.Lucian()

bullet_set = set()
mine_set = set()
explosion_set = set()


time_since_shot = 0
score = 0

### ----------------
### GAME LOOP 

while 1:
	
	## read mouse
	
	#print(pg.mouse.get_pos())
	#print(pg.mouse.get_pressed())
	
	##	clock/timed events
	
	clock.tick(60)
	time_since_shot += clock.get_time()
		
	##	input events

	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()

		if event.type == custom and lucian.alive:
			mine_set.update(classes.Mine.spawn())

		if event.type == pg.KEYDOWN:
			key = event.key
			if key == K_ESCAPE:
				sys.exit()

			elif key == K_w:
				lucian.up_move()
			elif key == K_s:
				lucian.down_move()
			elif key == K_d:
				lucian.right_move()
			elif key == K_a:
				lucian.left_move()

			elif key == K_r and not lucian.alive:
				lucian.alive = True
				lucian.rect = lucian.surface.get_rect()
				lucian.speed = [4,0]
				score = 0


				
	click = pg.mouse.get_pressed()[0]
	
	if time_since_shot > 500 and  click:

		mouse_pos = pg.mouse.get_pos()
		lucian_pos = lucian.rect.midright
		
		print(f"mouse pos: {mouse_pos}")
		print(f"lucian pos: {lucian_pos}")
		
		x_diff = mouse_pos[0] - lucian_pos[0]
		y_diff = mouse_pos[1] - lucian_pos[1]
		
		print(x_diff, y_diff)
		
		
		speed_vector = get_speed(x_diff, y_diff)
		
		
		
		new_bullet = lucian.shoot(0, speed_vector)

		bullet_set.add(new_bullet)
		time_since_shot = 0
		
		print(new_bullet.speed)


				
				

	### update image
	
	## move objects
	
	lucian.rect = lucian.rect.move(lucian.speed)

		
	for bullet in bullet_set:
		bullet.rect = bullet.rect.move(bullet.speed)

	for mine in mine_set:
		mine.rect = mine.rect.move(mine.speed)
	
	
	## check collisions
	
	# bullet-mine collisions
	# 1. see if bullet-mine collide in new image
	# 2. if yes, set state to FALSE
	#			 and create explosion
	
	for bullet in bullet_set:
		for mine in mine_set:
			
			if bullet.state is False:
				break
			
			contact = check_contact(bullet, mine)
			if contact is True:
				bullet.state = False
				mine.state = False
				score += 1
				
				new_explosion = classes.Explosion(mine)
				explosion_set.add(new_explosion)
	
	
	
	# lucian-wall collision
	# 1. see if lucian-wall collide
	# 2. if yes, set alive to FALSE
		
	if lucian.rect.right > screen_width or lucian.rect.left < 0 or \
		lucian.rect.bottom > screen_height or lucian.rect.top < 0:
		
		lucian.alive = False
		bullet_set.clear()
		mine_set.clear()
		explosion_set.clear()
	
	
				
	# other-wall collisions
	# 1. see if bullet or mine collides with wall
	# 2. if yes, set state to FALSE
		
	for bullet in bullet_set:
		if bullet.rect.left > screen_width:
			bullet.state = False
	
	for mine in mine_set:
		if mine.rect.right < 0:
			mine.state = False
	
	
	# remove all FALSE bullets and mines from sets
	bullet_set = {bullet for bullet in bullet_set if bullet.state is True}
	mine_set = {mine for mine in mine_set if mine.state is True}
	
	

	## update explosion image	

	for explosion in explosion_set:
		explosion.surface.fill(light_green)
		explosion.radius -= 0.7
		pg.draw.circle(explosion.surface, orange, explosion.center, explosion.radius)

	explosion_set = {explosion for explosion in explosion_set if explosion.radius > 0}





	
		

	### print image

	text_score = font_smol.render(f"score: {score}", True, black)

	
	if lucian.alive:
		screen.fill(light_green)

		for explosion in explosion_set:
			screen.blit(explosion.surface, explosion.rect)

		for bullet in bullet_set:
			screen.blit(bullet.surface, bullet.rect)

		for mine in mine_set:
			screen.blit(mine.surface, mine.rect)

		screen.blit(lucian.surface, lucian.rect)

		
	else: # game over screen
		screen.fill(gray)
		
		screen.blit(text_death, text_death_pos)
		screen.blit(text_respawn, text_respawn_pos)

		
		
	screen.blit(font_smol.render(f"score: {score}", True, black), text_score_rect)
	
	pg.display.flip()
	
	#print(f"mine list: {mine_set}")
	#print(f"bullet list: {bullet_set}")
	#print(f"explosion list: {explosion_set}")

	
	
print("loop ended, end of program reached")