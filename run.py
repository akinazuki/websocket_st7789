import spidev as SPI
import logging
import ST7789
import time
import json
import base64
import RPi.GPIO as GPIO
from io import BytesIO
from websocket_server import WebsocketServer
from PIL import Image, ImageDraw, ImageFont, ImageColor

websocket_port = 13254

RST = 27
DC = 25
BL = 24
bus = 0 
device = 0
GPIO.setmode(GPIO.BCM)

keys = [
	{
		'name': 'KEY1',
		'gpio': 21
	},
	{
		'name': 'KEY2',
		'gpio': 20,
	},
	{
		'name': 'KEY3',
		'gpio': 16
	},
	{
		'name': 'UP',
		'gpio': 6
	},
	{
		'name': 'DOWN',
		'gpio': 19
	},
	{
		'name': 'LEFT',
		'gpio': 5
	},
	{
		'name': 'RIGHT',
		'gpio': 26
	},
	{
		'name': 'PRESS',
		'gpio': 13
	}
]


display = ST7789.ST7789(SPI.SpiDev(bus, device),RST, DC, BL)

display.Init()
display.clear()

server = WebsocketServer(websocket_port, host='0.0.0.0')

def new_client(client, server):
	print("New Connection",client)

def receive_message(client,server,message):
	msg = json.loads(message)
	if msg['method'] == 'picture':
		img = BytesIO(base64.b64decode(msg['data']))
		display.clear()
		status = display.ShowImage(Image.open(img),0,0)
		server.send_message(client, json.dumps({
			'method': msg['method'],
			'status': status
		}))
	elif msg['method'] == 'clear':
		status = display.clear()
		server.send_message(client, json.dumps({
			'method': msg['method'],
			'status': status
		}))
	elif msg['method'] == 'light':
		status = display.backlight(msg['switch'])
		server.send_message(client, json.dumps({
			'method': msg['method'],
			'status': status
		}))
		

def gpio_button_press_callback(KEY):
	for x in keys:
		if x['gpio'] == KEY:
			print("Key: " + x['name'] + " Pressed")
			server.send_message_to_all(json.dumps({
				'method': 'key_press',
				'key': KEY,
				'name': x['name']
			}))

for x in keys:
	print("Setup GPIO Port[" + str(x['gpio']) + "], Key: " + x['name'])
	GPIO.setup(x['gpio'],GPIO.IN,GPIO.PUD_UP)
	print("Adding GPIO Port[" + str(x['gpio']) + "], Key: " + x['name'] + " Event Callback")
	GPIO.add_event_detect(x['gpio'], GPIO.FALLING, gpio_button_press_callback, 200)
	pass

server.set_fn_new_client(new_client)
server.set_fn_message_received(receive_message)
server.run_forever()
