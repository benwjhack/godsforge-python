import player
import util.functions, util.imperative

class Map(object):
	
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
	
	def getLocationArray(self, target):
		return [target] + util.functions.foldr(util.functions.add, [], [self.getLocationArray(thing) for thing in target.children])
	
	def move(self, target, dest):
		def doMove():
			target.parent.children.remove(target)
			target.parent = dest
			target.parent.children.append(target)
		def doMove2():
			target.parent.children.remove(target)
			target.parent = dest.parent
			target.parent.children.append(target)
		if type(target.parent) == Tile:
			if dest == target.parent: return 0
			if type(dest) == Tile:
				if not target.moveActions > 0 or not dest in target.parent.adjacent():
					return 1
				target.moveActions -= 1
				doMove()
			else:
				if not dest in target.parent.children:
					return 1
				doMove()
		else:
			if dest == target.parent:
				doMove2()
			elif dest in target.children: # this is slightly dubious
				temp = target.parent
				doMove2()
				dest.parent = temp
			else:
				return 1
		fights = []
		for entity in target.parent:
			if entity.isHostileTo(target):
				fights.append(self.game.fight(target, entity))
		return (fights if fights else 0)

class Tile(object):
	
	def __init__(self, map, x, y):
		self.map = map
		self.children = []
		self.location = (x,y)
		self.id = map.generateID(self)
		self.type = Tile
	
	def adjacentTiles(self):
		locations = []
		location = self.location
		locations.append((location[0]+1, location[1]))
		locations.append((location[0]-1, location[1]))
		locations.append((location[0], location[1]+1))
		locations.append((location[0], location[1]-1))
		return util.functions.shuffled(locations)
	
	def adjacent(self):
		return filter(lambda x : x != 1, [self.map.getTile(*location) for location in self.adjacentTiles()]) + self.children
	
	def __str__(self):
		return ("%s (%s):" % (self.location,self.id)) + '\n'.join( [child._indent_print(1) for child in self.children] )
	
	def _getName(self):
		return str(self.location)
	
	def initCycle(self):
		pass
	
	def message(self, string):
		pass
	
	def __order__(self, *args):
		return [3, 0, ["This is a tile..."]]
	
	def preCycle(self):
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
		
		self.owner = owner
		self.owner.owned.append(self)
		self.owned = []
		
		self.acceptOrders = [owner]
		self.sayOwner = [owner for player in map.game.players] # Unique order preserved by game object player arrray
		
		self.basedp = basedp
		self.modifiers = modifiers
		
		self.effectivedp = cost(basedp, modifiers)
		
		self.type = type
		
		self.description = description
		self.name = self.type+str(self.id)
		
		self.currentDP = {}
		self.moveSpeed = 0
		self.moveActions = self.moveSpeed
		
		self.defaultHostile = False
		self.hostileExceptions = []
		
		self.living = 0.0
		self.sustain = 0
		self.currentSustain = 0
	
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
		if subcode == 3: # Calculate fight strength
			return [0, 0, [sum([thing._fightStrength() for thing in self.map.getLocationArray(self)])]]
		if subcode == 4: # Do the fight
			result = self.game.fight(self, map.getEntity(int(param[0])))
			return [not result]
		if subcode == 5: # Move entity
			moveTo = self.map.getEntity(int(params[0]))
			path = util.imperative.breadth_search(lambda x: x.adjacent(), self, moveTo)[0]
			result = 0
			actuallyTraversed = []
			for place in path[1:]:
				result = self.map.move(self, place)
				if result: break
				actuallyTraversed.append(place)
			return [1 if result else 0, 0, ["Ran out of movement (probably) - " + str(result) if result else "Success!"] + actuallyTraversed]
		if subcode == 6: # Move actions left
			return [0,0,[self.moveActions]]
		if subcode == 7: # Toggle default hostility
			self.defaultHostile = not self.defaultHostile
			return [0,0,[self.defaultHostile]]
		if subcode == 8: # Add/remove entity from hostility exceptions
			entity = self.map.getEntity(int(param[0]))
			if entity in self.hostileExceptions:
				self.hostileExceptions.remove(entity)
			else:
				self.hostileExceptions.append(entity)
			return [0,0,[entity in self.hostileExceptions]]
		if subcode == 9: # Get hostility information
			return [0,0,[self.defaultHostile]+self.hostileExceptions]
	
	def _getName(self):
		return self.name
	
	def __str__(self):
		return self._indent_print(0)
	
	def _indent_print(self, indent):
		string = "\n"+("\t"*indent) + self._details()
		for child in self.children:
			string += child._indent_print(indent+1)
		return string
	
	def _details(self):
		return "%s %s (%s): %sdp %s; %s" % (self.type, self.name, self.id, self.effectivedp, self.parent._getName(), self.description)
	
	def _fightStrength(self):
		return 0
	
	def preCycle(self):
		self.sustainCurrent = self.sustain
	
	def initCycle(self):
		self.moveActions = self.moveSpeed
		if self.living != 0:
			currentEntity = self.parent
			fedAmount = 0
			while currentEntity.type != Tile:
				need = self.living - fedAmount
				if need > currentEntity.sustainCurrent:
					fedAmount += need
					currentEntity.sustainCurrent -= need
				else:
					fedAmount += currentEntity.sustainCurrent
					currentEntity.sustainCurrent = 0
				currentEntity = currentEntity.parent
			if fedAmount < self.living:
				self.effectivedp -= (self.living - fedAmount) / 2.0
	
	def message(self, message):
		self.owner.message(message)
	
	def getDPGeneration(self):
		return 0
	
	def hurt(self, value):
		self.effectivedp -= value
		if self.effectivedp <= 0:
			self.parent.children.remove(self)
			self.map.entities.remove(self)
			print "%s died by hurt!" % (self._getName())
	
	def adjacent(self):
		return [self.parent] + util.functions.shuffled(self.children)
	
	def isHostileTo(self, enemy):
		def _hostile(entity):
			if (entity.defaultHostile and (type(entity) == Creature and type(enemy) == Creature and entity.race == enemy.race)) or (entity.defaultHostile and enemy in entity.hostileExceptions):
				return True
			else:
				return False
		return util.functions.foldr(util.functions._or, False, map( _hostile, self.map.getLocationArray(self)))

class Land(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Land, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.name = "Land (%s, %s)" % parent.location
		self.sustain = 4.0
	

class Generator(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description, dpType):
		super(Generator, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.dpType = dpType
	
	def initCycle(self):
		super(Generator, self).initCycle()
		self.currentDP[self.dpType] = self.currentDP.setdefault(self.dpType, 0) + self.effectivedp / player.GENERATOR_COST
	
	def getDPGeneration(self):
		return self.effectivedp / 4.0

CONTROL_CONTROLLED = 0
CONTROL_AUTOMATED  = 1

class Race(Entity):
	
	def __init__(self, map, owner, parent, controlType, basedp, modifiers, description):
		super(Race, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		map.game.races.append(self)
		self.trouble = 0
		self.controlType = controlType
	
	def _details(self):
		return "%s %s (%s); %s" % (self.type, self.name, self.id, self.description)
	
	def _fightStrength(self):
		return self.effectivedp / 2.0

class Creature(Entity):
	
	def __init__(self, map, owner, parent, race, basedp, modifiers, description):
		super(Creature, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.race = race
		self.moveSpeed = 2
		self.living = 1.0
	
	def _details(self):
		return "%s %s (%s): %sdp %s %s; %s" % (self.type, self.name, self.id, self.effectivedp, self.parent._getName(), self.race._getName(), self.description)
	
	def getDPGeneration(self):
		return self.effectivedp / 4.0

class Fortifications(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Fortifications, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
	
	def _fightStrength(self):
		return self.effectivedp / 2.0

class Equipment(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Equipment, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
	
	def _fightStrength(self):
		return self.effectivedp

class Legend(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Legend, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)
		self.living = 1/4.0
		self.moveSpeed = 2

class Paragon(Entity):
	
	def __init__(self, map, owner, parent, basedp, modifiers, description):
		super(Paragon, self).__init__(self.__class__.__name__, map, owner, parent, basedp, modifiers, description)


costing = {"autonomous": 0.5, "controlled": 1.0, "military": 1.5, "mobile": 1.5, "fertile": 2.0}
def cost(basedp, modifiers):
	answer = basedp
	for modifier in modifiers:
		answer /= costing[modifier]
	return answer
