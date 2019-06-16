# from coapthon.client.helperclient import HelperClient
# import json
# from collections import OrderedDict
# import threading
from time import sleep

import Global
from Client import coapClient
from handleRas import machine
from handleObserve import Observer
from handleImage import imageHandler

jsondata = Global.jsonData()
host = jsondata.getServerIp()
port = jsondata.getPort()
# lock = threading.Lock()


def main():
	rasec = machine(jsondata)
	rasec.start()

	client = coapClient(jsondata)
	client.start()

	sleep(1.0)

	observer = Observer(jsondata)
	observer.start()

	sleep(1.0)

	imghandler = imageHandler(jsondata)
	imghandler.start()

	# client.stop()
	return


if __name__ == '__main__':
	main()
