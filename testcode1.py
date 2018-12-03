import Rpi.GPIO as GPIO
from Adafruit_IO import Client
import time

ADAFRUIT_IO_USERNAME = "ameyaditya"
ADAFRUIT_IO_KEY = "85049e20366041e0812a3b5786526548"
current = ''

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUTPUT)
GPIO.setup(26,GPIO.INPUT, pull_up_down = GPIO.PUD_DOWN)
def switch_on():
	GPIO.output(2, False)
	current = 'ON'
def switch_off():
	GPIO.output(2, True)
	current = 'OFF'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
current_26 = GPIO.input(26)
while True:
	if GPIO.input(26) != current_26:
		if current == 'ON':
			switch_off()
			aio.send('toggle-switch','OFF')
			current_26 = GPIO.input(26)
		else:
			switch_on()
			aio.send('toggle-switch','ON')
			current_26 = GPIO.input(26)
	data = aio.receive('toggle-switch')
	if data.value == 'OFF' and current != 'OFF':
		switch_off()
	elif data.value == 'ON' and current != 'ON':
		switch_on()
	time.sleep(1)
	