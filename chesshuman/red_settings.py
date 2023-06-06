#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  settings.py
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
import copy

class RedSettings():
	
	"""
	存储游戏的所有设置
	"""
	
	def __init__(self):
		
		"""
		初始化游戏的设置
		"""
		
		#设置屏幕参数
		self.screen_width = 1500
		self.screen_height = 1000
		self.back_color = (255, 214, 0) #背景颜色
		
		#设置棋盘参数
		self.d = 90 #棋盘格子边长
		self.originx = 60 #棋盘原点横坐标
		self.originy = 60 #棋盘原点纵坐标
		self.board_width = 780 #棋盘长度
		self.board_height = 870 #棋盘宽度
		self.outer_frame_color = (0, 0, 0) #外框线颜色
		self.board_color = (255, 214, 0) #棋盘颜色
		
		#设置棋子参数
		self.r = (int)(self.d / 2 - 2) #棋子半径
		
		#用于记录棋子当前状态
		self.red_label = {
				'帅': {'color':'red', 'cur_loc':[450, 900]},
				'仕1': {'color':'red', 'cur_loc':[360, 900]},
				'仕2': {'color':'red', 'cur_loc':[540, 900]},
				'相1': {'color':'red', 'cur_loc':[270, 900]},
				'相2': {'color':'red', 'cur_loc':[630, 900]},
				'马1': {'color':'red', 'cur_loc':[180, 900]},
				'马2': {'color':'red', 'cur_loc':[720, 900]},
				'车1': {'color':'red', 'cur_loc':[90, 900]},
				'车2': {'color':'red', 'cur_loc':[810, 900]},
				'炮1': {'color':'red', 'cur_loc':[180, 720]},
				'炮2': {'color':'red', 'cur_loc':[720, 720]},
				'兵1': {'color':'red', 'cur_loc':[90, 630]},
				'兵2': {'color':'red', 'cur_loc':[270, 630]},
				'兵3': {'color':'red', 'cur_loc':[450, 630]},
				'兵4': {'color':'red', 'cur_loc':[630, 630]},
				'兵5': {'color':'red', 'cur_loc':[810, 630]}
				}
		self.black_label = {
				'将': {'color':'black', 'cur_loc':[450, 90]},
				'士1': {'color':'black', 'cur_loc':[360, 90]},
				'士2': {'color':'black', 'cur_loc':[540, 90]},
				'象1': {'color':'black', 'cur_loc':[270, 90]},
				'象2': {'color':'black', 'cur_loc':[630, 90]},
				'马1': {'color':'black', 'cur_loc':[180, 90]},
				'马2': {'color':'black', 'cur_loc':[720, 90]},
				'车1': {'color':'black', 'cur_loc':[90, 90]},
				'车2': {'color':'black', 'cur_loc':[810, 90]},
				'炮1': {'color':'black', 'cur_loc':[180, 270]},
				'炮2': {'color':'black', 'cur_loc':[720, 270]},
				'卒1': {'color':'black', 'cur_loc':[90, 360]},
				'卒2': {'color':'black', 'cur_loc':[270, 360]},
				'卒3': {'color':'black', 'cur_loc':[450, 360]},
				'卒4': {'color':'black', 'cur_loc':[630, 360]},
				'卒5': {'color':'black', 'cur_loc':[810, 360]}
				}
				
				
		#用于暂时存储上一步棋的位置
		self.red_backup = []
		self.black_backup = []
		
		#记录执子落子状态
		self.running = True
		
		#记录输赢
		self.result = 0
		
		#记录游戏结束与否
		self.over = False
		
		#记录当前落子方，红棋先手
		self.order = 1

		#记录历史棋盘
		self.backup = []

		#记录常将
		self.red_attack = False
		self.red_attack_time = 0
		self.red_attack_judge = -1
		self.black_attack = False
		self.black_attack_time = 0
		self.black_attack_judge = -1
		
		#记录游戏昵称
		self.name = '倾斓'
		self.rival_name = ''
		#记录分配方，0为红方
		self.side = 0
		self.game_id = ""
		self.get = 0
		self.srcx  = 0
		self.srcy  = 0
		self.dstx  = 0
		self.dsty  = 0
		self.ssrcx  = 0
		self.ssrcy  = 0
		self.sdstx  = 0
		self.sdsty  = 0
		
