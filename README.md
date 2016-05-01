# 1337-multiplayer-game
real-time socket mega fun arcade
#######################################
#######################################
# Player Matrix:
#######################################
	L_ID	G_ID	COORDX	COORDY	DIR

	0		5433	000150	000150	3
	1		3452	000150	000150	3
	2		3245	000150	000150	3
	3		3453	000150	000150	3
#######################################
#	Player update Server String Package Code (sspc):
	
	Legend:
			C - Package code
			L - Local ID
			G - Global ID
			X - Coordinate X
			Y - Coordinate Y
			D - Direction

	Examples for each player:
		"CLXXXXXXYYYYYYD"
	1.	"000001110002221"
	2.	"010010190005553"
	3.	"020000330002213"
	4.	"030000010000222"
	
	SSCP full package example:
		CLXXXXXXYYYYYYDCLXXXXXXYYYYYYDCLXXXXXXYYYYYYDCLXXXXXXYYYYYYD
		000001110002221010010190005553020000330002213030000010000222
	TODO:	"LGGGGXXXXXXYYYYYYDDD"
#######################################
#	Client update Client String Package Code:

	Legend:	
			L - Local ID
			M - If move
			D - Direction
			S - If shoot

	Examples:
		"LMDS"
	1.	"0100"
	2.	"1111"
#######################################
#	Directory index codes (TODO: change to 360 with mouse observe):

	0 - UP
	1 - LEFT
	2 - DOWN
	3 - RIGHT
#######################################
#######################################
# Bullet Matrix:
	Bullet update Server String Package Code:
	
	Legend:
			C - Package Code
			N - Number ID
			X - Coordinate X
			Y - Coordinate Y
			D - Direction vector

	Examples:
		"CNXXXXXXYYYYYYD"
	1.	"100001110002221"
	2.	"110010190004353"

#######################################
