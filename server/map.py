
import util.id

class Map:
	
	def __init__(self, game):
		self.game = game
		self.tiles = []
		self.IDcounter = 0
	
	def initTiles(self, minX, maxX, minY, maxY):
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		for x in xrange(minX, maxX+1):
			for y in xrange(minY, maxY+1):
				tile = Tile(self, x, y)
				self.tiles.append(tile)
	
	def generateID(self):
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

class Tile:
	
	def __init__(self, map, x, y):
		self.map = map
		self.children = []
		self.location = (x,y)
	
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

class Entity(object):
	
	def __init__(self, type, map, owner, parent, basedp, modifiers, description):
		self.map = map
		self.uid = map.game.generateUID()
		self.id = map.generateID()
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
		
		self.type = type #self.__class__.__bases__[0].__name__
		
		self.description = description
	
	def __str__(self):
		return "%s: %sdp %s; %s" % (self.type, self.effectivedp, self.location, self.description)

class Land(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Land, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
	

class Generator(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Generator, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
