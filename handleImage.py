import threading
from collections import OrderedDict
import json
import requests
from datetime import datetime
import base64
import os
from time import sleep


class imageHandler(threading.Thread):
	def __init__(self, jsondata):
		threading.Thread.__init__(self)
		self.jsondata = jsondata
		# self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.url = "http://" + self.jsondata.getServerIp() + ":8080/RaSec/photos"
		self.date = ""
		return

	def sendImage(self):
		while(True):
			# print(self.jsondata.getCamera())
			if self.jsondata.getCamera():
				data = OrderedDict()
				filelist = os.listdir("./pic")
				imgname = './pic/' + filelist[-1]

				with open(imgname, mode='rb') as file:
					img = file.read()

				data['name'] = str(datetime.now().month) + '-' + str(datetime.now().day) + \
							   '-' + str(datetime.now().hour) + '-' + str(datetime.now().minute) + \
							   '-' + str(datetime.now().second)
				# img_bytes = "".join(map(chr, img))
				# data['imageByte'] = img_bytes
				# tmp = base64.encodebytes(img).decode("utf-8")
				# print(type(tmp))
				# data['imageByte'] = base64.encodebytes(img).decode("utf-8")
				data['imageByte'] = str(base64.b64encode(img))
				# print(str(base64.b64decode(img)))
				headers = {'Content-Type': 'application/json'}
				payload = json.dumps(data, ensure_ascii=False, indent='\t')
				response = requests.put(self.url, data=payload, headers=headers)
				print(response)
				self.jsondata.setCamera(False)

			sleep(2.0)

		# threading.Timer(1.0, self.sendImage()).start()
		return

	def run(self):
		self.sendImage()
		return
