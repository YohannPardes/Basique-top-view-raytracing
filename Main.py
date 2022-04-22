import pygame, time
from pygame.math import Vector2
from math import cos, sin, pi
from random import randrange

WIDTH = HEIGHT = 1000
box = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def deg_rad(degrees):
	"""A basic function that convert degrees to radians
	using - 1 radian = degree*(pi/180)"""

	return degrees*(pi/180)

class Obstacle:

	def __init__(self, pt1 = None, pt2 = None, random = True):

		if random:

			self.pt1 = Vector2(randrange(WIDTH), randrange(HEIGHT))
			self.pt2 = Vector2(randrange(WIDTH), randrange(HEIGHT))
		else:

			self.pt1 = Vector2(pt1[0], pt1[1])
			self.pt2 = Vector2(pt2[0], pt2[1])


	def show(self):

		pygame.draw.line(screen, (140, 140, 140), (self.pt1.x, self.pt1.y), (self.pt2.x, self.pt2.y), 1)

class Ray:

	def __init__(self, pos, dir):

		self.pos = Vector2(pos)
		self.dir = deg_rad(dir)
		self.size = 1

	def show(self):

		pygame.draw.line(screen, (255, 255, 255), (self.pos.x, self.pos.y), (self.pos.x+cos(self.dir)*self.size, self.pos.y-sin(self.dir)*self.size))

	def cast(self, wall):

		x1 = wall.pt1.x
		y1 = wall.pt1.y
		x2 = wall.pt2.x
		y2 = wall.pt2.y

		x3 = self.pos.x
		y3 = self.pos.y
		x4 = self.pos.x+cos(self.dir)
		y4 = self.pos.y-sin(self.dir)

		den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

		if den == 0:
			return False

		t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4))/den

		u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3))/den

		if t>0 and t<1 and u>0:

			return x1 + t*(x2-x1), y1 + t*(y2-y1)

		else:
			return False

	def set_dir(self, x, y):

		self.dir = deg_rad((Vector2(x-self.pos.x, y-self.pos.y)).angle_to(Vector2(1,0)))

	def update(self, pos):

		self.pos =  pos

	def look(self, walls):

		self.view_range = 1000
		closest = None 
		for wall in walls:
			pt = self.cast(wall)
			if pt:
				dist = ((pt[0]-self.pos.x)**2 + ((pt[1]-self.pos.y)**2))**0.5
				if dist < self.view_range:
					closest = pt
					self.view_range = dist

		return closest

class Particle:

	def __init__(self):
		self.pos = Vector2(WIDTH/2, HEIGHT/2)

		self.rays = []
		for deg in range(0, 360, 3):
			self.rays.append(Ray(self.pos, deg))

	def show(self, walls):
		for ray in self.rays:
			ray.show()

			pt = ray.look(walls)
			if pt:
				pygame.draw.line(screen, (255, 255, 255), ray.pos, pt, 2)
				# pygame.draw.circle(screen, (255, 255, 255), (int(pt[0]), int(pt[1])), 5)

	def update(self, pos):

		self.pos = Vector2(pos)

		for ray in self.rays:
			ray.pos = self.pos

walls = []
for i in range(4):
	i = Obstacle()
	walls.append(i)

if box:
	walls.append(Obstacle((0,0), (WIDTH,0), False))
	walls.append(Obstacle((WIDTH,0), (WIDTH,HEIGHT), False))
	walls.append(Obstacle((WIDTH,HEIGHT), (0,HEIGHT), False))
	walls.append(Obstacle((0,HEIGHT), (0,0), False))


P = Particle()

done = False
pos = (0,0)
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.MOUSEMOTION:
			pos = event.pos
	screen.fill((10, 10, 10))

	P.show(walls)
	P.update(pos)
	
	for O in walls:
		O.show()
	pygame.display.flip()