
global currentUID
currentUID = 0

def getCurrentUID():
	return currentUID

def generateUID():
	global a
	a += 1
	return a

class User:
	
	def __init__(self):
		self.uid = generateUID();
		self.uber = false
	
	def loadUser(uid, key=None): # TODO: make this function check user is valid, then return false if not
		if uid > getCurrentUID(): return false
		self.uid = uid
		return True
