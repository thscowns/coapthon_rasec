import threading
from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO
from datetime import datetime
# from io import BytesIO


pirPin = 12
buzzerPin = 24
switchPin = 20


class machine(threading.Thread):
	def __init__(self, jsondata):
		threading.Thread.__init__(self)
		self.jsondata = jsondata

		self.camera = PiCamera()
		self.camera.resolution = (130, 100) #(2592, 1944)
		self.camera.start_preview()

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pirPin, GPIO.IN)
		GPIO.setup(buzzerPin, GPIO.OUT)
		GPIO.setup(switchPin, GPIO.IN, GPIO.PUD_DOWN)

		GPIO.setup(buzzerPin, False)
		self.buzzer = GPIO.PWM(buzzerPin, 100)
		self.switch = GPIO.input(switchPin)
		self.picnum = 0

		# self.lock = lock
		return

	def ringBuzzer(self):
		self.buzzer.start(100)
		self.buzzer.ChangeDutyCycle(90)

		# GPIO.output(buzzerPin, True)
		sleep(0.5)
		# GPIO.output(buzzerPin, False)

		self.buzzer.stop()
		return

	def checkmachine(self):
		while(True):
			'''
			if self.switch != 0:
				self.jsondata.setState('on')
			else:
				self.jsondata.setState('off')
			'''
			# print(self.jsondata.getBuzzer())
			if self.jsondata.getBuzzer():
				print("Buzzer Ring!")
				self.ringBuzzer()
				self.jsondata.setBuzzer(False)

			# self.camera.capture('./pic/%s.jpg', str(datetime.now()))

			if not self.jsondata.getCamera():
				self.camera.capture('./pic/' + str(self.picnum) + '.jpg')
				self.jsondata.setCamera(True)
				self.picnum += 1

			'''
			tmp = input("set State on, off")
			if tmp == 'on':
				self.jsondata.setState('on')
			else:
				self.jsondata.setState('off')
			'''
			sleep(2.0)
		return

	def run(self):
		# codes for obtain sensor's info
		self.checkmachine()
		return
