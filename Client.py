from coapthon.client.helperclient import HelperClient
import threading
from collections import OrderedDict
import json
from time import sleep
# from PIL import Image
# import io
# import base64

# from handleObserve import Observer


class coapClient(threading.Thread):
	def __init__(self, jsondata):
		threading.Thread.__init__(self)
		self.jsondata = jsondata
		# self.lock = lock
		self.host = self.jsondata.getServerIp()
		self.port = self.jsondata.getPort()
		self.deviceid = self.jsondata.getDeviceId()
		self.client = HelperClient(server=(self.host, self.port))
		return

	def generatePayload(self, post=False):
		payload = OrderedDict()

		payload["DeviceID"] = self.deviceid
		payload["State"] = self.jsondata.getState()
		payload['CamState'] = self.jsondata.getCamera()
		payload['BuzzerState'] = self.jsondata.getBuzzer()

		if post:
			payload['Mode'] = self.jsondata.getMode()

		return json.dumps(payload, ensure_ascii=False, indent='\t')

	def requestPost(self):
		payload = self.generatePayload(post=True)

		try:
			response = self.client.post(path="connect", payload=payload)
			print(response.pretty_print())
		except Exception:
			print('##############################')
			print(Exception)

		return

	def requestPut(self, path):
		payload = self.generatePayload()
		return self.client.put(path, payload)

	def requestGet(self, interval=1.0):
		response = self.client.get(path='control/' + self.deviceid)
		print(response.payload)
		data = json.loads(response.payload)
		self.jsondata.setCamera(data['CamState'])
		self.jsondata.setBuzzer(data['BuzzerState'])
		# print("Camstate: ", data['CamState'])
		# print("Buzzerstate: ", data['BuzzerState'])

		threading.Timer(interval, self.requestGet).start()
		return

	# def requestObserve(self, path):
		# return self.client.observe(path, self.client_callback_observe)
	'''
	def client_callback_observe(self, response):
		if response.code == 'CONTENT':
			if response.payload is not None:
				data = json.loads(response.payload)
				# self.jsondata.setCamera(data['CamState'])
				# self.jsondata.setBuzzer(data['BuzzerState'])
				print("Camstate: ", data['CamState'])
				print("Buzzerstate: ", data['BuzzerState'])
		
		check = True
		while check:
			chosen = eval(input("Stop observing? [y/N]: "))
			if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
				print("Unrecognized choose.")
				continue
			elif chosen == "y" or chosen == "Y":
				while True:
					rst = eval(input("Send RST message? [Y/n]: "))
					if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
						print("Unrecognized choose.")
						continue
					elif rst == "" or rst == "y" or rst == "Y":
						self.client.cancel_observing(response, True)
					else:
						self.client.cancel_observing(response, False)
					check = False
					break
			else:
				break
		'''

	def checkState(self, interval=1.0):
		while():
			if self.jsondata.getState() == 'on':
				# turn on rasec if it is off

				if self.jsondata.getFirst():
					put_response = self.requestPut(path='report/' + self.deviceid)
					self.jsondata.setFirst(False)
					print(put_response.pretty_print())
			else:
				if not self.jsondata.getFirst():
					self.jsondata.setFirst(True)

			sleep(interval)

		# threading.Timer(interval, self.checkState).start()
		return

	def sendImage(self):
		data = OrderedDict()
		with open('./low.jpg', mode='rb') as file:
			img = file.read()
			# img = Image.open('./ex.jpg', mode='r')
			# f = file.read()
			# img_bytes = bytearray(f)
		# data['Image'] = base64.encodebytes(img).decode("utf-8")
		# data['Image'] = base64.b64decode(img)
		# payload = json.dumps(data, ensure_ascii=False, indent='\t')
		# img_bytes = io.BytesIO()
		# img.save(img_bytes, format='PNG')
		# img_bytes = img_bytes.getvalue()
		img_bytes = "".join(map(chr, img))
		data['Image'] = img_bytes
		payload = json.dumps(data, ensure_ascii=False, indent='\t')
		# print(img_bytes)
		# img_bytes.decode("utf-8")

		response = self.client.put(path='report/' + self.deviceid, payload=payload, timeout=5.0)
		print(response.pretty_print())
		return

	def run(self):
		self.requestPost()

		# observer = Observer(self.jsondata)
		# observer.observe()
		# observe_response = self.requestObserve(path='obs/' + self.deviceid)
		# self.handleObserve(observe_response)

		# self.sendImage()

		self.checkState()
		# self.requestGet()

		# get_response = self.requestGet(path='control/' + self.jsondata.getDeviceId())
		# print(get_response.pretty_print())

		return

	def end_trans(self):
		self.client.stop()
		return
