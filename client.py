#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
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

import uuid 
import sys
import json
import queue
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from pip._vendor.distlib.compat import raw_input


class Client_thread(threading.Thread):
	def __init__(self):
		
		"""
		初始化
		"""
		
		#线程
		super(Client_thread, self).__init__()
		#定义ip地址、端口号
		self.server_name = "10.21.190.77"
		self.server_port = 6688
		#socket连接
		self.clientSocket = socket(AF_INET, SOCK_STREAM)
		#用户名等定义
		self.name = "by"
		self.counterpart_name = ""
		self.inQueue = queue.Queue()
		self.outQueue = queue.Queue()
		self.clientSocket.setblocking(False)
		self.clientSocket.settimeout(0.5)
		self.game_id = ""
		self.side = 0
		self.quit_me = False
		self.status = 0
		self.changjiang = False
		self.over = False

	def send_msg_to(self,msg):
		
		"""
		发送信息
		"""
		
		try:
			#打包信息
			package = json.dumps(msg)
			package = package.encode('utf-8')
			self.clientSocket.send(package)
			return True
		except Exception as e:
			return False
			pass

	def recieve_msg_from(self):
		
		"""
		接收信息
		"""
		
		try:
			data = self.clientSocket.recv(1024)
			time.sleep(0.00001)
			data = json.loads(data)
			return data
		except Exception as e:
			pass

	def send_blocked(self,data):
		
		"""
		传输阻塞
		"""
		
		while True:
			if self.send_msg_to(data) == True:
				break
			if self.quit_me == True:
				self.clientSocket.close()
			time.sleep(0.5)

	def receive_blocked(self):
		
		"""
		接收阻塞
		"""
		
		while True:
			rec = self.recieve_msg_from()
			if rec:
				return rec
			if self.quit_me == True:
				self.clientSocket.close()
				return
			time.sleep(0.5)

	def quit(self):
		
		"""
		退出
		"""
		
		print("quit!")
		self.quit_me = True

	def run(self):
		
		"""
		运行线程
		"""
		
		self.clientSocket.connect((self.server_name,self.server_port))
		self.send_blocked({"type":0,"msg":{"name":self.name}})
		rec = self.receive_blocked()
		if self.quit_me == False:
			self.side = rec["side"]
			self.status = rec["status"]
			self.counterpart_name = rec["counterpart_name"]
			if rec["status"] == 1:
				self.inQueue.put(rec)
				time.sleep(0.5)
				self.game_id = rec["game_id"]
				while (True):
					if self.outQueue.empty() == False:
						send_msg = self.outQueue.get()
						self.send_msg_to(send_msg)
					rec = self.recieve_msg_from()
					if self.quit_me == True:
						if self.changjiang == True:
							self.send_msg_to({
								"type": 2,
								"msg": {
									"request": "exit",
									"game_id": self.game_id,
									"side": abs(1-self.side)
								}
							})
						else:
							self.send_msg_to({
								"type": 2,
								"msg": {
									"request": "exit",
									"game_id": self.game_id,
									"side": self.side
								}
							})
						break
					if not rec:
						time.sleep(0.5)
						continue
					if "status" in rec:
						#回复退出请求
						if rec["status"] == 2:  
							self.send_msg_to({"type": 3})
							self.over = True
							break
					else:
						print("received!*****************")
						print(rec)
						self.inQueue.put(rec)
			else:
				print("time out!")
			self.clientSocket.close()

