import socket
import sys
import threading
from threading import Thread
from random import randint
import time
import json

class Main:
	# Technical:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = 'localhost'
	port = 54416
	serveraddress = (host, port)
	sock.bind(serveraddress)
	sock.listen(4)

	clients = set()
	clients_lock = threading.Lock()
	connectionNum = 0

	# Game:
	players_max = 4
	players_params = 5
	playersMatrix = []
	for i in range (0, players_max):
		new = []
		for j in range (0, players_params):
			new.append(0)
		playersMatrix.append(new)
	# Player starting coordinates:
	playersMatrix[0][0] = 0		# local_id
	playersMatrix[0][1] = 0		# global_id
	playersMatrix[0][2] = 100	# coord_x
	playersMatrix[0][3] = 150	# coord_y
	playersMatrix[0][4] = 0		# direction
	playersMatrix[1][0] = 1
	playersMatrix[1][1] = 0
	playersMatrix[1][2] = 111
	playersMatrix[1][3] = 160
	playersMatrix[0][4] = 0
	playersMatrix[2][0] = 2
	playersMatrix[2][1] = 0
	playersMatrix[2][2] = 74
	playersMatrix[2][3] = 100
	playersMatrix[0][4] = 0
	playersMatrix[3][0] = 3
	playersMatrix[3][1] = 0
	playersMatrix[3][2] = 120
	playersMatrix[3][3] = 120
	playersMatrix[0][4] = 0

	bullet_list = []
	for i in range (0, 4):
		new = []
		for j in range (0, 3):
			new.append(0)
		bullet_list.append(new)
	def bulletsAdd(self, x, y, vector):
		Main.bullet_list.append([len(Main.bullet_list) + 1, [x, y, vector]])
	def bulletHandler(self): # rename?
		for i in len(Main.bullet_list):
			# Bullet's move:
			if Main.bullet_list[i][2] == 0: # 0 - UP
				Main.bullet_list[i][1] -= 1
			if Main.bullet_list[i][2] == 1: # 1 - LEFT
				Main.bullet_list[i][0] -= 1
			if Main.bullet_list[i][2] == 2: # 2 - DOWN
				Main.bullet_list[i][1] += 1
			if Main.bullet_list[i][2] == 3: # 3 - RIGHT
				Main.bullet_list[i][0] += 1
			# Collision check statement (rename?):
			if Main.bullet_list[i][0] > 300 or Main.bullet_list[i][0] < 0:
				Main.bullet_list.remove[i]
			elif Main.bullet_list[i][1] > 300 or Main.bullet_list[i][1] < 0:
				Main.bullet_list.remove[i]
			# TODO: add player collision
	def bulletDel(self): # WIP
		return 0

	def actionHandler(self, data): # Player's actions
		i = int(data[0]) # Player identificator
		# Player walk:
		if data[1:3] == '10':
			Main.playersMatrix[i][3] = Main.playersMatrix[i][3] - 1
		if data[1:3] == '11':
			Main.playersMatrix[i][2] = Main.playersMatrix[i][2] - 1
		if data[1:3] == '12':
			Main.playersMatrix[i][3] = Main.playersMatrix[i][3] + 1
		if data[1:3] == '13':
			Main.playersMatrix[i][2] = Main.playersMatrix[i][2] + 1
		# Player shoot:
		if data[3] == '1':
			self.bulletsAdd(Main.playersMatrix[i][2], Main.playersMatrix[i][3], data[2])

	def clientActionThread(self, connection, client_address):
		with self.clients_lock:
			self.clients.add(connection)
		try:
			while 1:
				data = connection.recv(4).decode()
				if data == 'updt': # client's update request while idling
					for c in self.clients:
						c.sendall(json.dumps(
							{
								"players_params": [{
									"local_id": Main.playersMatrix[0][0],
									"global_id": Main.playersMatrix[0][1],
									"coord_x": Main.playersMatrix[0][2],
									"coord_y": Main.playersMatrix[0][3],
									"direction": Main.playersMatrix[0][4]
								}, {
									"local_id": Main.playersMatrix[1][0],
									"global_id": Main.playersMatrix[1][1],
									"coord_x": Main.playersMatrix[1][2],
									"coord_y": Main.playersMatrix[1][3],
									"direction": Main.playersMatrix[1][4]
								}, {
									"local_id": Main.playersMatrix[2][0],
									"global_id": Main.playersMatrix[2][1],
									"coord_x": Main.playersMatrix[2][2],
									"coord_y": Main.playersMatrix[2][3],
									"direction": Main.playersMatrix[2][4]
								}, {
									"local_id": Main.playersMatrix[3][0],
									"global_id": Main.playersMatrix[3][1],
									"coord_x": Main.playersMatrix[3][2],
									"coord_y": Main.playersMatrix[3][3],
									"direction": Main.playersMatrix[3][4]
								}]
							}).encode())
				else: # client's update request during action
					self.actionHandler(data)
		finally:
			with self.clients_lock:
				print('No more data from ', client_address)
				Main.connectionNum = Main.connectionNum - 1
				self.clients.remove(connection)
				connection.close()

	def __init__(self):
		print('Server created.')
		# Main loop:
		while 1:
			if Main.connectionNum < 5:
				connection, client_address = Main.sock.accept()
				print('Client connected from ', client_address)
				Thread(target = self.clientActionThread, args = (connection, client_address)).start()
				connection.sendall(str(Main.connectionNum).encode())
				Main.connectionNum = Main.connectionNum + 1

main = Main()
main.__init__()