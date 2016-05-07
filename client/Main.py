import socket
import pygame
import threading
from threading import Thread
import time
import json

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
	exit = False # gameloop boolean

	client_id = 0 # should be unique for each player
	players_max, players_params = 4, 5 # 0 - server number, 1 - player id, 2 - x, 3 - y
	playersMatrix = []
	for i in range (0, players_max):
		new = []
		for j in range (0, players_params):
			new.append(0)
		playersMatrix.append(new)

	if_move = 0
	player_dir = 0
	if_shoot = 0

	# variables init:
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
	
	bullet_list = []
	for i in range (0, 4):
		new = []
		for j in range (0, 3):
			new.append(0)
		bullet_list.append(new)
	def bulletsAdd(self, x, y, vector):
		Main.bullet_list.append([len(Main.bullet_list) + 1, [x, y, vector]])
	
	def reqUpdThread(self, sock): # request for update package
		while 1:
			time.sleep(0.01) # dunno if this sleep time is ok
			sock.sendall('updt'.encode())

	def getUpdThread(self, sock):
		while 1:
			responce = sock.recv(1024)
			#print(responce.decode())
			jsonResponse = json.loads(responce.decode())
			jsonData = jsonResponse["players_params"]
			for item in jsonData:
				Main.playersMatrix[item.get("local_id")][2] = item.get("coord_x")
				Main.playersMatrix[item.get("local_id")][3] = item.get("coord_y")
				Main.playersMatrix[item.get("local_id")][4] = item.get("direction")

	def eventListener(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			Main.if_move = 1
			Main.player_dir = 0
			self.sendpack()
		if keys[pygame.K_LEFT]:
			Main.if_move = 1
			Main.player_dir = 1
			self.sendpack()
		if keys[pygame.K_DOWN]:
			Main.if_move = 1
			Main.player_dir = 2
			self.sendpack()
		if keys[pygame.K_RIGHT]:
			Main.if_move = 1
			Main.player_dir = 3
			self.sendpack()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Main.exit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					Main.if_shoot = 1
					self.sendpack()
	def sendpack(self):
		Main.sock.sendall((str(Main.client_id) + str(Main.if_move) + str(Main.player_dir) + str(Main.if_shoot)).encode())
		Main.if_move = 0
		Main.if_shoot = 0
		
	def __init__(self):
		# On connection server data request (preload server data):
		client_id = Main.sock.recv(1).decode()
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
		print('GUI loaded.')
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