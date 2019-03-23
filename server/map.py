import player

class Map:
	
	def __init__(self, game):
		self.game = game
		self.tiles = []
		self.IDcounter = 0
		self.entities = []
	
	def initTiles(self, minX, maxX, minY, maxY):
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		for x in xrange(minX, maxX+1):
			for y in xrange(minY, maxY+1):
				tile = Tile(self, x, y)
				self.tiles.append(tile)
	
	def generateID(self, thing):
		self.entities.append(thing)
		temp = self.IDcounter
		self.IDcounter += 1
		return temp
	
	def getTile(self, x, y):
		if x < self.minX or x > self.maxX or y < self.minY or y > self.maxX:
			return 1
		for tile in self.tiles:
			if tile.location[0] == x and tile.location[1] == y:
				return tile
		return 1
	
	def getEntity(self, id):
		for entity in self.entities:
			if entity.id == id:
				return entity
		return None

class Tile:
	
	def __init__(self, map, x, y):
		self.map = map
		self.children = []
		self.location = (x,y)
		self.id = map.generateID(self)
	
	def adjacentTiles(self):
		locations = []
		location = self.location
		locations.append((location[0]+1, location[1]))
		locations.append((location[0]-1, location[1]))
		locations.append((location[0], location[1]+1))
		locations.append((location[0], location[1]-1))
		return locations
	
	def __str__(self):
		return ("%s:\n" % (self.location,)) + '\n'.join( [str(child) for child in self.children] )
	
	def _getName(self):
		return str(self.location)
	
	def initCycle(self):
		pass
	
	def message(self, string):
		pass

class Entity(object):
	
	def __init__(self, type, map, owner, parent, basedp, modifiers, description):
		self.map = map
		self.game = map.game
		self.UID = map.game.generateUID(self)
		self.id = map.generateID(self)
		self.children = []
		self.parent = parent
		self.parent.children.append(self)
		
		self.location = self.parent.location
		self.owner = owner
		self.acceptOrders = [owner]
		self.sayOwner = [owner for player in map.game.players] # Unique order preserved by game object player arrray
		
		self.basedp = basedp
		self.modifiers = modifiers
		
		self.effectivedp = basedp
		
		self.type = type
		
		self.description = description
		self.name = self.type+str(self.id)
		
		self.currentDP = {}
	
	def __order__(self, orderer, subcode, params):
		if self.owner != orderer:
			return [3, 0, ["You don't own this entity"]] # Eventually, this needs to be more subtle
		if subcode == 0: # Transfer DP
			dpType = params[0]
			amount = int(params[1])
			if not dpType in self.currentDP or self.currentDP[dpType] < amount:
				return [3, 0, ["Not enough DP to transfer"]]
			entity = self.map.getEntity(int(params[2]))
			if not entity:
				return [3, 0, ["No such entity to transfer DP to"]]
			self.currentDP[dpType] -= amount
			entity.currentDP[dpType] += amount
			return [0]
		if subcode == 1: # Tell current DP
			self.game.sendMessage(self, self.owner.UID, "I have the following DP:" + str(self.currentDP))
			return [0]
		if subcode == 2: # Change name
			self.name = params[0]
			return [0]
	
	def _getName(self):
		return self.name
	
	def __str__(self):
		return self._indent_print(0)
	
	def _indent_print(self, indent):
		string = "\n"+("\t"*indent)+"%s %s (%s): %sdp %s; %s" % (self.type, self.name, self.id, self.effectivedp, self.parent._getName(), self.description)
		for child in self.children:
			string += child._indent_print(indent+1)
		return string
	
	def initCycle(self):
		pass
	
	def message(self, message):
		self.owner.message(message)

class Land(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Land, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.name = "Land (%s, %s)" % parent.location
	

class Generator(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description, dpType):
		super(Generator, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.dpType = dpType
	
	def initCycle(self):
		self.currentDP[self.dpType] = self.currentDP.setdefault(self.dpType, 0) + self.effectivedp / player.GENERATOR_COST

class Race(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Race, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		map.game.races.append(self)
		self.trouble = 0
	
	def _indent_print(self, indent):
		string = "\n"+("\t"*indent)+"%s %s (%s); %s" % (self.type, self.name, self.id, self.description)
		for child in self.children:
			string += child._indent_print(indent+1)
		return string

class Creature(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Creature, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
