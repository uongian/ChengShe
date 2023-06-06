#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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
from button import Mybutton
from chess import Mychess
from red_settings import RedSettings
from black_settings import BlackSettings
import red_game_function as rgf
import black_game_function as bgf
from client import Client_thread

import pygame
import pygame.font
import traceback
from pygame.locals import *
import sys
import math
import panda3d.core 
import direct.showbase.ShowBase #Panda显示模块
import direct.gui.OnscreenText
import direct.task.Task #Panda任务模块
import direct.interval.LerpInterval
import direct.gui.DirectCheckButton
import collections
from client import *

def main():
	
	#启动客户端
	client = Client_thread()
	client.start()
	#等待匹配成功
	while client.status != 1:
		time.sleep(5)
	#初始化设置
	if client.side == 1:
		s = BlackSettings()
	else:
		s = RedSettings()
	s.side = client.side
	s.game_id = client.game_id
	s.counterpart_name = client.counterpart_name
	print(s.side)
	
	#初始化pygame和屏幕对象
	pygame.init()
	
	#创建一个窗口
	screen = pygame.display.set_mode([s.screen_width, 
									s.screen_height])
	# 设置窗口标题
	pygame.display.set_caption("中国象棋")
	
	
	#分配为黑方
	if s.side == 1:
		while True:
			
			Mychess.draw_chessboard(s, screen)
			Mychess.draw_all_chessman(s.r, screen, s.red_label, s.black_label)
			Mybutton.draw_button(screen)
			clock = pygame.time.Clock()
			if client.over == True:
				s.over = True
			bgf.check_events(s, screen, client)#监听所有事件
			if s.order == 1:
				#红棋落子
				bgf.red_order(s, screen)
			elif s.order == -1:
				#黑棋落子
				bgf.black_order(s, screen)
			if s.red_backup:
				#红框选中
				pygame.draw.rect(screen, [255, 0, 0], 
					[s.red_label[s.red_backup[0]]['cur_loc'][0] - 45, 
					s.red_label[s.red_backup[0]]['cur_loc'][1] - 45, 87, 87], 5)
			elif s.black_backup:
				#黑框选中
				pygame.draw.rect(screen, [0, 0, 0], 
					[s.black_label[s.black_backup[0]]['cur_loc'][0] - 45, 
					s.black_label[s.black_backup[0]]['cur_loc'][1] - 45, 87, 87], 5)
			#红方胜利
			if s.result == 1:
				bgf.red_victory(s, screen)
				client.quit()
			#黑方胜利
			elif s.result == -1:
				bgf.black_victory(s, screen)
				client.quit()
			elif s.result == 100:
				bgf.peace(s, screen)
				client.quit()
			pygame.display.flip()
		
	#分配为红方
	else:
		while True:
			Mychess.draw_chessboard(s, screen)
			Mychess.draw_all_chessman(s.r, screen, s.red_label, s.black_label)
			Mybutton.draw_button(screen)
			clock = pygame.time.Clock()
			if client.over == True:
				s.over = True
			rgf.check_events(s, screen, client)#监听所有事件
			if s.order == 1:
				#红棋落子
				rgf.red_order(s, screen)
			elif s.order == -1:
				#黑棋落子
				rgf.black_order(s, screen)
			if s.red_backup:
				#红框选中
				pygame.draw.rect(screen, [255, 0, 0], 
					[s.red_label[s.red_backup[0]]['cur_loc'][0] - 45, 
					s.red_label[s.red_backup[0]]['cur_loc'][1] - 45, 87, 87], 5)
			elif s.black_backup:
				#黑框选中
				pygame.draw.rect(screen, [0, 0, 0], 
					[s.black_label[s.black_backup[0]]['cur_loc'][0] - 45, 
					s.black_label[s.black_backup[0]]['cur_loc'][1] - 45, 87, 87], 5)
			#红方胜利
			if s.result == 1:
				rgf.red_victory(s, screen)
				client.quit()
			#黑方胜利
			elif s.result == -1:
				rgf.black_victory(s, screen)
				client.quit()
			elif s.result == 100:
				rgf.peace(s, screen)
				client.quit()
			pygame.display.flip()


if '__main__' == __name__:
	main()


if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()
