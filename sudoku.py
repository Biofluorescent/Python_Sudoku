import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

# Global Variables
BOARDS = ['debug', 'n00b', 'l33t', 'error']
MARGIN = 20 # Pixels around board
SIDE = 50 # Width of a cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width & Height of entire board


class SudokuError(Exception):
	"""
	An application specific error.
	"""
	pass
	

class SudokuBoard(object):
	"""
	Sudoku Board Representation
	"""
	def __init__(self, board_file):
		self.board = __create_board(board_file)
	
	
	def __create_board(self, board_file):
		# Create starting matrix, a list of a list
		board = []
		
		# iterate each line
		for line in board_file:
			line = line.strip()
			
			# Error if not 9 chars
			if len(line) != 9:
				board = []
				raise SudokuError("Each line in the sudoku puzzle must be 9 chars long.")

			# create list for this line
			board.append([])
			
			#then each character
			for c in line:
				# Error if not integer
				if not c.isdigit():
					raise SudokuError("Valid characters must be in 0-9")
				# Add to latest list for the line
				board[-1].append(int(c))
			
		# Raise error if not 9 lines
		if len(board) != 9:
			raise SudokuError("Each puzzle must be 9 lines long.")
		
		# Return constructed board
		return board


class SudokuGame(object):
	"""
	A Sudoku game, store board state and check if puzzle is completed.
	"""
	def __init__(self, board_file):
		self.board_file = board_file
		self.start_puzzle = SudokuBoard(board_file).board
		
	
	def start(self):
		self.game_over = False
		# Cannot assign to start_puzzle, it would act like a pointer, not a new object
		self.puzzle = []
		# Copy over each line
		for i in xrange(9):
			self.puzzle.append([])
			for j in xrange(9):
				self.puzzle[i].append(self.start_puzzle[i][j])


	def check_win(self):
		for row in xrange(9):
			if not self.__check_row(row):
				return False
		for column in xrange(9):
			if not self.__check_column(column):
				return False
		for row in xrange(3):
			for column in xrange(3):
				if not self.__check_square(row, column):
					return False
		self.game_over = True
		return True
		
		
	def __check_block(self, block):
		return set(block) == set(range(1, 10))
		
	
	def __check_row(self, row):
		return self.__check_block(self.puzzle[row])
		
	
	def __check_column(self, column):
		# List comprehension of a column
		return self.__check_block([self.puzzle[row][column] for row in xrange(9)])
		
	
	def __check_square(self, row, column):
		return self.__check_block(
			[
				self.puzzle[r][c]
				for r in xrange(row * 3, (row + 1) * 3)
				for c in xrange(column * 3, (column + 1) * 3)
			]
		)
	
	
class SudokuUI(Frame):
	"""
	The Tkinter UI, draws board and takes input.
	"""
	def __init__(self, parent, game):
		self.game = game
		self.parent = parent
		Frame.__init__(self, parent)
		
		self.row, self.col = 0, 0
		
		self.__initUI()
		
	
	def __initUI(self):
		self.parent.title("Sudoku")
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, width=Width, height=HEIGHT)
		self.canvas.pack(fill=BOTH, side=TOP)
		clear_botton = Button(self, text="Clear Answers", command=self.__clear_answers)
		clear_botton.pack(fill=BOTH, side=BOTTOM)
		
		self.__draw_grid()
		self.__draw_puzzle()
		
		# When click on puzzle, call __cell_clicked
		self.canvas.bind("<Button-1>", self.__cell_clicked)
		# When a key is pressed, call __key_pressed
		self.canvas.bind("<Key>", self.__key_pressed)
		
		
	def __draw_grid(self):
		"""
		Draws grid in 3x3 square
		"""
		for i in xrange(10):
			color = "blue" if i % 3 == 0 else "gray"
			
			x0 = MARGIN + i * SIDE
			y0 = MARGIN
			x1 = MARGIN + i * SIDE
			y1 = HEIGHT - MARGIN
			self.canvas.create_line(x0, y0, x1, y1, fill=color)
			
			x0 = MARGIN
			y0 = MARGIN + i * SIDE
			x1 = WIDTH - MARGIN
			y1 = MARGIN + i * SIDE
			self.canvas.create_line(x0, y0, x1, y1, fill=color)
			
	
	def __draw_puzzle(self):
		self.canvas.delete("numbers")
		for i in xrange(9):
			for j in xrange(9):
				answer = self.game.puzzle[i][j]
				if answer != 0:
					x = MARGIN + j * SIDE + SIDE / 2
					y = MARGIN + i * SIDE + SIDE / 2
					original = self.game.start_puzzle[i][j]
					color = "black" if answer == original else "sea green"
					self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)
					
					
	def __clear_answers(self):
		self.game.start()
		self.canvas.delete("victory")
		self.__draw_puzzle()
		
		
	def __cell_clicked(self, event):
		if self.game.game_over:
			return
		
		x, y = event.x, event.y
		if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
			self.canvas.focus_set()
			# get row and column
			row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
			
			# if cell already selected, deselect
			if (row, col) == (self.row, self.col):
				self.row, self.col = -1, -1
			elif self.game.puzzle[row][col] == 0:
				self.row, self.col = row, col
				
		self.__draw_cursor()
		
		
	def __draw_cursor(self):
		self.canvas.delete("cursor")
		if self.row >= 0 and self.col >=0:
		x0 = MARGIN + self.col * SIDE + 1
		y0 = MARGIN + self.row * SIDE + 1
		x1 = MARGIN + (self.col + 1) * SIDE - 1
		y1 = MARGIN + (self.row + 1) * SIDE - 1
		self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags = "cursor")
		
	
	def __key_pressed(self, event):
		if self.game.game_over:
			return
		if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
			self.game.puzzle[self.row][self.col] = int(event.char)
			self.col, self.row = -1, -1
			self.__draw_puzzle()
			self.__draw_cursor()
			if self.game.check_win():
				self.__draw_victory()
				
	
	def __draw_victory(self):
		# create oval (circle)
		x0 = y0 = MARGIN + SIDE * 2
		x1 = y1 = MARGIN + SIDE * 7
		self.canvas.create_oval(
			x0, y0, x1, y1, t
			ags="victory", fill="dark orange", outline="orange"
		)
		# Create text 
		x = y = MARGIN + 4 * SIDE + SIDE / 2
		self.canvas.create_text(
			x, y,
			text="You win!", tags="winner",
			fill="white", font=("Arial", 32)
		)