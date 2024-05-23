# Console 'flappy bird'-like game
# 2021

import time
import os
import random
import msvcrt

# Game field height
HEIGHT = 20
# Game field width
WIDTH = 40
# You can change screen update time by adjusting `UPDATE_TIME` 
UPDATE_TIME = 0.12
# DISTANCE BETWEEN COLUMNS
DBS = 12 

# Empty space symbol
DEFAULT_SYMBOL = ' '
COLUMN_SYMBOL = 'X'
PLAYER_SYMBOL = 'O'
G = 1

cls = lambda: os.system('cls')

def read_input():
	if msvcrt.kbhit():
		return msvcrt.getch()
	return False


class Player():

	def __init__(self, h):
		self.speed = 0
		self.pos = h // 2
		self.t = 0
		self.max_height = h

	def reset(self):
		self.speed = 0
		self.pos = self.max_height // 2
		self.t = 0

	def update_pos(self, t = 1):
		self.pos += self.speed * t
		self.speed += G * self.t
		self.t += t

	def get_pos(self):
		return self.pos

	def flap(self):
		self.speed = -1
		self.t = 0



class Field(): # добавлять колонны, очищать поле, двигать поле вправо влево, добавлять игрока

	def __init__(self, h, w):
		self.f_array = [[DEFAULT_SYMBOL] * w for i in range(h)]
		self.height = h
		self.width = w

	def set_player(self, p):
		if p.get_pos() < 0:
			self.f_array[0][1] = PLAYER_SYMBOL
			return True # gameover
		elif p.get_pos() >= self.height:
			self.f_array[self.height - 1][1] = PLAYER_SYMBOL
			return True
		elif self.check_for_collisions(p.get_pos()):
			self.f_array[p.get_pos()][1] = PLAYER_SYMBOL
			return True
		self.f_array[p.get_pos()][1] = PLAYER_SYMBOL
		return False

	def redraw(self):
		cls()
		for l in self.f_array:
			print(*l)

	def reset(self):
		for line in self.f_array:
			for i in range(self.width):
				line[i] = DEFAULT_SYMBOL

	def move_left(self):
		for line in self.f_array:
			for i in range(self.width - 1):
				line[i] = line[i + 1]
			line[self.width - 1] = DEFAULT_SYMBOL

	def make_column(self, min_window, max_window):
		w = random.randint(min_window, max_window)
		upper_column = random.randint(0, self.height - w)
		l = 0
		while l < upper_column:
			self.f_array[l][-1] = COLUMN_SYMBOL
			l += 1
		l += w
		while l < self.height:
			self.f_array[l][-1] = COLUMN_SYMBOL
			l += 1

	def replace(self, h, w, c = DEFAULT_SYMBOL):
		self.f_array[h][w] = c

	def animation(self, t = 0.01):
		for line in self.f_array:
			for i in range(self.width):
				line[i] = '.' #COLUMN_SYMBOL
			self.redraw()
			time.sleep(t/4)
		for line in self.f_array:
			for i in range(self.width):
				line[i] = DEFAULT_SYMBOL
			self.redraw()
			time.sleep(t)
		time.sleep(t*5)

	def check_for_collisions(self, player_pos): # It checks collisions between player and columns
		return self.f_array[player_pos][1] == COLUMN_SYMBOL

	
class Game():

	def __init__(self, height, width, update_time = 0.2):
		self.field = Field(height, width)
		self.player = Player(height)
		self.update_time = update_time
		self.high_score = 0
		self.score = 0
		self.gameover = False

	def update(self):
		if read_input():
			self.player.flap()
		last = self.player.get_pos()
		self.player.update_pos()
		self.field.move_left()
		if last > self.player.get_pos():
			self.field.replace(last, 0, '/')
		elif last < self.player.get_pos():
			self.field.replace(last, 0, '\\')
		else:
			self.field.replace(last, 0, '-')
		g_o = self.field.set_player(self.player) # set_player() returns bool, true if gameover
		self.field.redraw()
		print("SCORE:", self.score, " |  BEST:", self.high_score)
		return g_o # game over or not

	def animation(self):
		self.field.animation()

	def start(self):
		global s
		c = 0
		while True:
			if self.gameover:
				self.animation()
				self.player.reset()
				self.field.reset()
				self.field.redraw()
				print("SCORE:", self.score, " |  BEST:", self.high_score)
				self.high_score = max(self.score, self.high_score)
				self.score = 0
				c = 0
				print("Game over!")
				input("Нажмите Enter для продолжения... ")
				self.gameover = False
			self.gameover = self.update() # update() возвращает True если игра закончилась
			if c % DBS == 0:
				self.field.make_column(self.field.height // 4, self.field.height // 2)
			if (c - self.field.width + 3) >= 0 and (c - self.field.width + 3) % DBS == 0:
				self.score += 1
			c += 1
			time.sleep(self.update_time)

my_game = Game(HEIGHT, WIDTH, UPDATE_TIME)
my_game.start()
