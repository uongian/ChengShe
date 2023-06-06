#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game_function.py
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

import collections
import pygame
import pygame.font
import sys
import copy
from math import sqrt
from pygame.locals import *
import main
from client import *



def transfer(x, y):
	
	"""
	将像素坐标转换为棋盘坐标
	"""
	
	chess_x = x / 90 - 1
	chess_y = y / 90 - 1
	
	return [chess_x, chess_y]
	
def retransfer(chess_x, chess_y):
	
	"""
	将棋盘坐标转换为像素坐标
	"""
	
	x = (int)(90*(chess_x + 1))
	y = (int)(90*(chess_y + 1))
	
	return [x, y]
	
def getxy(client, s):
	
	"""
	接收对方消息
	"""
	
	if client.inQueue.empty() == False:  # to process the rival's message
		rival_move = client.inQueue.get()
		if "src" in rival_move:
			#翻转坐标
			s.srcx = abs(8 - rival_move["src"]["x"])
			s.srcy = abs(9 - rival_move["src"]["y"])
			s.dstx = abs(8 - rival_move["dst"]["x"])
			s.dsty = abs(9 - rival_move["dst"]["y"])
			#坐标转换
			[s.srcx, s.srcy] = retransfer(s.srcx, s.srcy)
			[s.dstx, s.dsty] = retransfer(s.dstx, s.dsty)
			#置收到消息信号为1
			s.get = 1
			
	print("收集到的坐标是", s.srcx, s.srcy, s.dstx, s.dsty)

def sendxy(client, s):
	
	"""
	发送己方消息
	"""
	
	[s.ssrcx, s.ssrcy] = transfer(s.ssrcx, s.ssrcy)
	[s.sdstx, s.sdsty] = transfer(s.sdstx, s.sdsty)
	if (s.side == 0 and s.order == 1 ):
		client.outQueue.put({
			"type": 1,
			"msg": {
				"game_id": client.game_id,
				"side": client.side,
				"src": {
					"x": s.ssrcx,
					"y": s.ssrcy
				},
				"dst": {
					"x": s.sdstx,
					"y": s.sdsty
				}
			}
		})
	if (s.side == 1 and s.order == -1):
		client.outQueue.put({
			"type": 1,
			"msg": {
				"game_id": client.game_id,
				"side": client.side,
				"src": {
					"x": s.ssrcx,
					"y": s.ssrcy
				},
				"dst": {
					"x": s.sdstx,
					"y": s.sdsty
				}
			}
		})

def check_events(s, screen, client):
	
	"""
	响应键盘和鼠标事件
	"""
	
	for event in pygame.event.get():
		#退出游戏
		if event.type == pygame.QUIT:
			client.quit()
			exit()
			withdraw()
		elif event.type == MOUSEBUTTONDOWN:
			#胜负未定
			if s.over == False:
				rival_chessman_move(client, s)
				chessman_move(event, s, screen, client)
				if s.red_attack_time == 3:
					if s.order == -1 and s.running == True:
						victory_judge(s)
				elif s.black_attack_time == 3:
					if s.order == 1 and s.running == True:
						victory_judge(s)
				else:
					victory_judge(s)
				if s.order == -1 and s.running == False:
					red_attack_judge(s)
				if s.order == 1 and s.running == False:
					black_attack_judge(s)
				
			#退出游戏
			if 1180 < event.pos[0] <1480 and 655 < event.pos[1] < 755:
				withdraw()
			#重新开始
			elif 1180 < event.pos[0] <1480 and 455 < event.pos[1] < 555:
				restart()
			#悔棋
			elif 1180 < event.pos[0] <1480 and 255 < event.pos[1] < 355:
				restract(s)
			#认输
			elif 1180 < event.pos[0] <1320 and 55 < event.pos[1] < 155:
				defeat(s)
			#求和
			elif 1340 < event.pos[0] <1480 and 55 < event.pos[1] < 155:
				s.result = 100
		elif event.type == pygame.KEYDOWN:
			#退出游戏
			if event.key == pygame.K_ESCAPE:
				withdraw()
			#重新开始
			elif event.key == pygame.K_F5:
				restart()
			#悔棋
			elif event.key == pygame.K_BACKSPACE:
				restract(s)
			
def red_victory(s, screen):
	
	"""
	红方胜利
	"""
	
	s.over = True
	victory = pygame.image.load('images/result.png')
	pic_rect = victory.get_rect()
	pic_rect.centerx = 450
	pic_rect.centery = 500
	screen.blit(victory, pic_rect)
	font = pygame.font.Font('font.ttf', 100)
	rv = font.render("红方胜利", True, [255, 0, 0])
	screen.blit(rv, (250, 450))
	
def black_victory(s, screen):
	
	"""
	黑方胜利
	"""
	
	s.over = True
	victory = pygame.image.load('images/result.png')
	pic_rect = victory.get_rect()
	pic_rect.centerx = 450
	pic_rect.centery = 500
	screen.blit(victory, pic_rect)
	font = pygame.font.Font('font.ttf', 100)
	bv = font.render("黑方胜利", True, [0, 0, 0])
	screen.blit(bv, (250, 450))
	
def victory_judge(s):
	
	"""
	判断输赢结果
	"""
	
	meet(s)
	if ('将' not in s.black_label.keys()) or s.black_attack_time == 3:
		s.result = 1
	if ('帅' not in s.red_label.keys()) or s.red_attack_time == 3:
		s.result = -1
		
def red_attack_judge(s):
	
	"""
	判断红方将军及常将
	"""
	
	s.red_attack = False
	for key in s.red_label.keys():
		if key != '帅':
			i = 0
			while i < len(s.red_label[key]['nxt_loc']):
				if '将' in s.black_label.keys():
					if s.red_label[key]['nxt_loc'][i] == s.black_label['将']['cur_loc']:
						s.red_attack = True
				i = i + 1
	if s.red_attack and s.red_attack_time == s.red_attack_judge:
		s.red_attack_time += 1
	else:
		s.red_attack_judge = -1
		s.red_attack_time = 0
	s.red_attack_judge += 1
	
def black_attack_judge(s):
	
	"""
	判断黑方将军及常将
	"""
	
	s.black_attack = False
	for key in s.black_label.keys():
		if key != '将':
			i = 0
			while i < len(s.black_label[key]['nxt_loc']):
				if '帅' in s.red_label.keys():
					if s.black_label[key]['nxt_loc'][i] == s.red_label['帅']['cur_loc']:
						s.black_attack = True
				i = i + 1
	if s.black_attack and s.black_attack_time == s.black_attack_judge:
		s.black_attack_time += 1
	else:
		s.black_attack_judge = -1
		s.black_attack_time = 0
	s.black_attack_judge += 1
	
def meet(s):
	
	"""
	判断将帅面对面的情况
	"""
	
	if '帅' in s.red_label.keys() and '将' in s.black_label.keys():
		x = s.red_label['帅']['cur_loc'][0]
		y = s.red_label['帅']['cur_loc'][1]
		nxtx = s.black_label['将']['cur_loc'][0]
		nxty = s.black_label['将']['cur_loc'][1]
		if s.red_label['帅']['cur_loc'][0] == s.black_label['将']['cur_loc'][0] and interval(x, y, nxtx, nxty, s) == 0:
			if s.order == 1:
				s.result = 1
			else:
				s.result = -1
		
def red_order(s, screen):
	
	"""
	红棋落子
	"""
	font = pygame.font.Font('font.ttf', 60)
	ro = font.render("红棋落子", True, [255, 0, 0])
	screen.blit(ro, (900, 50))
	
def black_order(s, screen):
	
	"""
	黑棋落子
	"""
	font = pygame.font.Font('font.ttf', 60)
	bo = font.render("黑棋落子", True, [0, 0, 0])
	screen.blit(bo, (900, 50))

def rival_chessman_move(client, s):
	
	"""
	对方棋子移动
	"""
	
	getxy(client, s)
	#暂存对方选中的红棋
	if s.order == 1 and s.get == 1:
		for key in s.red_label.keys():
			if s.srcx == s.red_label[key]['cur_loc'][0] and s.srcy == s.red_label[key]['cur_loc'][1]:
				s.red_backup = [key, s.red_label[key]]
	if s.red_backup:
		#改为落子状态
		s.running = False
	#更新红棋位置
	if s.red_backup and s.get == 1:
		print(loc_judge(s.dstx, s.dsty, s))
		if loc_judge(s.dstx, s.dsty, s) == -1:
			#删除选中位置的棋子
			print("**********************************")
			for key in list(s.black_label.keys()):
				if [s.dstx, s.dsty] == s.black_label[key]['cur_loc']:
					del s.black_label[key]
		s.red_label[s.red_backup[0]] = s.red_backup[1]
		s.red_label[s.red_backup[0]]['cur_loc'] = [s.dstx, s.dsty]
		
		#改为黑棋落子
		s.order = -1
		s.red_backup = []
		#改为选子状态
		s.running = True
	

def chessman_move(event, s, screen, client):
	
	"""
	己方棋子移动
	"""
	
	loc_to_move(s)
	if event.button == 1 and 47 < event.pos[0] < 853 and 47 < event.pos[1] < 943:
		#鼠标第一次按下选择棋子
		if s.running:
			red = copy.deepcopy(s.red_label)
			black = copy.deepcopy(s.black_label)
			s.backup.append([red, black])
			x, y = event.pos[0], event.pos[1]
			#暂存选中的黑棋
			if s.order == -1:
				for key in s.black_label.keys():
					if sqrt((s.black_label[key]['cur_loc'][0] - x) ** 2 
					+ (s.black_label[key]['cur_loc'][1] - y) ** 2) < s.r:
						s.black_backup = [key, s.black_label[key]]
						#保存初始位置
						s.ssrcx = (event.pos[0] + s.r) // 90 * 90
						s.ssrcy = (event.pos[1] + s.r) // 90 * 90
			if s.black_backup:
				#改为落子状态
				s.running = False
		#鼠标再次按下，落下棋子
		else:
			if s.r < event.pos[0] < 810 + s.r and s.r < event.pos[1] < 900 + s.r:
				x = (event.pos[0] + s.r) // 90 * 90
				y = (event.pos[1] + s.r) // 90 * 90
				#黑棋
				if s.black_backup:
					#判断所走位置不符合中国象棋规则
					if [x, y] not in s.black_label[s.black_backup[0]]['nxt_loc'] or loc_judge(x, y, s) == -1:
						s.black_label[s.black_backup[0]] = s.black_backup[1]
					#落子在新的位置
					else:
						s.sdstx = x
						s.sdsty = y
						#吃子
						if loc_judge(x, y, s) == 1:
							#删除选中位置的棋子
							for key in list(s.red_label.keys()):
								if [x, y] == s.red_label[key]['cur_loc']:
									del s.red_label[key]
							#位置被新棋子占领
							s.black_label[s.black_backup[0]] = s.black_backup[1]
							s.black_label[s.black_backup[0]]['cur_loc'] = [x, y]
							
						else:
							s.black_label[s.black_backup[0]] = s.black_backup[1]
							s.black_label[s.black_backup[0]]['cur_loc'] = [x, y]
						#发送消息后改为红棋落子
						sendxy(client, s)
						s.order = 1
					s.black_backup = []
					#改为选子状态
					s.running = True
					
			
def restract(s):
	
	"""
	悔棋
	"""
	
	if s.backup:
		s.red_label = s.backup[-1][0]
		s.black_label = s.backup[-1][1]
		s.backup.pop(-1)
		s.order = - s.order
		#分出胜负后
		if s.result != 0:
			s.result = 0
			s.over = False
	
def restart():
	
	"""
	重新开始
	"""
	
	main.main()
	
def withdraw():
	
	"""
	退出游戏
	"""
	
	pygame.quit()
	sys.exit()
	
def defeat(s):
	
	"""
	认输
	"""
	
	s.result = -s.order
		
def peace(s, screen):
	
	"""
	求和
	"""
	
	s.over = True
	victory = pygame.image.load('images/result.png')
	pic_rect = victory.get_rect()
	pic_rect.centerx = 450
	pic_rect.centery = 500
	screen.blit(victory, pic_rect)
	font = pygame.font.Font('font.ttf', 100)
	bv = font.render("  和   棋 ", True, [0, 0, 0])
	screen.blit(bv, (250, 450))
		
def find(x, y, s):
	
	"""
	通过位置寻找棋子
	"""
	
	for key in s.red_label.keys():
		if sqrt((s.red_label[key]['cur_loc'][0] - x) ** 2 + 
		(s.red_label[key]['cur_loc'][1] - y) ** 2) < r:
			return [key, s.red_label[key]]

	for key in s.black_label.keys():
		if sqrt((s.black_label[key]['cur_loc'][0] - x) ** 2 +
		(s.black_label[key]['cur_loc'][1] - y) ** 2) < r:
			return [key, s.black_label[key]]

def loc_judge(x, y, s):
	
	"""
	判断该位置有无棋子
	"""
	
	for key in s.red_label.keys():
		if [x, y] == s.red_label[key]['cur_loc']:
			return 1

	for key in s.black_label.keys():
		if [x, y] == s.black_label[key]['cur_loc']:
			return -1

	return 0
	
def out(x, y):
	
	"""
	判断该位置是否出界
	"""
	
	if x < 47 or x > 853 or y < 47 or y > 943:
		return True
	else:
		return False
		
def out_camp(x, y):
	
	"""
	判断将、帅、士、仕是否出田字格
	"""
	
	if 317 < x < 583 and (47 < y < 313 or 677 < y < 943):
		return False
	else:
		return True

def interval(x, y, nxtx, nxty, s):
	
	"""
	判断两个棋子中间相隔多少棋子
	"""
	
	tempx = x
	tempy = y
	count = 0
	if nxtx > x:
		while tempx < nxtx - s.d:
			tempx += s.d
			if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
				count = count + 1
		return count
	elif nxtx < x:
		while tempx > nxtx + s.d:
			tempx -= s.d
			if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
				count = count + 1
		return count
	if nxty > y:
		while tempy < nxty - s.d:
			tempy += s.d
			if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
				count = count + 1
		return count
	elif nxty < y:
		while tempy > nxty + s.d:
			tempy -= s.d
			if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
				count = count + 1
		return count
	return count
		

def loc_to_move(s):
	
	"""
	根据规则确定可走的位置
	"""
	
	#基础规则
	for key in s.red_label.keys():
		x = s.red_label[key]['cur_loc'][0]
		y = s.red_label[key]['cur_loc'][1]
		if key == '帅':
			s.red_label[key]['nxt_loc'] = [[x + s.d, y],
											[x - s.d, y],
											[x, y + s.d],
											[x, y - s.d]]
		elif (key == '仕1') or (key == '仕2'):
			s.red_label[key]['nxt_loc'] = [[x + s.d, y - s.d],
											[x - s.d, y - s.d],
											[x + s.d, y + s.d],
											[x - s.d, y + s.d]]
		elif key == '相1' or key == '相2':
			s.red_label[key]['nxt_loc'] = [[x + 2*s.d, y - 2*s.d],
											[x - 2*s.d, y - 2*s.d],
											[x + 2*s.d, y + 2*s.d],
											[x - 2*s.d, y + 2*s.d]]
		elif key == '马1' or key == '马2':
			s.red_label[key]['nxt_loc'] = [[x + s.d, y - 2*s.d],
											[x - s.d, y - 2*s.d],
											[x + s.d, y + 2*s.d],
											[x - s.d, y + 2*s.d],
											[x + 2*s.d, y - s.d],
											[x - 2*s.d, y - s.d],
											[x + 2*s.d, y + s.d],
											[x - 2*s.d, y + s.d]]
		elif key == '车1' or key == '车2':
			s.red_label[key]['nxt_loc'] = []
			i = 1
			while i <= 9:
				s.red_label[key]['nxt_loc'].append([x, y + s.d*i])
				s.red_label[key]['nxt_loc'].append([x + s.d*i, y])
				s.red_label[key]['nxt_loc'].append([x, y - s.d*i])
				s.red_label[key]['nxt_loc'].append([x - s.d*i, y])
				i = i + 1
		elif key == '炮1' or key == '炮2':
			s.red_label[key]['nxt_loc'] = []
			i = 1
			while i <= 9:
				s.red_label[key]['nxt_loc'].append([x, y + s.d*i])
				s.red_label[key]['nxt_loc'].append([x + s.d*i, y])
				s.red_label[key]['nxt_loc'].append([x, y - s.d*i])
				s.red_label[key]['nxt_loc'].append([x - s.d*i, y])
				i = i + 1
		elif key == '兵1' or key == '兵2' or key == '兵3' or key == '兵4' or key == '兵5':
			if s.d <= y <= 5*s.d:
				s.red_label[key]['nxt_loc'] = [[x, y + s.d]]
			else:
				s.red_label[key]['nxt_loc'] = [[x, y + s.d],
												[x + s.d, y],
												[x - s.d, y]]
	for key in s.black_label.keys():
		x = s.black_label[key]['cur_loc'][0]
		y = s.black_label[key]['cur_loc'][1]
		if key == '将':
			s.black_label[key]['nxt_loc'] = [[x + s.d, y],
											[x - s.d, y],
											[x, y + s.d],
											[x, y - s.d]]
		elif key == '士1' or key == '士2':
			s.black_label[key]['nxt_loc'] = [[x + s.d, y - s.d],
											[x - s.d, y - s.d],
											[x + s.d, y + s.d],
											[x - s.d, y + s.d]]
		elif key == '象1' or key == '象2':
			s.black_label[key]['nxt_loc'] = [[x + 2*s.d, y - 2*s.d],
											[x - 2*s.d, y - 2*s.d],
											[x + 2*s.d, y + 2*s.d],
											[x - 2*s.d, y + 2*s.d]]
		elif key == '马1' or key == '马2':
			s.black_label[key]['nxt_loc'] = [[x + s.d, y - 2*s.d],
											[x - s.d, y - 2*s.d],
											[x + s.d, y + 2*s.d],
											[x - s.d, y + 2*s.d],
											[x + 2*s.d, y - s.d],
											[x - 2*s.d, y - s.d],
											[x + 2*s.d, y + s.d],
											[x - 2*s.d, y + s.d]]
		elif key == '车1' or key == '车2':
			s.black_label[key]['nxt_loc'] = []
			i = 1
			while i <= 9:
				s.black_label[key]['nxt_loc'].append([x, y + s.d*i])
				s.black_label[key]['nxt_loc'].append([x + s.d*i, y])
				s.black_label[key]['nxt_loc'].append([x, y - s.d*i])
				s.black_label[key]['nxt_loc'].append([x - s.d*i, y])
				i = i + 1
		elif key == '炮1' or key == '炮2':
			s.black_label[key]['nxt_loc'] = []
			i = 1
			while i <= 9:
				s.black_label[key]['nxt_loc'].append([x, y + s.d*i])
				s.black_label[key]['nxt_loc'].append([x + s.d*i, y])
				s.black_label[key]['nxt_loc'].append([x, y - s.d*i])
				s.black_label[key]['nxt_loc'].append([x - s.d*i, y])
				i = i + 1
		elif key == '卒1' or key == '卒2' or key == '卒3' or key == '卒4' or key == '卒5':
			if 6*s.d <= y <= 10*s.d:
				s.black_label[key]['nxt_loc'] = [[x, y - s.d]]
			else:
				s.black_label[key]['nxt_loc'] = [[x, y - s.d],
												[x + s.d, y],
												[x - s.d, y]]
	#进一步规则
	for key in s.red_label.keys():
		x = s.red_label[key]['cur_loc'][0]
		y = s.red_label[key]['cur_loc'][1]
		i = 0
		while i < len(s.red_label[key]['nxt_loc']):
			#去掉超出棋盘范围的走位
			if out(s.red_label[key]['nxt_loc'][i][0], s.red_label[key]['nxt_loc'][i][1]):
				s.red_label[key]['nxt_loc'].pop(i)
				i = i - 1
			#去掉帅、仕超出田字格的走位
			if key == '帅' or key == '仕1' or key == '仕2':
				if out_camp(s.red_label[key]['nxt_loc'][i][0], s.red_label[key]['nxt_loc'][i][1]):
					s.red_label[key]['nxt_loc'].pop(i)
					i = i - 1
			#去掉相越过楚河汉界的走位
			if key == '相' or key == '相2':
				if s.red_label[key]['nxt_loc'][i][1] > 450:
					s.red_label[key]['nxt_loc'].pop(i)
					i = i - 1
			i = i + 1
		#蹩马腿
		if key == '马1' or key == '马2':
			i = 0
			while i < len(s.red_label[key]['nxt_loc']):
				if loc_judge(x + s.d, y, s) == 1 or loc_judge(x + s.d, y, s) == -1:
					if [x + 2*s.d, y - s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + 2*s.d, y - s.d])
						i = i - 1
					if [x + 2*s.d, y + s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + 2*s.d, y + s.d])
						i = i - 1
				if loc_judge(x - s.d, y, s) == 1 or loc_judge(x - s.d, y, s) == -1:
					if [x - 2*s.d, y - s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - 2*s.d, y - s.d])
						i = i - 1
					if [x - 2*s.d, y + s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - 2*s.d, y + s.d])
						i = i - 1
				if loc_judge(x, y - s.d, s) == 1 or loc_judge(x, y - s.d, s) == -1:
					if [x - s.d, y - 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - s.d, y - 2*s.d])
						i = i - 1
					if [x + s.d, y - 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x, y + s.d, s) == 1 or loc_judge(x, y + s.d, s) == -1:
					if [x - s.d, y + 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - s.d, y + 2*s.d])
						i = i - 1
					if [x + s.d, y + 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + s.d, y + 2*s.d])
						i = i - 1
				i = i + 1
		#塞象心
		elif key == '相1' or key == '相2':
			i = 0
			while i < len(s.red_label[key]['nxt_loc']):
				if loc_judge(x + s.d, y + s.d, s) == 1 or loc_judge(x + s.d, y + s.d, s) == -1:
					if [x + 2*s.d, y + 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + 2*s.d, y + 2*s.d])
						i = i - 1
				if loc_judge(x + s.d, y - s.d, s) == 1 or loc_judge(x + s.d, y - s.d, s) == -1:
					if [x + 2*s.d, y - 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x + 2*s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x - s.d, y - s.d, s) == 1 or loc_judge(x - s.d, y - s.d, s) == -1:
					if [x - 2*s.d, y - 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - 2*s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x - s.d, y + s.d, s) == 1 or loc_judge(x - s.d, y + s.d, s) == -1:
					if [x - 2*s.d, y + 2*s.d] in s.red_label[key]['nxt_loc']:
						s.red_label[key]['nxt_loc'].remove([x - 2*s.d, y + 2*s.d])
						i = i - 1
				i = i + 1
		#炮打隔子
		elif key == '炮1' or key == '炮2':
			i = 0
			while i < len(s.red_label[key]['nxt_loc']):
				if loc_judge(s.red_label[key]['nxt_loc'][i][0], s.red_label[key]['nxt_loc'][i][1], s) == -1:
					if interval(x, y, s.red_label[key]['nxt_loc'][i][0], s.red_label[key]['nxt_loc'][i][1], s) != 1:
						s.red_label[key]['nxt_loc'].pop(i)
						i = i - 1
				else:
					if interval(x, y, s.red_label[key]['nxt_loc'][i][0], s.red_label[key]['nxt_loc'][i][1], s) > 0:
						s.red_label[key]['nxt_loc'].pop(i)
				i = i + 1
		#车不间隔走直线
		elif key == '车1' or key == '车2':
			i = 0
			while i < len(s.red_label[key]['nxt_loc']):
				tempx = x
				tempy = y
				nxtx = s.red_label[key]['nxt_loc'][i][0]
				nxty = s.red_label[key]['nxt_loc'][i][1]
				if nxtx > x:
					while tempx < nxtx:
						tempx += s.d
						if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
							while tempx <= 810:
								tempx = tempx + s.d
								if [tempx, y] in s.red_label[key]['nxt_loc']:
									s.red_label[key]['nxt_loc'].remove([tempx, y])
					tempx = x
				elif nxtx < x:
					while tempx > nxtx:
						tempx -= s.d
						if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
							while tempx >= 90:
								tempx = tempx - s.d
								if [tempx, y] in s.red_label[key]['nxt_loc']:
									s.red_label[key]['nxt_loc'].remove([tempx, y])
					tempx = x
				if nxty > y:
					while tempy < nxty:
						tempy += s.d
						if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
							while tempy <= 900:
								tempy = tempy + s.d
								if [x, tempy] in s.red_label[key]['nxt_loc']:
									s.red_label[key]['nxt_loc'].remove([x, tempy])
					tempy = y
				elif nxty < y:
					while tempy > nxty:
						tempy -= s.d
						if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
							while tempy >= 90:
								tempy = tempy - s.d
								if [x, tempy] in s.red_label[key]['nxt_loc']:
									s.red_label[key]['nxt_loc'].remove([x, tempy])
					tempy = y
				i = i + 1
	for key in s.black_label.keys():
		x = s.black_label[key]['cur_loc'][0]
		y = s.black_label[key]['cur_loc'][1]
		
		i = 0
		while i < len(s.black_label[key]['nxt_loc']):
			#去掉超出棋盘范围的走位
			if out(s.black_label[key]['nxt_loc'][i][0], s.black_label[key]['nxt_loc'][i][1]):
				s.black_label[key]['nxt_loc'].pop(i)
				i = i - 1
			#去掉将、士超出田字格的走位
			if key == '将' or key == '士1' or key == '士2':
				if out_camp(s.black_label[key]['nxt_loc'][i][0], s.black_label[key]['nxt_loc'][i][1]):
					s.black_label[key]['nxt_loc'].pop(i)
					i = i - 1
			#去掉象越过楚河汉界的走位
			if key == '象' or key == '象2':
				if s.black_label[key]['nxt_loc'][i][1] < 540:
					s.black_label[key]['nxt_loc'].pop(i)
					i = i - 1
			i = i + 1
		#蹩马腿
		if key == '马1' or key == '马2':
			i = 0
			while i < len(s.black_label[key]['nxt_loc']):
				if loc_judge(x + s.d, y, s) == 1 or loc_judge(x + s.d, y, s) == -1:
					if [x + 2*s.d, y - s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + 2*s.d, y - s.d])
						i = i - 1
					if [x + 2*s.d, y + s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + 2*s.d, y + s.d])
						i = i - 1
				if loc_judge(x - s.d, y, s) == 1 or loc_judge(x - s.d, y, s) == -1:
					if [x - 2*s.d, y - s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - 2*s.d, y - s.d])
						i = i - 1
					if [x - 2*s.d, y + s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - 2*s.d, y + s.d])
						i = i - 1
				if loc_judge(x, y - s.d, s) == 1 or loc_judge(x, y - s.d, s) == -1:
					if [x - s.d, y - 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - s.d, y - 2*s.d])
						i = i - 1
					if [x + s.d, y - 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x, y + s.d, s) == 1 or loc_judge(x, y + s.d, s) == -1:
					if [x - s.d, y + 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - s.d, y + 2*s.d])
						i = i - 1
					if [x + s.d, y + 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + s.d, y + 2*s.d])
						i = i - 1
				i = i + 1
		#塞象心
		elif key == '象1' or key == '象2':
			i = 0
			while i < len(s.black_label[key]['nxt_loc']):
				if loc_judge(x + s.d, y + s.d, s) == 1 or loc_judge(x + s.d, y + s.d, s) == -1:
					if [x + 2*s.d, y + 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + 2*s.d, y + 2*s.d])
						i = i - 1
				if loc_judge(x + s.d, y - s.d, s) == 1 or loc_judge(x + s.d, y - s.d, s) == -1:
					if [x + 2*s.d, y - 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x + 2*s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x - s.d, y - s.d, s) == 1 or loc_judge(x - s.d, y - s.d, s) == -1:
					if [x - 2*s.d, y - 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - 2*s.d, y - 2*s.d])
						i = i - 1
				if loc_judge(x - s.d, y + s.d, s) == 1 or loc_judge(x - s.d, y + s.d, s) == -1:
					if [x - 2*s.d, y + 2*s.d] in s.black_label[key]['nxt_loc']:
						s.black_label[key]['nxt_loc'].remove([x - 2*s.d, y + 2*s.d])
						i = i - 1
				i = i + 1
		#炮打隔子
		elif key == '炮1' or key == '炮2':
			i = 0
			while i < len(s.black_label[key]['nxt_loc']):
				if loc_judge(s.black_label[key]['nxt_loc'][i][0], s.black_label[key]['nxt_loc'][i][1], s) == 1:
					if interval(x, y, s.black_label[key]['nxt_loc'][i][0], s.black_label[key]['nxt_loc'][i][1], s) != 1:
						s.black_label[key]['nxt_loc'].pop(i)
						i = i - 1
				else:
					if interval(x, y, s.black_label[key]['nxt_loc'][i][0], s.black_label[key]['nxt_loc'][i][1], s) > 0:
						s.black_label[key]['nxt_loc'].pop(i)
				i = i + 1
		#车不间隔走直线
		elif key == '车1' or key == '车2':
			i = 0
			while i < len(s.black_label[key]['nxt_loc']):
				tempx = x
				tempy = y
				nxtx = s.black_label[key]['nxt_loc'][i][0]
				nxty = s.black_label[key]['nxt_loc'][i][1]
				if nxtx > x:
					while tempx < nxtx:
						tempx += s.d
						if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
							while tempx <= 810:
								tempx = tempx + s.d
								if [tempx, y] in s.black_label[key]['nxt_loc']:
									s.black_label[key]['nxt_loc'].remove([tempx, y])
					tempx = x
				elif nxtx < x:
					while tempx > nxtx:
						tempx -= s.d
						if loc_judge(tempx, y, s) == 1 or loc_judge(tempx, y, s) == -1:
							while tempx >= 90:
								tempx = tempx - s.d
								if [tempx, y] in s.black_label[key]['nxt_loc']:
									s.black_label[key]['nxt_loc'].remove([tempx, y])
					tempx = x
				if nxty > y:
					while tempy < nxty:
						tempy += s.d
						if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
							while tempy <= 900:
								tempy = tempy + s.d
								if [x, tempy] in s.black_label[key]['nxt_loc']:
									s.black_label[key]['nxt_loc'].remove([x, tempy])
					tempy = y
				elif nxty < y:
					while tempy > nxty:
						tempy -= s.d
						if loc_judge(x, tempy, s) == 1 or loc_judge(x, tempy, s) == -1:
							while tempy >= 90:
								tempy = tempy - s.d
								if [x, tempy] in s.black_label[key]['nxt_loc']:
									s.black_label[key]['nxt_loc'].remove([x, tempy])
					tempy = y
				i = i + 1
