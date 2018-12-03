import RPi.GPIO as GPIO
from Adafruit_IO import Client
import time

ADAFRUIT_IO_USERNAME = "ameyaditya"
ADAFRUIT_IO_KEY = "85049e20366041e0812a3b5786526548"
current = 'OFF'

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(26,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
def switch_on():
	print("Turning on")
	GPIO.output(2, False)
	global current
	current = 'ON'
def switch_off():
	print("turning off")
	GPIO.output(2, True)
	global current
	current = 'OFF'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
current_26 = GPIO.input(26)
while True:
	if GPIO.input(26) != current_26:
		if current == 'ON':
			switch_off()
			print("Switch off current state = {0}, previous state {1}".format(GPIO.input(26), current_26))
			aio.send('toggle-switch','OFF')
			current_26 = GPIO.input(26)
		else:
			switch_on()
			print("Switch off current state = {0}, previous state {1}".format(GPIO.input(26), current_26))
			print("turning on state:{0}".format(GPIO.input(26)))
			aio.send('toggle-switch','ON')
			current_26 = GPIO.input(26)
	data = aio.receive('toggle-switch')
	if data.value == 'OFF' and current != 'OFF':
		print("assistant off")
		switch_off()
	elif data.value == 'ON' and current != 'ON':
		print("assistant on")
		switch_on()
	print(current)
	time.sleep(1)
	