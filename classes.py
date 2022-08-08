### ---------------------------------------
### ------ SETUP

import sys, random, pygame as pg
from pygame.locals import *

pg.init()


light_green = pg.Color(204, 255, 153)
orange = pg.Color(255, 100, 0)
red = pg.Color(255, 0, 0)
gray = pg.Color(152,152,152)
black = pg.Color(0,0,0)

screen_size = screen_width, screen_height = 1000, 500


## ---------------------------------------
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

	def shoot(self, angle, speed):
		new_bullet = Bullet(self, angle, speed)
		return new_bullet

	
	
class Bullet:
	def __init__(self, lucian, angle, speed):
		surface = pg.Surface((12,6))
		#surface.set_alpha(80)
		surface.set_colorkey(light_green)
		surface = pg.transform.rotate(surface, angle)
		
		rect = surface.get_rect()
		rect.top = lucian.rect.center[1]
		rect.left = lucian.rect.right

		self.surface = surface
		self.rect = rect
		self.speed = speed
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

		back_mine = Mine()
		back_mine.rect.left = screen_width + 180
		back_mine.rect.top = front_mine.rect.top
		
		return [front_mine, back_mine]


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
