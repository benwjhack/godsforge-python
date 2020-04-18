
import map
import interpreter
import util.functions

LAND_COST = 1.0
GENERATOR_COST = 4.0
RACE_COST = 0.0

class Player:
	
	def __init__(self, game, uid, secret, domain, subdomain1, subdomain2, uber=False):
		self.game = game
		if uid == None:
			uid = game.generateUID(self)
		self.secret = secret
		self.UID = uid
		self.id = game.map.generateID(self)
		self.name = "Anonymous"
		self.messages = []
		self.baseDP = {'generic': 4, domain: 4, subdomain1: 1, subdomain2: 1}
		self.currentDP = {'generic': 0, domain: 0, subdomain1: 0, subdomain2: 0}
		self.domainNames = [domain, subdomain1, subdomain2]
		self.gameIndex = -1
		self.owned = []
		
		if not uber:
			game.addPlayer(self)
		else:
			self.children = [] # List so that uber player can be parent of races...
			game.players.append(self)
			self.baseDP = self.currentDP = {'generic': float("inf")}
			self.domainNames = ["generic", "generic", "generic"]
			self.name = "Game Master"
		self.uber = uber
		
		self.orders = []
		
		self.interpreter = interpreter.Interpreter(game, self)
		self.interpret = self.interpreter.interpret
	
	def message(self, message):
		self.messages.append(message)
	
	def initCycle(self):
		self.currentDP = self.baseDP.copy()
		self.orders = []
	
	def getDPGeneration(self):
		return sum([self.currentDP[name] for name in ["generic"]+self.domainNames]) # TODO: add 'controlled' stuffs' DP
	
	def getCurrentDP(self):
		return [self.currentDP[name] for name in ["generic"]+self.domainNames]
	
	def __spend__(self, dpType, amount, modifiers):
		if not dpType in self.currentDP or self.currentDP[dpType] < amount:
			return [3, 0, ["Not enough DP - you need %s" % amount]]
		self.currentDP[dpType] -= amount
		return 0
	
	def createLand(self, dpType, x, y, description, id=None):
		if sum([entity.type == "Land" for entity in self.game.map.getTile(x,y).children]) > 0: # If the tile already has a land
			return [3, 0, ["There is already Land on this tile"]]
		spendAttempt = self.__spend__(dpType, LAND_COST, [])
		if spendAttempt:
			return spendAttempt
		id = map.Land(self.game.map, self, self.game.map.getTile(x,y), LAND_COST, [], description).id
		return [0, 0, [id]]
	
	def createGenerator(self, dpType, parent, description, id=None):
		spendAttempt = self.__spend__(dpType, GENERATOR_COST, [])
		if spendAttempt:
			return spendAttempt
		id = map.Generator(self.game.map, self, parent, GENERATOR_COST, [], description, dpType).id
		return [0, 0, [id]]
	
	def createRace(self, dpType, description, controlType, id=None):
		modifiers = ["autonomous" if controlType else "controlled"]
		spendAttempt = self.__spend__(dpType, RACE_COST, modifiers)
		if spendAttempt:
			return spendAttempt
		id = map.Race(self.game.map, self, self.game.masterPlayer, controlType, RACE_COST, modifiers, description).id
		return [0, 0, [id]]
	
	def createCreature(self, dpType, dpAmount, parent, race, description, id=None):
		modifiers = ["autonomous" if race.controlType else "controlled"]
		spendAttempt = self.__spend__(dpType, dpAmount, modifiers)
		if spendAttempt:
			return spendAttempt
		id = map.Creature(self.game.map, self, parent, race, dpAmount, modifiers, description).id
		return [0, 0, [id]]
	
	def createFortification(self, dpType, dpAmount, parent, description, id=None):
		spendAttempt = self.__spend__(dpType, dpAmount, modifiers)
		if spendAttempt:
			return spendAttempt
		id = map.Fortification(self.game.map, self, parent, dpAmount, modifiers, description).id
		return [0, 0, [id]]
	
	def createEquipment(self, dpType, dpAmount, parent, description, id=None):
		spendAttempt = self.__spend__(dpType, dpAmount, [])
		if spendAttempt:
			return spendAttempt
		id = map.Equipment(self.game.map, self, parent, dpAmount, [], description).id
		return [0, 0, [id]]
	
	def createLegend(self, dpType, dpAmount, parent, description, id=None):
		spendAttempt = self.__spend__(dpType, dpAmount, [])
		if spendAttempt:
			return spendAttempt
		id = map.Legend(self.game.map, self, parent, dpAmount, [], description).id
		return [0, 0, [id]]
	
	def createParagon(self, dpType, dpAmount, parent, description, id=None):
		spendAttempt = self.__spend__(dpType, dpAmount, [])
		if spendAttempt:
			return spendAttempt
		id = map.Paragon(self.game.map, self, parent, dpAmount, [], description).id
		return [0, 0, [id]]
	
	def addOrder(self, order):
		self.orders.append(order)
	
	def load(self):
		pass
	
	def save(self):
		pass
	
	def __str__(self):
		# Maybe players shouldn't be uniquely identifiable (idk yet if UID's can be re-assigned once out of use)
		return "%s (%s) (%s)" % (self.name, self.UID, self.id)
	
	def __order__(self, *args):
		return [3, 0, ["This is a player..."]]
	
	def getOwnedArray(self, target=None):
		if not target: target = self
		return [target] + util.functions.foldr(util.functions.add, [], [self.getOwnedArray(thing) for thing in target.owned])
	
	def preCycle(self):
		pass
