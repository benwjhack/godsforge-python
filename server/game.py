from map import Map

class Game:
	
	def __init__(self):
		self.UIDcounter = 0
		self.players = []
		self.maxPlayers = 6
		self.closed = False
		self.cycle = 0
		self.started = False
		self.map = Map(self)
		self.map.initTiles(-4, 4, -4, 4)
		Message.game = self
		self.story = ""
	
	def sendMessage(self, sender, receiverUID, content):
		mask = str(sender)
		message = Message(mask, content, receiverUID)
		self.getEntity(receiverUID).message(message)
		return 0
	
	def addStory(self, line):
		if not line in self.story:
			self.story += line + "\n"
	
	def vote(self, player, value):
		if not self.started: return
		
		self.votes[player.UID] = value
		if sum(self.votes.values()) >= len(self.players):
			self.advanceCycle()
	
	def resetVotes(self):
		self.votes = {player:False for player in [p.UID for p in self.players]}
	
	def initCycle(self):
		self.resetVotes()
		for player in self.players:
			player.initCycle()
	
	def startGame(self):
		print "\n----------------------------STARTING GAME----------------------------\n"
		self.closed = True
		self.started = True
		self.initCycle()
		for i in xrange(len(self.players)):
			self.players[i].gameIndex = i
	
	def advanceCycle(self):
		# Maybe rename this function to _advanceCycle, and make an adavanceCycle function to spin this function off as a thread- so as not to block server-client thread.
		self.cycle += 1
		print "\n----------------------------CYCLE %s----------------------------\n" % (self.cycle,)
		self.initCycle()
	
	def addPlayer(self, player):
		if self.closed:
			raise Exception()
		self.players.append(player)
		if len(self.players) == self.maxPlayers:
			self.closed = True
	
	def generateUID(self):
		temp = self.UIDcounter
		self.UIDcounter += 1
		return temp
	
	@property
	def entities(self):
		return self.players + []
	
	def getEntity(self, UID):
		for entity in self.entities:
			if entity.UID == UID:
				return entity
		return None
	
	def save(self):
		pass
	
	def load(self):
		pass
class Message:
	
	game = None
	
	def __init__(self, mask, content, UID):
		self.mask = mask
		self.content = content
		self.receiverUID = UID
		self.receiver = Message.game.getEntity(UID)
	
	def __str__(self):
		return "From: %s; To: %s; Content: %s" % (self.mask, self.receiver, self.content)

