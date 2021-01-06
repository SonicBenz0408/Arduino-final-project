import socket


class WiFi():

	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.ip = socket.gethostbyname(socket.gethostname())
		print(self.ip)
		self.port = 1234

	def send_data(self, data):
		try:
			self.client.connect((self.ip, self.port))
			print("successfully connect")

			self.client.send(data)
			print("send:", data)
		except:
			print("send error")

if __name__ == '__main__':
	test = WiFi()
	test.connect_wifi()