#!/usr/bin/env python

'''
For this to work you must start timidity MIDI server:
	1. Start timidity as daemon service (timidity -iAD).
	2. List MIDI servers (aconnect -o).
	3. The list will contain ('ALSA', 'Timidity port 0', 0, 1, 0). The position
	of this line in the list, starting with a zero position, is the port you
	will use in pygame.midi.Output
'''

from time import sleep
import os, sys
import RPi.GPIO as GPIO
import pygame
import pygame.midi
from random import randint

#MIDI setup (not all voices worked, only those that did are available)
instruments = [0,1,2,4,5,6,7,8,9,13,14,15,16,19,21,23,24,25,26,27,28,29,30,
	32,33,34,35,36,37,38,40,42,44,45,46,47,48,53,56,57,58,59,60,61,64,65,66,
	67,68,69,70,71,72,73,74,75,76,79,80,84,88,94,95,98,101,102,104,114,115,
	120,122,125]

instrument = instruments[randint(0,len(instruments)-1)]

pygame.init()
pygame.midi.init()

for i in range(0,pygame.midi.get_count()):
	print(pygame.midi.get_device_info(i))

port = 2
midiOutput = pygame.midi.Output(port, 1)
midiOutput.set_instrument(instrument)

keyPins = [22,18,24]
instrumentPins = [17,4]

#Input pins setup
GPIO.setmode(GPIO.BCM)

for v in keyPins:
	GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(v, GPIO.BOTH)

for v in instrumentPins:
	GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(v, GPIO.FALLING)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def playSound(note):
	midiOutput.note_on(note,127)

def stopSound(note):
	midiOutput.note_off(note,127)

pinState = [0,0,0]
pinSound = [60,64,67]

try:
	while True:
		#change instruments
		for v in instrumentPins:
			if GPIO.event_detected(v):
				if v == 4 and instruments.index(instrument) < len(instruments)-1:
					instrument = instruments[instruments.index(instrument) + 1]
				elif v == 4 and instruments.index(instrument) == len(instruments)-1:
					instrument = instruments[0]
				if v == 17 and instruments.index(instrument) > 0:
					instrument = instruments[instruments.index(instrument) - 1]
				elif v == 17 and instruments.index(instrument) == 0:
					instrument = instruments[len(instruments)-1]
				print(instrument)
			midiOutput.set_instrument(instrument)

		#play note assigned to button
		for v in keyPins:
			if GPIO.event_detected(v):
				if not GPIO.input(v):
					playSound(pinSound[keyPins.index(v)])
					pinState[keyPins.index(v)] = 1
				else:
					stopSound(pinSound[keyPins.index(v)])
					pinState[keyPins.index(v)] = 0

		if not GPIO.input(25):
			for i in pinSound:
				midiOutput.note_off(i,127)
		sleep(0.0001)

except KeyboardInterrupt:
	print("\nClosing keyboard...")
	del midiOutput
	sys.exit()
	pygame.midi.quit()
	GPIO.cleanup()
