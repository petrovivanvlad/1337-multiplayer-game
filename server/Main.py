import socket
import sys
import threading
import thread
from threading import Thread
from thread import *
from random import randint
import time

class Main:
	# technical:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = 'localhost'
	port = 54416
	serveraddress = (host, port)
	sock.bind(serveraddress)
	sock.listen(4)

	clients = set()
	clients_lock = threading.Lock()
	connectionNum = 0

	# game:
	players_max, players_params = 4, 5 # 0 - server number, 1 - player id, 2 - x, 3 - y
	playersMatrix = [[0 for x in range(players_params)] for y in range(players_max)]
	droplets_max = 20
	dropletsMatrix = [[0 for x in range(2)] for y in range(droplets_max)]
	for i in range(droplets_max):
		dropletsMatrix[i][0] = randint(0, 300)
		dropletsMatrix[i][1] = randint(0, 300)
		dropletsMatrix[i][1] = dropletsMatrix[i][1] * -1

	# Player starting coordinates:
	playersMatrix[0][0] = 0 # local_player_id
	playersMatrix[0][1] = 0 # global_player_id
	playersMatrix[0][2] = 100 # player_x
	playersMatrix[0][3] = 150 # player_y
	playersMatrix[0][4] = 0 # player_direction
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

	def dropletsMovement(self):
		for i in range(droplets_max):
			dropletsMatrix[i][1] = dropletsMatrix[i][1] + 1
			time.sleep(0.1) # dunno about time
	def dropletsRegen(self):
		for i in range(droplets_max):
			if dropletsMatrix[i][1] > 300:
				dropletsMatrix[i][1] = randint(0, -300)

	def actionHandler(self, data):
		i = int(data[0]) # Player identificator
		# Player walk:
		if data[1:3] == '00':
			Main.playersMatrix[i][3] = Main.playersMatrix[i][3] - 3
		if data[1:3] == '11':
			Main.playersMatrix[i][2] = Main.playersMatrix[i][2] - 3
		if data[1:3] == '12':
			Main.playersMatrix[i][3] = Main.playersMatrix[i][3] + 3
		if data[1:3] == '03':
			Main.playersMatrix[i][2] = Main.playersMatrix[i][2] + 3

	def playersMatrixBuild(self, player_ident):
		tempstr = str(player_ident)
		for j in range(6 - len(str(Main.playersMatrix[int(player_ident)][2]))):
			tempstr = tempstr + '0'
		tempstr = tempstr + str(Main.playersMatrix[int(player_ident)][2])
		for j in range(6 - len(str(Main.playersMatrix[int(player_ident)][3]))):
			tempstr = tempstr + '0'
		tempstr = tempstr + str(Main.playersMatrix[int(player_ident)][3])
		return tempstr

	def clientThread(self, connection, client_address):
		with self.clients_lock:
			self.clients.add(connection)
		try:
			while 1:
				data = connection.recv(3)
				if data == 'upd':
					# Read README file for tempstr structure info.
					tempstr = self.playersMatrixBuild(0) + self.playersMatrixBuild(1) + self.playersMatrixBuild(2) + self.playersMatrixBuild(3)
				else:
					self.actionHandler(data)
				with self.clients_lock:
					for c in self.clients:
						c.sendall(tempstr)
		finally:
			with self.clients_lock:
				print 'No more data from ', client_address
				Main.connectionNum = Main.connectionNum - 1
				self.clients.remove(connection)
				connection.close()

	def __init__(self):
		print 'Server created.'
		# Main loop:
		while 1:
			if Main.connectionNum < 5:
				connection, client_address = Main.sock.accept()
				print 'Client connected from ', client_address
				start_new_thread(self.clientThread, (connection, client_address))
				connection.sendall(str(Main.connectionNum))
				Main.connectionNum = Main.connectionNum + 1

main = Main()
main.__init__()