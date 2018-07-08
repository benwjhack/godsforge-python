
import map
import interpreter

LAND_COST = 1

class Player:
	
	def __init__(self, game, uid, secret, domain, subdomain1, subdomain2):
		self.game = game
		if uid == None:
			uid = game.generateUID()
		self.secret = secret
		self.UID = uid
		self.name = "Anonymous"
		self.messages = []
		self.baseDP = {'generic': 4, domain: 4, subdomain1: 1, subdomain2: 1}
		self.currentDP = {'generic': 0, domain: 0, subdomain1: 0, subdomain2: 0}
		self.domainNames = [domain, subdomain1, subdomain2]
		self.gameIndex = -1
		
		game.addPlayer(self)
		
		self.orders = []
		
		self.interpreter = interpreter.Interpreter(game, self)
		self.interpret = self.interpreter.interpret
	
	def message(self, message):
		self.messages.append(message)
	
	def initCycle(self):
		self.currentDP = self.baseDP.copy()
		self.orders = []
	
	def getDPGeneration(self):
		# Possible bug- this assumes order generic, domain, subdomain1, subdomain2 is preserved (same for getCurrentDP() )
		return sum(self.baseDP.values()) # TODO: add 'controlled' stuffs' DP
	
	def getCurrentDP(self):
		return self.currentDP.values()
	
	def createLand(self, dpType, x, y, description):
		if self.currentDP[dpType] < LAND_COST:
			return 1
		self.currentDP[dpType] -= LAND_COST
		map.Land(self.game.map, self, self.game.map.getTile(x,y), LAND_COST, [], description)
		return 0
	
	def addOrder(self, order):
		self.orders.append(order)
	
	def load(self):
		pass
	
	def save(self):
		pass
	
	def __str__(self):
		# Maybe players shouldn't be uniquely identifiable (idk yet if UID's can be re-assigned once out of use)
		return "%s (%s)" % (self.name, self.UID)
