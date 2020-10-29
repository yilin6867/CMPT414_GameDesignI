#Globlin Tower Defense#
##Arthur: Yi Lin##
##Version: Alpha Game##

###Overview###
This project is a game that mimics the Bloon Tower Defense Game.
The goal of the game is to prevent any goblin from approaching the end of the course.

### Dependencies ###
Please install pygame through
`pip install pygame`

###Howe to Play###
Player can use mouse to select characters from the side navigator on the right to build defenses against approaching goblin.
	Please press an hold down the mouse to the select character and drag it to desire location.
	The transparent black circle is the attack range of the player. Please use it as a reference when placing the character
Player can release the mouse press to place the character
The character can only be placed in the plane outside of the road.
	Place character in the road and in select will be omitted
After placing characters in the desire area, the player can press the start button in the side navigator to start the game.
The goblin will spawn at the top right and start to move to the end of the course.
During the game, the player can click on the character to see the status of the character which is render in the side navigator.
	In the side navigator, the player can click release to remove the character and get a portion of the cost to hired the character.
During the game, the player can press the pause button in the side navigator to pause game.
	Player can press the pause button again to resume the game
During the game, the player can press the quit button in the side navigator to quit the game.
The windows X (exit) button will not exit the game. It is temparily a restart button.

### Bugs to fix ###
Prevent the character being place overlapping into the road
Fix the logic of how the Globlin move so it would not seem as it move slightly towards left in the road

### Features plan to Add or Complete ###
Add more characters and goblins into the game
Allow the character to self upgrade based on the number of goblin it defeat.
