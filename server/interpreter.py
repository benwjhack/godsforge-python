
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
		if code == 53:
			entity = self.game.map.getEntity(int(param[0]))
			return entity.__order__(self.player, subcode, param[1:])
		
		if code == 60:
			return self.create(subcode, param)
	
	def create(self, subcode, param):
		
		game = self.game
		player = self.player
		parentType = param[1] == "True"
		if parentType:
			x, y = map(int, param[2].split("/"))
		else:
			id = int(param[2])
		
		if subcode == 0: # Land
			print str(player), "creating land with", param
			if not parentType:
				return [3, 0, ["Land must be attatched to a tile"]]
			response = player.createLand(param[0], x, y, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			return [response] # Maybe should be moved left one indent, so everything returns a response code?
		if subcode == 1: # Generator
			print str(player), "creating generator with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			response = player.createGenerator(param[0], parent, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			if type(response) == list:
				return response
			else:
				return [response]
		if subcode == 2: # Race
			print str(player), "creating race with", param
			response = player.createRace(param[0], param[3], int(param[5])) # Notably, param[2] is empty for consistency
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			return [response]
		if subcode == 3: # Creature
			print str(player), "creating creature with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			parentRace = self.game.map.getEntity(int(param[5]))
			if parentRace.type != "Race":
				return [3, 0, ["Parent race needs to be a *race*"]]
			response = player.createCreature(param[0], float(param[6]), parent, parentRace, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			return [response]
		if subcode == 4: # Fortification
			print str(player), "creating fortification with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			response = player.createFortification(param[0], float(param[5]), parent, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			if type(response) == list:
				return response
			else:
				return [response]
		if subcode == 5: # Equipment
			print str(player), "creating equipment with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			response = player.createEquipment(param[0], float(param[5]), parent, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			if type(response) == list:
				return response
			else:
				return [response]
		if subcode == 6: # Legend
			print str(player), "creating legend with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			response = player.createLegend(param[0], float(param[5]), parent, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			if type(response) == list:
				return response
			else:
				return [response]
		if subcode == 7: # Paragon
			print str(player), "creating paragon with", param
			if parentType:
				parent = self.game.map.getTile(x, y)
			else:
				parent = self.game.map.getEntity(id)
			response = player.createParagon(param[0], float(param[5]), parent, param[3])
			if response == 0:
				game.addStory(param[4])
			else:
				print "failed"
			if type(response) == list:
				return response
			else:
				return [response]
