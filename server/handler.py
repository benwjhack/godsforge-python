
import util.message
from player import Player

def handle(sock, game):
	
	print "Starting player thread handle..."
	
	message = util.message.Message(sock)
	
	loginM = message.get()
	loginB = loginM["code"] == 10
	
	selectedPlayer = None
	if loginB:
		# Do login stuff
		selectedPlayer = game.getPlayer(loginM["param"][0])
		if not selectedPlayer:
			message.send(2)
			print "Player entered inavlid secret, killing thread..."
			return
		message.send(0)
	else:
		if game.closed:
			message.send(3, 0, ["Game closed- cannot join"])
			return
		
		selectedPlayer = Player(game, None, *loginM["param"])
		message.send(0)
		
		print "Registered player!"
	
	while 1:
		
		messageO = message.get()
		code = messageO["code"]
		subcode = messageO["subcode"]
		param = messageO["param"]
		
		if code == 1:
			break
		
		if code == 20:
			if subcode == 0:
				tiles = [str(tile) for tile in game.map.tiles]
				message.send(0, 0, tiles)
			if subcode == 1:
				message.send(0, 0, [game.cycle])
			if subcode == 3:
				message.send(0, 0, [str(player) for player in game.players])
			if subcode == 4:
				message.send(0, 0, [game.closed])
			if subcode == 5:
				message.send(0, 0, [str( game.map.getTile( int( param[0] ), int( param[1] ) ))])
			if subcode == 6:
				message.send(0, 0, [game.story])
		
		if code == 21:
			if subcode == 0:
				message.send(0, 0, [selectedPlayer.baseDP["generic"], selectedPlayer.baseDP[selectedPlayer.domainNames[0]], selectedPlayer.baseDP[selectedPlayer.domainNames[1]], selectedPlayer.baseDP[selectedPlayer.domainNames[2]]])
			if subcode == 1:
				message.send(0, 0, selectedPlayer.domainNames)
			if subcode == 3:
				message.send(0, 0, selectedPlayer.getCurrentDP())
			if subcode == 4:
				message.send(0, 0, [str(message1) for message1 in selectedPlayer.messages])
		
		if code == 30:
			game.vote(selectedPlayer, subcode)
			message.send(0)
		
		if code >= 40 and code < 70:
			response = selectedPlayer.interpreter.interpret([code, subcode, param])
			message.send(*response)
		
		if code == 70:
			game.addOrder(selectedPlayer, [int(param[0]), int(param[1]), param[2:]])
			message.send(0)
		
		if code == 100:
			#continue
			if subcode == 0:
				game.startGame()
			if subcode == 1:
				game.advanceCycle()
			if subcode == 2:
				result = eval(''.join(param))
				message.send(0, 0, [result])
				continue
			if subcode == 3:
				game.save()
			message.send(0)
	
	# Do cleanup
	
	print "Ending player thread handle..."


