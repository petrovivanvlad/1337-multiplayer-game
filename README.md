# 1337-multiplayer-game
real-time socket mega fun arcade
#######################################
#######################################
# Player Matrix:
#######################################
#	Legend:
		L_ID	G_ID	COORDX	COORDY	DIR

	Example:
		0		5433	000150	000150	3
		1		3452	000150	000150	3
		2		3245	000150	000150	3
		3		3453	000150	000150	3
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