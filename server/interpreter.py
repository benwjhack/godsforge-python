
class Interpreter:
	
	def __init__(self, game, player):
		self.game = game # Could access this through player, but I don't think this clutters the variable space too much
		self.player = player
	
	def interpret(self, order):
		code, subcode, param = order
		code = code % 10 # So as to disregard whether in block 70 or 80 - possible alternative if refactoring, as orders are stored, change the order code to the correct block (allows more versatile mapping)
		if code == 0:
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
			# Maybe include possibility for params as well? In case of error message?
			return response # Maybe should be moved left one indent, so everything returns a response code?

