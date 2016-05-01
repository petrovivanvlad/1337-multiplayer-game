import socket
import sys
import threading
from threading import Thread
from random import randint
import time

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

	package_lenght = 60 # Each package, which is sent to client, should be fixed by number of characters (length of string)

	# Game:
	players_max = 4
	players_params = 5 # 0 - server number, 1 - player id, 2 - x, 3 - y
	playersMatrix = []
	for i in range (0, players_max):
		new = []
		for j in range (0, players_params):
			new.append(0)
		playersMatrix.append(new)
	# Player starting coordinates:
	playersMatrix[0][0] = 0		# local_player_id
	playersMatrix[0][1] = 0		# global_player_id
	playersMatrix[0][2] = 100	# player_x
	playersMatrix[0][3] = 150	# player_y
	playersMatrix[0][4] = 0		# player_direction
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

	droplets_max = 20
	dropletsMatrix = [[0 for x in range(2)] for y in range(droplets_max)]
	# Droplets generation:
	for i in range(droplets_max):
		dropletsMatrix[i][0] = randint(0, 300)
		dropletsMatrix[i][1] = randint(0, 300)
		dropletsMatrix[i][1] = dropletsMatrix[i][1] * -1
	def dropletsMovement(self):
		for i in range(droplets_max):
			dropletsMatrix[i][1] = dropletsMatrix[i][1] + 1
			time.sleep(0.1) # dunno about time
	def dropletsRegen(self):
		for i in range(droplets_max):
			if dropletsMatrix[i][1] > 300:
				dropletsMatrix[i][1] = randint(0, 300)
				dropletsMatrix[i][1] = dropletsMatrix[i][1] * (-1)

	bullet_list = []
	for i in range (0, players_max):
		new = []
		for j in range (0, players_params):
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

	def bulletSSPCBuilder(self, bulletNumber):
		sspc = '1'
		sspc = sspc + str(bulletNumber)
		for j in range(6 - len(str(Main.bullet_list[int(bulletNumber)][0]))):
			sspc = sspc + '0'
		sspc = sspc + str(Main.bullet_list[int(bulletNumber)][0])
		for j in range(6 - len(str(Main.bullet_list[int(bulletNumber)][1]))):
			sspc = sspc + '0'
		sspc = sspc + str(Main.bullet_list[int(bulletNumber)][1]) # + str(Main.bullet_list[int(bulletNumber)][2])
		while len(sspc) != Main.package_lenght:
			sspc = sspc + '0'
		return sspc

	def bulletMovementThread(self, connection, client_address):
		with self.clients_lock:
			self.clients.add(connection)
			#for c in self.clients:
				#while True:
					#if len(Main.bullet_list) > 0:
						#for k in range(0, len(Main.bullet_list)):
							#c.sendall((self.bulletSSPCBuilder(k)).encode())

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

	def playersSSPCBuilder(self, player_id):
		sspc = '0' # Package code for player update
		sspc = sspc + str(player_id) # Check out README.MD file for "Server string package code" (sspc variable) structure info.
		for j in range(6 - len(str(Main.playersMatrix[int(player_id)][2]))):
			sspc = sspc + '0'
		sspc = sspc + str(Main.playersMatrix[int(player_id)][2])
		for j in range(6 - len(str(Main.playersMatrix[int(player_id)][3]))):
			sspc = sspc + '0'
		sspc = sspc + str(Main.playersMatrix[int(player_id)][3]) + str(Main.playersMatrix[int(player_id)][4])
		return sspc

	def clientMovementThread(self, connection, client_address):
		with self.clients_lock:
			self.clients.add(connection)
		try:
			while 1:
				data = connection.recv(4).decode()
				if data == 'updt': # client's update request while idling
					sspc = self.playersSSPCBuilder(0) + self.playersSSPCBuilder(1) + self.playersSSPCBuilder(2) + self.playersSSPCBuilder(3)
				else: # client's update request during action
					self.actionHandler(data)
				for c in self.clients:
					c.sendall(sspc.encode())
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
				Thread(target = self.clientMovementThread, args = (connection, client_address)).start()
				Thread(target = self.bulletMovementThread, args = (connection, client_address)).start()
				connection.sendall(str(Main.connectionNum).encode())
				Main.connectionNum = Main.connectionNum + 1

main = Main()
main.__init__()