
from util.sockets import ServerSocket
from util.message import Message
import threading
from handler import handle
import os
from game import Game

SAVEFILE = "game.save"

print "Checking for savefile..."

game = None

if os.path.isfile(SAVEFILE):
	# Do some loading stuff
	pass
else:
	game = Game()
	game.initGame()


print "Starting server..."

socket = ServerSocket('localhost', 5050)

try:
	while 1:
		client = socket.getClientObject()
		t = threading.Thread(target=handle, args=(client,game))
		t.daemon = True
		t.start()
except KeyboardInterrupt:
	# Exiting normally wouldn't end attached daemon threads, hence we force a brutal system module exit to make sure the death is at least clean.
	import sys
	sys.exit(0)

