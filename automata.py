import numpy as np
import random
import os
import time
from rich.console import Console

console = Console()

mask = [(-1,-1),(-1,0),(-1,1),
		(0,-1),(0,0),(0,1),
		(1,-1),(1,0),(1,1)
]

dev_board =[[0,0,0,0,0],
		 	[0,0,1,0,0],
		 	[0,1,1,1,0],
			[0,0,1,0,0],
		 	[0,0,0,0,0]
]

location = (2,2)
size = (50,50)
speed = 1

def generate_board(size):
	board = np.zeros(size)
	for x in range(size[1]):
		for y in range(size[0]):
			board[y,x] = random.randint(0,1)
	return board

def count_neighbors(xy,board):
	neighbors = 0
	for coord in mask:
		nx = xy[1]+coord[1]
		ny = xy[0]+coord[0]
		if nx >= 0 and ny >= 0 and nx < len(board[0]) and ny < len(board) and (ny,nx) != xy:
			if board[ny][nx] == 1:
				neighbors += 1

	return neighbors

def step(board):
	temp_board = np.copy(board)
	for y in range(len(board)):
		for x in range(len(board[y])):
			neighbors = count_neighbors((y,x),board)

			if board[y][x] == 1:
				if neighbors < 2:
					temp_board[y][x] = 0
				elif neighbors > 3:
					temp_board[y][x] = 0
			else:
				if neighbors == 3:
					temp_board[y][x] = 1
	print()
	return temp_board

def show(board):
	for row in board:
		for cell in row:
			print(int(cell),end='')
		print()

def simulate(generations,board):
	for i in range(generations):
		console.clear()
		show(board)
		board = step(board)
		time.sleep(speed)

board = generate_board(size)

generations = input('generations - ')
os.system('cls')
simulate(int(generations),board)


