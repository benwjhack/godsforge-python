
class Message():
	
	def __init__(self, socket=None, LOG=False):
		self.socket = socket
		self.LOG = LOG
	
	def setSocket(self, sock):
		self.socket = sock
	
	def encode(self, code, subcode, param):
		if type(code) != int:
			raise TypeError("Code must be an integer")
		if type(subcode) != int:
			raise TypeError("Subcode must be an integer")
		if type(param) != list:
			raise TypeError("Param must be a list")
		param = [str(i).replace(":", "\c").replace(";", "\s").replace("\n", "\e") for i in param]
		return str(code)+":"+str(subcode)+":"+';'.join(param)
	
	def decode(self, message):
		info = {"code": None, "subcode": None, "param": []}
		parts = message.split(":")
		info["code"] = int(parts[0])
		info["subcode"] = int(parts[1])
		info["param"] = [i.replace("\c", ":").replace("\s", ";").replace("\e", "\n") for i in parts[2].split(";")]
		return info
	
	def get(self):
		return self.decode(self.socket.readLine())
	
	def send(self, code, subcode=0, param=[]):
		self.socket.sendLine(self.encode(code, subcode, param))
