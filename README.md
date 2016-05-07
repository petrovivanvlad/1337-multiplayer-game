# 1337-multiplayer-game
real-time socket mega fun arcade
#######################################
#######################################
# Player Matrix:

	Example:
		L_ID	G_ID	X		Y		DIR
		0		5433	150		150		3
		1		3452	150		150		3
		2		3245	150		150		3
		3		3453	150		150		3
#######################################
#	Client update Client String Package Code (cspc) [TODO: move to json???]:

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
#	Directory index codes [TODO: change to 360 with mouse observe]:

	0 - UP
	1 - LEFT
	2 - DOWN
	3 - RIGHT