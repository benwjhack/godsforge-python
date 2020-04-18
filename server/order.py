

class Order:
	
	def __init__(self, player, code, subcode, param):
		self.player = player
		self.game = self.player.game
		self.interpreter = player.interpreter
		self.code = code
		self.subcode = subcode
		self.param = param
		self.delayed = False
	
	def setDelayed(self):
		self.reservedID = self.game.map.reserveID()
		self.delayed = True
	
