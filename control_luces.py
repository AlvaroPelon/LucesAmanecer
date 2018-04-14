#!/usr/bin/python3
# coding=utf-8

# Este script solo funciona con python 3
# Requerimientos:
# - astral -> pip install astral

# Luz -> Pin 17
# Escrito por Alvaro Rodriguez -> https://github.com/AlvaroPelon

import time
import datetime
import RPi.GPIO as GPIO 


class luz:
	def __init__(self, pin):
		
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
	def on(self):
		GPIO.setup(self.pin, GPIO.OUT)
		print('Pin %s -> HIGH' %(self.pin))
		GPIO.output(self.pin, GPIO.HIGH)
	def off(self):
		GPIO.setup(self.pin, GPIO.OUT)
		print('Pin %s -> LOW' %(self.pin))
		GPIO.output(self.pin, GPIO.LOW)

class sun:
	def __init__(self, city='Madrid'):
		try:
			from astral import Astral
		except ImportError:
			raise ImportError('La libreria astral es necesaria')
		a = Astral()
		a.solar_depression = 'civil'
		self.city = a[city]

		self.now = datetime.datetime.now()

	def to_integer(self, hour, minute):
		return hour*100 + minute

	def sunset(self):
		sun = self.city.sun(date=datetime.date(self.now.year, self.now.month, self.now.day), local=True)
		sunsetHour = sun['sunset'].strftime('%H')
		sunsetMinute = sun['sunset'].strftime('%M')
		return self.to_integer(hour=int(sunsetHour), minute=int(sunsetMinute))

	def check_sun(self):
		now = self.to_integer(hour=self.now.hour, minute=self.now.minute)
		print (now)
		print (self.sunset())
		if now >= self.sunset():
			return True

		
if __name__ == '__main__':
	luz = luz(pin=17)
	while True:
		if sun(city='Madrid').check_sun():
			luz.on()
		else:
			luz.off()
		time.sleep(60)




