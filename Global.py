class jsonData(object):
	def __init__(self):
		self.pollinginterval = 3000
		self._deviceid = "device1"
		self._serverip = '192.168.0.3'
		# self._serverip = '127.0.0.1'
		self._port = 5683
		self._mode = 'push'
		self._state = "off"
		self._control = ""
		self._camera = False
		self._buzzer = False
		self._first = True
		return

	def getServerIp(self):
		return self._serverip

	def getPort(self):
		return self._port

	def getDeviceId(self):
		return self._deviceid

	def setDeviceId(self, deviceid):
		self._deviceid = deviceid
		return

	def getState(self):
		return self._state

	def setState(self, state):
		self._state = state
		return

	def getMode(self):
		return self._mode

	def getCamera(self):
		return self._camera

	def setCamera(self, camera):
		self._camera = camera
		return

	def getBuzzer(self):
		return self._buzzer

	def setBuzzer(self, buzzer):
		self._buzzer = buzzer
		return

	def getFirst(self):
		return self._first

	def setFirst(self, first):
		self._first = first
		return
