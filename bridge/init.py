from simple_websocket_server import WebSocketServer, WebSocket

from util.sockets import ClientSocket

import threading

SECRET = "super!!secure--"

class SimpleEcho(WebSocket):
	def handle(self):
		string = self.data
		print "reced", string
		if not string.startswith(SECRET): return
		print "received", string
		
		self.sock.sendLine(string.strip(SECRET))
	
	def connected(self):
		print(self.address, 'connected')
		
		sock = ClientSocket('localhost', 5050)
		self.sock = sock
		
		def handle(sock):
			while True:
				m = sock.readLine()
				print "sending", repr(m)
				self.send_message(m)
		
		t = threading.Thread(target=handle, args=(sock,))
		t.daemon = True
		t.start()
	
	def handle_close(self):
		print(self.address, 'closed')


server = WebSocketServer('', 5051, SimpleEcho)
server.serve_forever()
