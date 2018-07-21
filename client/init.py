
from util.sockets import ClientSocket
from util.message import Message

sock = ClientSocket('localhost', 5050)
message = Message(sock)

loginB = "l" in raw_input("(L)ogin or (R)egister?").lower()

domain = None
subdomain1 = None
subdomain2 = None

if loginB:
	# Do login stuff
	secret = raw_input("Enter your secret:")
	message.send(10, 0, [secret])
	response = message.get()
	if response["code"] == 2:
		print "INVALID SECRET"
		import sys
		sys.exit(1)
	message.send(21, 1)
	response = message.get()
	domain = response["param"][0]
	subdomain1 = response["param"][1]
	subdomain2 = response["param"][2]
else:
	secret = raw_input("Enter a secret (like a password, but no security):")
	domain = raw_input("Enter a domain:")
	subdomain1 = raw_input("Enter a subdomain:")
	subdomain2 = raw_input("Enter a subdomain:")
	message.send(11, 0, [secret, domain, subdomain1, subdomain2])
	response = message.get()
	if response["code"] == 3:
		print response["param"][0]
		import sys
		sys.exit(1)

print "Login successful!\n\n"
print "Type a command, or 'help' to get information on commands"

# Ideally each order would call a single function, as some orders require others- but for now I can't be bothered for ones I haven't yet copied

toggleDelay = False

def sendMessage(code, subcode=0, param=[]):
	global message, toggleDelay
	if toggleDelay and code >= 40 and code < 100:
		message.send(70, 0, [code, subcode]+param)
	else:
		message.send(code, subcode, param)

def gameStarted():
	global message
	sendMessage(20, 4)
	return message.get()["param"][0] == "True"

while 1:
	order = raw_input().split(" ")
	command = order[0].lower()
	if "help" in command:
		print "idk"
	elif "cycle" in command:
		sendMessage(20, 1)
		print "It is Cycle %s" % (message.get()["param"][0])
	elif "started" in command:
		started = gameStarted()
		print "The game has" + (" " if started else " not ") + "started"
	elif "player" in command:
		sendMessage(20, 3)
		print "\n".join(message.get()["param"])
	elif "vote" in command:
		sendMessage(30, int("yes" in "".join(order)))
		message.get()
	elif "raw" in command:
		inp = raw_input().split(" ")
		sendMessage(int(inp[0]), int(inp[1]), inp[2:])
		print message.get()
	elif "name" in command:
		inp = raw_input("Enter your new name:")
		sendMessage(40, 0, [inp])
		if message.get()["code"] == 0:
			print "Successful!"
		else:
			print "Failed?"
	elif "messages" in command:
		sendMessage(51)
		print "\n".join(message.get()["param"])
	elif "message" in command:
		to = raw_input("Enter the UID of the entity you want to message:")
		if sum([not c in "0123456" for c in to]):
			print "Not a valid UID"
		content = raw_input("Enter the message you want to send:")
		sendMessage(50, 0, [to, content])
		message.get()
	elif "tiles" in command:
		sendMessage(20, 0)
		response = message.get()
		print response["param"]
		print "\n\n".join(response["param"])
	elif "story" in command:
		sendMessage(20, 6)
		response = message.get()
		print response["param"][0]
	elif "tile" in command:
		x = raw_input("x: ")
		y = raw_input("y: ")
		sendMessage(20, 5, [x, y])
		print message.get()["param"][0]
	elif "currentdp" in command:
		# Errors occur if a player has the same name for multiple domains- they derserve this.
		if not gameStarted():
			print "Game not started, cannot check."
			continue
		sendMessage(21, 3)
		response = message.get()["param"]
		print "You currently have %s generic, %s %s, %s %s, and %s %s DP" % (response[0], response[1], domain, response[2], subdomain1, response[3], subdomain2)
	elif "dp" in command:
		sendMessage(21, 0)
		response = message.get()
		params = (response["param"][0], response["param"][1], domain, response["param"][2], subdomain1, response["param"][3], subdomain2)
		print "You generate %s generic, %s %s domain, %s %s domain, and %s %s domain DP per cycle" % params
	elif "domain" in command:
		sendMessage(21, 1)
		response = message.get()
		print "Your greater domain is %s, and your subdomains are %s and %s" % tuple(response["param"])
	elif "exit" in command or "stop" in command or "quit" in command:
		sendMessage(1)
		message.socket.close()
		break
	elif "create" in command:
		sendMessage(20, 4)
		if message.get()["param"][0] == "False":
			print "Game has not started: stop"
			continue
		category = raw_input("Input what you would like to create: ").lower()
		if "land" in category:
			dpType = raw_input("Enter the type of dp you would like to spend: ").lower()
			if not dpType in ["generic", domain, subdomain1, subdomain2]:
				print "invalid domain type, try again"
				continue
			x = raw_input("x: ")
			y = raw_input("y: ")
			description = raw_input("Description (to be added in land description: ")
			story = raw_input("Summary (to be added to list of events): ")
			sendMessage(60, 0, [dpType, x, y, description, story])
		response = message.get()
		if response["code"] == 0:
			print "Success!"
		else:
			print "Failure..."
	elif "delay" in command:
		toggleDelay = not toggleDelay
	else:
		print "Unrecognised command: try again, or try 'help'"
		continue
	print ""

#Do cleanup (but I guess there won't ever be any?)
