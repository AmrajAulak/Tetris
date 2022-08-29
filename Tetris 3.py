
import pygame
from pygame.locals import *

pygame.init()

import random

#Consider the NumPy library

width, height = 500, 600

blockSize = 20
rows = 20
columns = 11
TblockSize = 19
margin = 1

gridHeight = rows * blockSize
gridWidth = columns * blockSize
sideB = (width - gridWidth) / 2
topB = (height - gridHeight) / 1.5

window = pygame.display.set_mode((width, height)) 
window.fill((0, 0, 0))

textFont = pygame.font.SysFont('Arial Rounded MT Bold.ttf', 24)  
text_colour = [255, 255, 255]
titleFont = pygame.font.SysFont('Arial Rounded MT Bold.ttf', 50)
goFont = pygame.font.SysFont('Arial Rounded MT Bold.ttf', 40)  

titleText = titleFont.render('TETRIS', True, text_colour)
text_r = textFont.render('Next Piece',True, text_colour)
gotext =goFont.render('Game Over!',True, text_colour)

O = [[1, 1],
	 [1, 1]]

T = [
	[[0, 1, 0],  
	 [1, 1, 1]], 
	 [[1, 0],
	  [1, 1],
	  [1, 0]],
	 [[1, 1, 1],
	  [0, 1, 0]],
	 [[0, 1],
	  [1, 1],
	  [0, 1]]
			]

S = [
	[[0, 1, 1],
	 [1, 1, 0]],
	 [[1, 0],
	  [1, 1],
	  [0, 1]],
	 [[0, 1, 1],
	  [1, 1, 0]],
	 [[1, 0],
	  [1, 1],
	  [0, 1]]
			]

Z = [
	[[1, 1, 0],
	 [0, 1, 1]],
	 [[0, 1],
	  [1, 1],
	  [1, 0]],
	 [[1, 1, 0],
	  [0, 1, 1]],
	 [[0, 1],
	  [1, 1],
	  [1, 0]]
			]

I = [
	[[1, 1, 1, 1]],
	 [[1],
	  [1],
	  [1],
	  [1]]
		 ]


L1 = [
	[[1, 0, 0],
	 [1, 1, 1]],
	 [[1, 1],
	  [1, 0],
	  [1, 0]],
	 [[1, 1, 1],
	  [0, 0, 1]],
	 [[0, 1],
	  [0, 1],
	  [1, 1]]
			]

L2 = [
	[[0, 0, 1],
	 [1, 1, 1]],
	 [[1, 0],
	  [1, 0],
	  [1, 1]],
	 [[1, 1, 1],
	  [1, 0, 0]],
	 [[1, 1],
	  [0, 1],
	  [0, 1]]
			]

y = (255, 255, 0)
r = (255, 0, 0)
lb = (0, 255, 247)
db = (21, 0, 255)
g = (14, 237, 59)
o = (237, 144, 14)
p = (152, 14, 237)

shape_selection = ['O', 'T', 'S', 'Z', 'I', 'L1', 'L2']
topLeft_init = [[5,0], [4,0], [4,0], [4,0], [5,0], [4,0], [4,0]]
colours = [y, p, g, r, lb, db, o]
	
landed = []

clock = pygame.time.Clock()




def draw_grid():
	for y in range (0, rows + 1):
		pygame.draw.line(window, (255, 255, 255),(sideB, (topB + y * blockSize)), ((sideB + gridWidth), (topB + y * blockSize)),1)
		for x in range (0, columns + 1):
			pygame.draw.line(window, (255, 255, 255), ((sideB + x * blockSize), topB), ((sideB + x * blockSize),(topB + gridHeight)), 1)

def make_grid():
	for i in range (rows):
		landed.append([])
		for j in range (columns):
			landed[i].append(0)
	

class Piece:
	def __init__(self):
		self.shapePick = O
		self.piece = 0
		self.piecePos = 0
		self.topLeft = 0
		self.pot_topLeft = 0
		self.rot_ind = 0
		self.colour = 0
		self.isLanded = False

	def get_shape(self):
		
		self.shapePick = str(random.choices(shape_selection))[2:-2]

		if self.shapePick == 'O':
			self.piecePos = O
			self.piece = self.piecePos

		else:

			if self.shapePick == 'T':
				self.piecePos = T
			elif self.shapePick == 'S':
				self.piecePos = S
			elif self.shapePick == 'Z':
				self.piecePos = Z
			elif self.shapePick == 'I':
				self.piecePos = I
			elif self.shapePick == 'L1':
				self.piecePos = L1
			elif self.shapePick == 'L2':
				self.piecePos = L2

			self.piece = self.piecePos[0]
			
		self.colour = colours[shape_selection.index(self.shapePick)]



	def spawn_piece(self):
		
		self.topLeft = [topLeft_init[shape_selection.index(self.shapePick)][0], 0]
		self.pot_topLeft = [self.topLeft[0], self.topLeft[1] + 1]
		

	def move_piece(self, mv_type):
		if self.piece != 0:
			if mv_type == 'left' and self.topLeft[0] > 0:
		
				self.pot_topLeft[0] += -1
				self.pot_topLeft[1] += -1
				self.isMoveValid()
				self.pot_topLeft[1] += 1

				if not self.isLanded:
					self.topLeft[0] += -1
				else: 
					self.pot_topLeft[0] += 1

			if mv_type == 'right' and self.topLeft[0] < (columns - len(self.piece[0])):

				self.pot_topLeft[0] += 1
				self.pot_topLeft[1] += -1
				self.isMoveValid()
				self.pot_topLeft[1] += 1

				if not self.isLanded:
					self.topLeft[0] += 1
				else: 
					self.pot_topLeft[0] += -1

			if mv_type == 'down':
				
				self.pot_topLeft[1] += 2
				self.isMoveValid()
				if not self.isLanded:
					self.topLeft[1] += 2
				else: 
					self.pot_topLeft[1] += -2
				
			if mv_type == 'up':	

				if self.shapePick != 'O':

					if self.rot_ind < (len(self.piecePos) - 1):
						self.rot_ind += 1
					else:
						self.rot_ind = 0
					
					self.piece = self.piecePos[self.rot_ind] 

					if (self.topLeft[0] + len(self.piece[0])) > columns:
						self.topLeft[0] = columns - len(self.piece[0])
						self.pot_topLeft[0] = self.topLeft[0]


					self.isMoveValid()
					if self.isLanded:
						if self.rot_ind == 0:
							self.rot_ind = len(self.piecePos) - 1
						else:
							self.rot_ind += -1

						self.piece = self.piecePos[self.rot_ind]
					

	def isMoveValid (self):
		self.isLanded = False
		if (self.pot_topLeft[1] + len(self.piece)) > rows:
			self.isLanded = True
			return
		for i in range(len(self.piece)):
			for j in range(len(self.piece[i])):
				if self.piece[i][j] != 0:
					if landed[i + self.pot_topLeft[1]][j + self.pot_topLeft[0]] != 0:
						self.isLanded = True


	def freeze_piece(self):
		for i in range(len(self.piece)):
			for j in range(len(self.piece[i])):
				if self.piece[i][j] != 0:
					landed[i + self.topLeft[1]][j + self.topLeft[0]] = self.colour
	
	
	def draw_piece(self):
		if self.piece != 0:
			for i in range(len(self.piece)):
				for j in range(len(self.piece[i])):
					if self.piece[i][j] != 0:
						pygame.draw.rect(window, self.colour, pygame.Rect((
							sideB + (self.topLeft[0] + j)*blockSize + margin),(topB + (self.topLeft[1] + i)*blockSize + margin), TblockSize, TblockSize))


	def draw_landed(self):
		for i in range(len(landed)):
			for j in range(len(landed[i])):
				if landed[i][j] != 0:
					pygame.draw.rect(window, landed[i][j], pygame.Rect((
						sideB + (j * blockSize) + margin),(
							topB + (i * blockSize) + margin), TblockSize, TblockSize))

	
	def draw_shape(self):
		if self.piece != 0:
			for i in range(len(self.piece)):
				for j in range(len(self.piece[i])):
					if self.piece[i][j] != 0:
						pygame.draw.rect(window, self.colour, pygame.Rect((1.2 * sideB + gridWidth + j*blockSize + margin),(
							topB + gridHeight/2 + i*blockSize + margin), TblockSize, TblockSize))

class Game ():
	score = 0
	level = 0
	def __init__(self):
		self.isFilled = False
		self.visited = 0
		self.rClear, self.rows = 0, []
		self.topHalf = 0
		self.block_x = []
		self.block_y = []
		self.blocks = []
		self.ind_x = []
		self.ind_y = []
		self.top_left =[]
		self.clear, self.gameOver = False, False
	 
	def check_rows(self):
		self.clear = False
		self.rClear = 0
		cl_rows = []

		for i in range(len(landed)):
			self.isFilled = True
			for j in range(len(landed[i])):
				if landed[i][j] == 0:
					self.isFilled = False 

			if self.isFilled:
				cl_rows.append(i)
				self.rClear = min(cl_rows)
				self.clear = True	  
		
		if self.clear:
			self.topHalf = landed[0:min(cl_rows)]
			
			Game.get_score(cl_rows)

			for i in range(max(cl_rows) + 1):
				landed[i] = [0] * columns
			self.get_blocks()
			self.check_rows()

	def check_gameOver(self):

		for x in range(len(landed[0])):
			if landed[0][x] != 0:
				self.gameOver = True
				window.blit(gotext, [5, topB + gridHeight + 10])
				pygame.display.update()
 
		while self.gameOver:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

	@classmethod
	def get_score(cls, cl_rows):

		count = 0
		count += len(cl_rows)
		n = 0
		if count == 10:
			cls.level += 1
			count = 0  

		if count == 1:
			n = 40 
		elif count == 2:
			n = 100
		else:
			n = 300

		cls.score += n * (cls.level + 1)

	@classmethod							
	def display_text(cls):
		
		score_text = textFont.render('Score: ' + str(cls.score), True, text_colour)
		window.blit(score_text, [sideB/4, topB+ gridHeight/2])
		window.blit(titleText, titleText.get_rect(center=(width/2, topB * 0.5)))
		window.blit(text_r, [gridWidth + sideB* 1.2, topB+ 170 ])


	def get_blocks(self):  
		self.visited = [[False for i in range(columns)] for j in range(len(self.topHalf))]

		for j in range(columns):
			if (not self.visited[self.rClear-1][j] and self.topHalf[self.rClear-1][j] != 0):
				
				x = self.rClear - 1
				y = j	

				def floodfill(x, y):
						
					if not self.visited[x][y] and self.topHalf[x][y] != 0: # the base case
						self.ind_x.append(x)
						self.ind_y.append(y)
						self.visited[x][y] = True
					else:
						return
					
					if y < columns - 1:
						floodfill(x, y + 1) # move right

					if y > 0:
						floodfill(x, y - 1) # move left

					if x < len(self.topHalf) - 1:
						floodfill(x + 1, y) # move down

					if x > 0:
						floodfill(x - 1, y) # move up
					
				self.ind_x = []
				self.ind_y = []

				floodfill(x,y)

				self.block_x.append(self.ind_x)
				self.block_y.append(self.ind_y)

		# find smallest row and smallest column
				
		for i in range (len(self.block_x)):
			self.top_left.append([min(self.block_y[i]), min(self.block_x[i])])
			for j in range(len(self.block_x[i])):
				self.block_x[i][j] += -self.top_left[i][1]
				self.block_y[i][j] += -self.top_left[i][0]


		for x in range (len(self.block_x)):
			self.blocks.append([])
			for i in range (max(self.block_x[x]) + 1):
				self.blocks[x].append([])
				for j in range(max(self.block_y[x]) + 1):
					if self.topHalf[i + self.top_left[x][1]][j + self.top_left[x][0]] != 0:
						self.blocks[x][i].append(self.topHalf[i + self.top_left[x][1]][j + self.top_left[x][0]])
					else:
						self.blocks[x][i].append(0)

		self.shift_blocks()


	def shift_blocks(self):

		block = Piece()
		for x in range(len(self.blocks)):
			block.piece = self.blocks[x]
			block.topLeft = self.top_left[x]
			block.pot_topLeft = [block.topLeft[0], block.topLeft[1] + 1]
			block.isLanded = False


			while not block.isLanded:
				block.isMoveValid()
				block.topLeft[1] += 1
				block.pot_topLeft[1] = block.topLeft[1] + 1

			block.topLeft[1] += -1
				
			for i in range(len(block.piece)):
				for j in range(len(block.piece[i])):
					landed[i + block.topLeft[1]][j + block.topLeft[0]] = block.piece[i][j]



def update_position(tetromino,nxtp):
		
	tetromino.isMoveValid()

	if not tetromino.isLanded:
		tetromino.pot_topLeft[1] = tetromino.topLeft[1] + 2
		tetromino.topLeft[1] += 1
			
	else:
		if tetromino.piece != 0:
			tetromino.freeze_piece()

			g = Game()
			g.check_gameOver()
			g.check_rows()

			tetromino.isLanded = False
			tetromino.piecePos = nxtp.piecePos
			tetromino.piece  = nxtp.piece
			tetromino.shapePick = nxtp.shapePick
			tetromino.colour = nxtp.colour

			tetromino.spawn_piece()
			nxtp.get_shape()
			nxtp.draw_shape()



def main():

	time_elapsed = 0
	dt_old = 0

	make_grid()

	tetromino = Piece()
	nxtp = Piece()
	#g = Game()
	tetromino.get_shape()
	tetromino.spawn_piece()
	nxtp.get_shape()

	count = 0
	running = True
	mv = ''
	time_int = 500

	while running:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					tetromino.move_piece('left')
				elif event.key == pygame.K_RIGHT:
					tetromino.move_piece('right')
				elif event.key == pygame.K_UP:
					tetromino.move_piece('up')
				elif event.key == pygame.K_DOWN: 
					tetromino.move_piece('down')


		dt = pygame.time.get_ticks() 

		time_int += -0.005
		if (dt -dt_old) > time_int:
			update_position(tetromino,nxtp)
			dt_old = dt
		
		
		window.fill([0,0,0])
		draw_grid()
		tetromino.draw_piece()
		tetromino.draw_landed()
		nxtp.draw_shape()
		Game.display_text()
		pygame.display.flip()
		clock.tick(60)

main()







