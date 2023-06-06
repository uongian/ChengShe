#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  button.py
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

class Mybutton():
	def draw_button(screen):
		
		'''
		绘制按键
		'''
		
		
		button_color = (163, 80, 21)
		pygame.draw.rect(screen, button_color, [1180, 55, 140, 100], 5)
		pygame.draw.rect(screen, button_color, [1340, 55, 140, 100], 5)
		pygame.draw.rect(screen, button_color, [1180, 255, 300, 100], 5)
		pygame.draw.rect(screen, button_color, [1180, 455, 300, 100], 5)
		pygame.draw.rect(screen, button_color, [1180, 655, 300, 100], 5)
 
		font = pygame.font.Font('font.ttf', 45)
		#画‘认输’，‘求和’，‘悔棋’，‘重新开始’和‘退出’按钮
		defeat = font.render("认  输", True, button_color)
		peace = font.render("求  和", True, button_color)
		retract = font.render("悔棋(Backspace)", True, button_color)
		restart = font.render("重新开始(F5)", True, button_color)
		withdraw = font.render("退出游戏(Esc)", True, button_color)
		screen.blit(defeat, (1190, 80))
		screen.blit(peace, (1350, 80))
		screen.blit(retract, (1180, 280))
		screen.blit(restart, (1210, 480))
		screen.blit(withdraw, (1200, 680))
		
