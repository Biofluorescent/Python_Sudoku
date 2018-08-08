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
	
	