import numpy as np
import os
import time
import copy
from rich.console import Console

mask = [(-1,-1),(-1,0),(-1,1),
		(0,-1),		   (0,1),
		(1,-1), (1,0), (1,1)]

orientations = [(0,1),(1,0),(0,-1),(-1,0)]

dev_grid =[ [0,0,0,0,0,0,0,0,0],
		 	[0,1,1,1,1,1,1,1,0],
		 	[0,1,2,1,2,1,2,1,0],
			[0,1,1,1,1,1,1,1,0],
		 	[0,0,0,0,0,0,0,0,0]]

sheep_count = 0
grass_count = 0
simtime = 0
size = (25,75)
speed = 0.05

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
		self.ntype = 1
		self.ncheck = False
		self.sprite = '▒'

	def surroundings(self,sgrid,mask):
		self.neighbors = []
		for coord in mask:
			self.y,self.x = self.yx
			self.y,self.x = self.yx[0]+coord[0],self.yx[1]+coord[1]
			if self.y >= 0 and self.x >= 0 and self.y < len(sgrid) and self.x < len(sgrid[0]):
				self.y = ((self.y + len(sgrid)) % len(sgrid))
				self.x = ((self.x + len(sgrid[0])) % len(sgrid[0]))
				self.neighbors.append(sgrid[self.y][self.x])	
		return

	def reproduce(self,rgrid):
		self.ncheck = False
		for cell in self.neighbors:
			if cell.type != 1:
				self.ncheck = True
		if self.ncheck:
			r = np.random.randint(0,5)
			if r == 4:
				cell = np.random.choice(self.neighbors)
				if cell.type == 0:
					rgrid[cell.yx[0]][cell.yx[1]] = plant((cell.yx[0],cell.yx[1]))
		return rgrid

	def update(self,ugrid,mask):
		if self.ntype == 0:
			ugrid[self.yx[0]][self.yx[1]] = tile(self.yx)
		self.surroundings(ugrid,mask)
		ugrid = self.reproduce(ugrid)
		return ugrid

class herbivore:
	def __init__(self,yx):
		self.yx = yx
		self.type = 2
		self.ntype = 2
		self.age = 0
		self.lifespan = 30
		self.stamina = 2
		self.rstamina = self.stamina
		self.food = 0
		self.sprite = '█'
		self.orientation = (0,1)
		self.ate = False

	def surroundings(self,sgrid,mask):
		self.neighbors = []
		for coord in mask:
			self.y,self.x = self.yx
			self.y,self.x = self.yx[0]+coord[0],self.yx[1]+coord[1]
			if self.y >= 0 and self.x >= 0 and self.y < len(sgrid) and self.x < len(sgrid[0]):
				self.y = ((self.y + len(sgrid)) % len(sgrid))
				self.x = ((self.x + len(sgrid[0])) % len(sgrid[0]))
				self.neighbors.append(sgrid[self.y][self.x])
		return

	def move(self,mgrid):
		ro = np.random.randint(0,4)
		self.orientation = orientations[ro]
		ny = self.yx[0] + self.orientation[0]
		nx = self.yx[1] + self.orientation[1]
		if ny >= 0 and nx >= 0 and ny < len(mgrid) and nx < len(mgrid[0]): 
			cell = mgrid[ny][nx]
			if cell.type == 0:
				mgrid[ny][nx] = self
				mgrid[self.yx[0]][self.yx[1]] = tile(self.yx)
				self.yx = (ny,nx)
				
		return mgrid

	def eat(self):
		close_plants = []
		for cell in self.neighbors:
			if cell.type == 1:
				close_plants.append(cell)
		if close_plants != []:
			trg_plant = np.random.choice(close_plants)
			trg_plant.ntype = 0
			self.food += 1
		return

	def reproduce(self,rgrid):
		if self.food > 10:
			cell = np.random.choice(self.neighbors)
			if cell.type == 0:
				rgrid[cell.yx[0]][cell.yx[1]] = herbivore(cell.yx)
				self.food = 0
			else:
				self.food -= 3
		return 
		
	def update(self,ugrid,mask):
		#print(self.age,self.food)
		self.age += 1
		#if self.ntype == 0:
		#	ugrid[self.yx[0]][self.yx[1]] = tile(self.yx)
		self.surroundings(ugrid,mask)
		self.eat()
		self.reproduce(ugrid)
		ugrid = self.move(ugrid)
		if self.age >= self.lifespan:
			ugrid[self.yx[0]][self.yx[1]] = tile(self.yx)
		return ugrid

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

def splice(shape,yx,grid):
	for y,row in enumerate(shape):
		for x,cell in enumerate(row):
			grid[y+yx[0]][x+yx[1]] = cell
	return grid

def simulate(sgrid):
	sheep_count = 0
	grass_count = 0
	start = time.perf_counter()
	ngrid = copy.deepcopy(sgrid)
	for row in sgrid:
		for cell in row:
			if cell.type != 0:
				ngrid = cell.update(ngrid,mask)
				if cell.type == 1:
					grass_count += 1
				elif cell.type == 2:
					sheep_count += 1

	end = time.perf_counter()
	simtime = end - start
	return ngrid, simtime, grass_count, sheep_count

grid = generate_grid(size)
grid = splice(dev_grid,(int(len(grid)/2),int(len(grid[0])/2)),grid)
#grid = dev_grid
grid = parse(grid)

for i in range(5000):
	Console().clear()
	show(grid)
	print(f'generation - {i+1}  sheep - {sheep_count}  grass - {grass_count}')
	print(f'sim time - {simtime*100}')
	grid,simtime,grass_count,sheep_count = simulate(grid)
	time.sleep(speed)



