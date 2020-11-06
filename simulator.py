#!/usr/bin/env python3
import math
import os
import time

try:
	import pygame
except ImportError:
	os.system('start cmd /c pip3 install pygame')
	import pygame

from pygame.locals import *

pygame.init()
pygame.display.set_caption('John Conway\'s Game Of Life Simulator')

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1360, 700), RESIZABLE)

GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

CEIL_WIDTH = 1360
CEIL_HEIGHT = 680
BLOCKSIZE = 10

running = True
start = False

Cur = [[0 for col in range(136)] for row in range(68)]
Next = [val[:] for val in Cur]

font = pygame.font.SysFont('sans', 50)
Clear = font.render('Clear', True, BLACK)
Start = font.render('Start', True, BLACK)
Stop = font.render('Stop', True, BLACK)
Exit = font.render('Exit', True, BLACK)
Title = font.render('John Conway\'s Game Of Life Simulator', True, BLACK)

clock = pygame.time.Clock()

def drawGrid():
	for col in range(CEIL_WIDTH // BLOCKSIZE):
		for row in range(CEIL_HEIGHT // BLOCKSIZE):
			rect = pygame.Rect(col * BLOCKSIZE, row * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
			if Cur[row][col]:
				pygame.draw.rect(screen, YELLOW, rect, 1)
			else:
				pygame.draw.rect(screen, BLACK, rect, 1)

def simulation():
	global Cur, Next
	for row in range(68):
		for col in range(136):
			near = 0
			near += Cur[(row + 67) % 68][(col + 135) % 136]
			near += Cur[(row + 67) % 68][(col + 136) % 136]
			near += Cur[(row + 67) % 68][(col + 137) % 136]
			near += Cur[(row + 68) % 68][(col + 135) % 136]
			near += Cur[(row + 68) % 68][(col + 137) % 136]
			near += Cur[(row + 69) % 68][(col + 135) % 136]
			near += Cur[(row + 69) % 68][(col + 136) % 136]
			near += Cur[(row + 69) % 68][(col + 137) % 136]
			if Cur[row][col] == 1:
				if 2 <= near <= 3:
					Next[row][col] = 1
				else:
					Next[row][col] = 0
			elif Cur[row][col] == 0:
				if near == 3:
					Next[row][col] = 1
				else:
					Next[row][col] = 0
	Cur = [val[:] for val in Next]

while running:
	clock.tick(60)
	screen.fill(GREY)

	if start:
		pygame.time.wait(300)
		simulation()

	pygame.draw.rect(screen, BLACK, (95 , 695, 110, 60))
	pygame.draw.rect(screen, WHITE, (100, 700, 100, 50))
	screen.blit(Clear, (100, 695))

	pygame.draw.rect(screen, BLACK, (295, 695, 100, 60))
	pygame.draw.rect(screen, WHITE, (300, 700, 90 , 50))
	if start == True:
		screen.blit(Stop, (300, 695))
	else:
		screen.blit(Start, (300, 695))

	pygame.draw.rect(screen, BLACK, (495, 695, 90, 60))
	pygame.draw.rect(screen, WHITE, (500, 700, 80, 50))
	screen.blit(Exit, (500, 695))

	screen.blit(Title, (650, 695))

	drawGrid()

	mouseX, mouseY = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if 0 < mouseX < 1360 and 0 < mouseY < 680:
					row = mouseY // BLOCKSIZE
					col = mouseX // BLOCKSIZE
					Cur[row][col] = 1 - Cur[row][col]
				elif 95 < mouseX < 205 and 695 < mouseY < 755:
					Cur = [[0 for col in range(136)] for row in range(68)]
				elif 295 < mouseX < 395 and 695 < mouseY < 755:
					start = not start
				elif 495 < mouseX < 585 and 695 < mouseY < 755:
					running = False

	pygame.display.flip()

pygame.quit()
