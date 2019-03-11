
from util.sockets import ServerSocket
from util.message import Message
from handler import handle
from game import Game
import loader
import threading

print "Checking for savefile..."

game = None

if loader.isSaveFile():
	print "Loading file..."
	game = loader.load()
	game.onLoad()
else:
	print "Creating new game..."
	game = Game()
	game.initGame()


print "Starting server..."

SERVER = "localhost"
PORT = 5050

socket = ServerSocket(SERVER, PORT)

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

