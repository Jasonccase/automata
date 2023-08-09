import numpy as np
import os
import time
import copy
from rich.console import Console

mask = [(-1,-1),(-1,0),(-1,1),
		(0,-1),		   (0,1),
		(1,-1), (1,0), (1,1)]

orientations = [(0,1),(-1,0),(0,-1),(-1,0)]

dev_grid =[ [0,0,0,0,0],
		 	[0,0,0,0,0],
		 	[0,0,1,0,0],
			[0,0,0,0,0],
		 	[0,0,0,0,0]]

size = (20,60)
speed = 0.25

class tile:
	def __init__(self,yx):
		self.yx = yx
		self.y,self.x = self.yx
		self.type = 0
		self.sprite = '░'

class plant:
	def __init__(self,yx):
		self.yx = yx
		self.type = 1
		self.neighbors = []
		self.sprite = '▒'

	def surroundings(self,grid,mask):
		for coord in mask:
			self.y,self.x = self.yx
			self.y,self.x = self.yx[0]+coord[0],self.yx[1]+coord[1]
			if self.y >= 0 and self.x >= 0 and self.y < len(grid) and self.x < len(grid[0]):
				self.y = ((self.y + len(grid)) % len(grid))
				self.x = ((self.x + len(grid[0])) % len(grid[0]))
				self.neighbors.append(grid[self.y][self.x])
			
		return

	def reproduce(self,grid):
		r = np.random.randint(0,5)
		if r == 4:
			cell = np.random.choice(self.neighbors)
			if cell.type == 0:
				grid[cell.y][cell.x] = plant((cell.y,cell.x))
		return grid

	def update(self,grid,mask):
		self.surroundings(grid,mask)
		return self.reproduce(grid)

class herbivore:
	def __init__(self,yx):
		self.yx = yx
		self.type = 2
		self.age = 0
		self.range = 2
		self.food = 0
		self.neighbors = []
		self.sprite = '█'
		self.orientation = (0,1)

	def surroundings(self,grid,mask):
		for coord in mask:
			self.y,self.x = self.yx
			self.y,self.x = self.yx[0]+coord[0],self.yx[1]+coord[1]
			if self.y >= 0 and self.x >= 0 and self.y < len(grid) and self.x < len(grid[0]):
				self.y = ((self.y + len(grid)) % len(grid))
				self.x = ((self.x + len(grid[0])) % len(grid[0]))
				self.neighbors.append(grid[self.y][self.x])
			
		return

	def move(self,grid):
		#grid[self.y+0][self.x+1] = self
		#grid[self.y][self.x] = tile((self.y,self.x))
		return

	def eat(self):
		return
	def reproduce(self):
		return
	def update(self,grid,mask):
		self.surroundings(grid,mask)
		self.move(grid)
		return grid

class carnivore:
	def __init__(self,yx):
		self.yx = yx
		self.type = 3
		self.age = 0
		self.range = 3
		self.food = 0
		self.neighbors = []

	def surroundings(self,grid,mask):
		for coord in mask:
			self.y,self.x = self.yx
			self.y,self.x = self.yx[0]+coord[0],self.yx[1]+coord[1]
			if self.y >= 0 and self.x >= 0 and self.y < len(grid) and self.x < len(grid[0]):
				self.y = ((self.y + len(grid)) % len(grid))
				self.x = ((self.x + len(grid[0])) % len(grid[0]))
				self.neighbors.append(grid[self.y][self.x])
			
		return

	def move(self):
		return
	def eat(self):
		return
	def reproduce(self):
		return

def generate_grid(size):
	grid = []
	grid = np.zeros(size)
	#grid = [[1 if np.random.randint(0,7) == 1 else 2 if np.random.randint(0,7) == 2 else 0 for cell in row] for row in grid]
	grid = [[0 for cell in row] for row in grid]
	return grid

def parse(grid):
	for y,row in enumerate(grid):
		for x,cell in enumerate(row):
			if cell == 1:
				grid[y][x] = plant((y,x))
			elif cell == 2:
				grid[y][x] = herbivore((y,x))
			elif cell == 3:
				grid[y][x] = carnivore((y,x)) 
			elif cell == 0:
				grid[y][x] = tile((y,x))

	return grid

def show(grid):
	disp = [[str(x.sprite) for x in y]for y in grid]
	for row in disp:
		print(''.join(row))
	return

def simulate(grid):
	for row in grid:
		for cell in row:
			if cell.type != 0:
				grid = cell.update(grid,mask)

grid = generate_grid(size)
grid[int(size[0]/2)][int(size[1]/2)] = 1
grid = parse(grid)

for i in range(100):
	Console().clear()
	show(grid)
	print(f'generation - {i+1}')
	simulate(grid)
	time.sleep(speed)



