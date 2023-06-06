#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  board.py
#  
#  Copyright 2019 Nancyqinglan <Nancyqinglan@NANCYQINGLAN-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import pygame
import pygame.font
import sys
import traceback
from pygame.locals import *

import math
import panda3d.core
import direct.showbase.ShowBase
import direct.gui.OnscreenText
import direct.task.Task
import direct.interval.LerpInterval
import direct.gui.DirectCheckButton
 
 
pygame.font.init()
pygame.init()


class Mychess():
	def draw_chessboard(s, screen):
		
		'''
		绘制棋盘
		'''
		
		#填充背景色
		screen.fill(s.back_color)
		
		#加载背景图
		background = pygame.image.load('images/map.bmp')
		rect = background.get_rect()
		screen_rect = screen.get_rect()
		rect.centerx = screen_rect.centerx
		rect.bottom = screen_rect.bottom
		screen.blit(background, rect)
		
		#画外框和棋盘

		pygame.draw.rect(screen,s.outer_frame_color,
			[s.originx, s.originy,
			s.board_width, s.board_height],5)
		chessboard_rect = pygame.draw.rect(screen, s.board_color,
			[s.originx, s.originy,
			s.board_width, s.board_height])
			
		#加载棋盘纹理图
		chessboard_pic = pygame.image.load('images/chessboard.bmp')
		pic_rect = chessboard_pic.get_rect()
		pic_rect.centerx = chessboard_rect.centerx
		pic_rect.bottom = chessboard_rect.bottom
		screen.blit(chessboard_pic, pic_rect)
		
		
		#棋盘行
		inner_frame_color = (0, 0, 0)
		for i in range(1, 11):
			pygame.draw.line(screen, inner_frame_color,
				(s.d, s.d * i),
				(9 * s.d, s.d * i)) 
		
		#棋盘列
		for i in range(1, 10):
			pygame.draw.line(screen, inner_frame_color,
				(s.d * i, s.d),
				(s.d * i, 10 * s.d))
		
		#‘将/帅’田字格
		jiang_rote_color = (0, 0, 0)
		pygame.draw.lines(screen, jiang_rote_color, True,
			[(360, 90),(360, 270),(540, 270),(540, 90)], 3)
		pygame.draw.lines(screen, jiang_rote_color, True,
			[(360, 720),(360, 900),(540, 900),(540, 720)], 3)
		
		#‘士’路线
		shi_rote_color = (0, 0, 0)
		pygame.draw.line(screen, shi_rote_color, 
			(360, 90), (540, 270), 3)
		pygame.draw.line(screen, shi_rote_color, 
			(540, 90), (360, 270), 3) 
		pygame.draw.line(screen, shi_rote_color, 
			(360, 720), (540, 900), 3)
		pygame.draw.line(screen, shi_rote_color, 
			(540, 720), (360, 900), 3)
		
		#‘兵/卒’,用抗锯齿连续线段
		bing_rote_color = (255,0,0)
		for j in range(0,2):
			for k in range(0,4):
				pygame.draw.aalines(screen, bing_rote_color, False, 
					[(260 + 180 * k, 330 + 270 * j), 
					(260 + 180 * k, 350 + 270 * j), 
					(240 + 180 * k, 350 + 270 * j)], 3)
				pygame.draw.aalines(screen, bing_rote_color, False, 
					[(260 + 180 * k, 390 + 270 * j), 
					(260 + 180 * k, 370 + 270 * j), 
					(240 + 180 * k, 370 + 270 * j)], 3)
				pygame.draw.aalines(screen, bing_rote_color, False, 
					[(100 + 180 * k, 330 + 270 * j), 
					(100 + 180 * k, 350 + 270 * j), 
					(120 + 180 * k, 350 + 270 * j)], 3)
				pygame.draw.aalines(screen, bing_rote_color, False, 
					[(100 + 180 * k, 390 + 270 * j), 
					(100 + 180 * k, 370 + 270 * j), 
					(120 + 180 * k, 370 + 270 * j)], 3)
		
		#‘炮’
		pao_rote_color = (255,0,0)
		for m in range(0,2):
			for n in range(0,2):
				pygame.draw.aalines(screen, pao_rote_color, False, 
					[(170 + 540 * n, 240 + 450 * m),
					(170 + 540 * n, 260 + 450 * m),
					(150 + 540 * n, 260 + 450* m)], 3)
				pygame.draw.aalines(screen, pao_rote_color, False, 
					[(170 + 540 * n, 300 + 450 * m),
					(170 + 540 * n, 280 + 450 * m),
					(150 + 540 * n, 280 + 450 * m)], 3)
				pygame.draw.aalines(screen, pao_rote_color, False, 
					[(190 + 540 * n, 240 + 450 * m),
					(190 + 540 * n, 260 + 450 * m),
					(210 + 540 * n, 260 + 450 * m)], 3)
				pygame.draw.aalines(screen, pao_rote_color, False, 
					[(190 + 540 * n, 300 + 450 * m),
					(190 + 540 * n, 280 + 450 * m),
					(210 + 540 * n, 280 + 450 * m)], 3)
 
		#绘制‘楚河汉界’
		pygame.draw.rect(screen, s.back_color, [91, 451, 719, 89])
		font1 = pygame.font.Font('font1.ttf', 76)
		chuhehanjie = font1.render(" 楚 河     汉 界", True, [60, 20, 0])
		screen.blit(chuhehanjie, (130, 460))
		
	def draw_chessman(r, screen, color, chessman, x, y):
		
		"""
		绘制单个棋子
		"""
		
		red_color = (255, 0, 0)
		black_color = (0, 0, 0)
 
		pygame.draw.circle(screen,(0, 0, 0), (x, y), r)
		pygame.draw.circle(screen,(247, 157, 12),(x, y), r - 1)
		pygame.draw.circle(screen,(0, 0, 0),(x,y),r - 6, 3)
		pygame.draw.circle(screen,(181, 131, 16),(x, y), r - 11)
 
		font2 = pygame.font.Font('font1.ttf', 60)
 
		if color == 'red':
			q_color = red_color
		elif color == 'black':
			q_color = black_color
		screen.blit(font2.render(chessman[0], 
		True, q_color), (x - 30, y - 30))
	
	def draw_all_chessman(r, screen, red_label, black_label):
		
		"""
		绘制所有棋子
		"""
		
		#绘制红棋
		for each_chessman in red_label.keys():
			Mychess.draw_chessman(r, screen, 
			red_label[each_chessman]['color'], 
			each_chessman, red_label[each_chessman]['cur_loc'][0], 
			red_label[each_chessman]['cur_loc'][1])
		#绘制黑棋
		for each_chessman in black_label.keys():
			Mychess.draw_chessman(r, screen, 
			black_label[each_chessman]['color'], 
			each_chessman, black_label[each_chessman]['cur_loc'][0], 
			black_label[each_chessman]['cur_loc'][1])
			
		
