
class Interpreter:
	
	def __init__(self, game, player):
		self.game = game # Could access this through player, but I don't think this clutters the variable space too much
		self.player = player
	
	def interpret(self, order):
		code, subcode, param = order
		# Notably, the returned value is unpacked into message.send(), so a list must be returned, that can be a variable length of parametres
		
		if code == 40:
			self.player.name = param[0]
			return [0]
		
		if code == 50:
			if subcode == 0:
				result = self.game.sendMessage(self.player, int(param[0]), param[1])
				return [result]
		
		if code == 60:
			return self.create(subcode, param)
	
	def create(self, subcode, param):
		
		game = self.game
		player = self.player
		
		if subcode == 0: # Land
			print str(player), "creating land with", param
			response = player.createLand(param[0], int(param[1]), int(param[2]), param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			return [response] # Maybe should be moved left one indent, so everything returns a response code?

