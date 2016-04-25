import socket
import pygame
import threading
import thread
from threading import Thread
from thread import *
import time

class Player_rect(pygame.sprite.Sprite): 
	def __init__(self, color, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()

class Main:
	# technical:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = 'localhost'
	port = 54416
	serveraddress = (host, port)
	sock.connect(serveraddress)
	
	# game:
	players_max, players_params = 4, 5 # 0 - server number, 1 - player id, 2 - x, 3 - y
	playersMatrix = [[0 for x in range(players_params)] for y in range(players_max)]
	client_id = 0 # should be unique for each player
	droplets_max = 20
	dropletsMatrix = [[0 for x in range(droplets_max)] for y in range(2)]
	exit = False # gameloop boolean
	# start coords:	 
	playersMatrix[0][0] = 0		# local_player_id
	playersMatrix[0][1] = 0		# global_player_id
	playersMatrix[0][2] = 0		# player_x
	playersMatrix[0][3] = 0		# player_y
	playersMatrix[0][4] = 0		# player_direction
	playersMatrix[1][0] = 1
	playersMatrix[1][1] = 0
	playersMatrix[1][2] = 0
	playersMatrix[1][3] = 0
	playersMatrix[0][4] = 0
	playersMatrix[2][0] = 2
	playersMatrix[2][1] = 0
	playersMatrix[2][2] = 0
	playersMatrix[2][3] = 0
	playersMatrix[0][4] = 0
	playersMatrix[3][0] = 3
	playersMatrix[3][1] = 0
	playersMatrix[3][2] = 0
	playersMatrix[3][3] = 0
	playersMatrix[0][4] = 0

	def reqUpdThread(self, sock): # request for update package
		while 1:
			time.sleep(0.01) # dunno if this sleep time is ok
			sock.sendall('upd')

	def getUpdThread(self, sock):
		upd_package = 0
		upd_package_lenght = 52 # size of update package (string)
		while 1:
			data = sock.recv(upd_package_lenght)
			while upd_package < upd_package_lenght:
				upd_package += len(data)
			Main.playersMatrix[0][2] = int(data[1:7])
			Main.playersMatrix[0][3] = int(data[7:13])
			Main.playersMatrix[1][2] = int(data[14:20])
			Main.playersMatrix[1][3] = int(data[20:26])
			Main.playersMatrix[2][2] = int(data[27:33])
			Main.playersMatrix[2][3] = int(data[33:39])
			Main.playersMatrix[3][2] = int(data[40:46])
			Main.playersMatrix[3][3] = int(data[46:52])

	def eventListener(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Main.exit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					Main.sock.sendall(str(Main.client_id) + '00') # change to socket.send() ?
				if event.key == pygame.K_LEFT:
					Main.sock.sendall(str(Main.client_id) + '11')
				if event.key == pygame.K_DOWN:
					Main.sock.sendall(str(Main.client_id) + '12')
				if event.key == pygame.K_RIGHT:
					Main.sock.sendall(str(Main.client_id) + '03')

	def __init__(self):
		# On connection server data request (preload server data):
		client_id = Main.sock.recv(1)
		Main.client_id = client_id

		t1 = Thread(target = self.reqUpdThread, args = (Main.sock, ))
		t2 = Thread(target = self.getUpdThread, args = (Main.sock, ))
		t1.start()
		t2.start()

		# Pygame init:
		# Colors:
		BLACK  = (  0,   0,   0)
		WHITE  = (255, 255, 255)
		RED    = (255,   0,   0)
		GREEN  = (  0, 255,   0)
		BLUE   = (  0,   0, 255)
		YELLOW = (  0, 255, 255)
		# Player sprites:
		all_sprites_list = pygame.sprite.Group()
		player0 = Player_rect(   RED, 20, 15)
		player1 = Player_rect( GREEN, 20, 15)
		player2 = Player_rect(  BLUE, 20, 15)
		player3 = Player_rect(YELLOW, 20, 15)
		all_sprites_list.add(player0)
		all_sprites_list.add(player1)
		all_sprites_list.add(player2)
		all_sprites_list.add(player3)
		# Window:
		screenSize = (300, 300)
		screen = pygame.display.set_mode(screenSize)
		pygame.display.set_caption('1337 game')
		pygame.init()
		print 'GUI loaded.'
		clock = pygame.time.Clock()

		# Main loop:
		while not Main.exit:
			self.eventListener()
			# Graphics:
			screen.fill(WHITE)
			player0.rect.x = Main.playersMatrix[0][2]
			player0.rect.y = Main.playersMatrix[0][3]
			player1.rect.x = Main.playersMatrix[1][2]
			player1.rect.y = Main.playersMatrix[1][3]
			player2.rect.x = Main.playersMatrix[2][2]
			player2.rect.y = Main.playersMatrix[2][3]
			player3.rect.x = Main.playersMatrix[3][2]
			player3.rect.y = Main.playersMatrix[3][3]
			all_sprites_list.draw(screen)
			pygame.display.flip()
			clock.tick(60)
		pygame.quit()

main = Main()
main.__init__()