import os, sys
import pygame

pygame.mixer.pre_init(48000,-16,2,2048)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
pygame.init()

size = 200,200
screen = pygame.display.set_mode(size)

def playSound(sound):
	soundLocation = os.path.join("SoundBank",sound+".wav")
	soundObject = pygame.mixer.Sound(soundLocation)
	soundObject.play()

startClock = pygame.time.Clock()
while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT: 
			sys.exit()
			pygame.mixer.quit()
		elif e.type == pygame.KEYDOWN:
			keyName = pygame.key.name(e.key)
			if keyName == "escape": 
				sys.exit()
				pygame.mixer.quit()
			elif keyName == "up":
				playSound("HiHat")
			elif keyName == "down":
				playSound("Bass")
			elif keyName == "left":
				playSound("Snare")
			elif keyName == "right":
				playSound("TomMid")
			elif keyName == "space":
				playSound("TomLow")
		elif e.type == pygame.MOUSEBUTTONDOWN:
			playSound("Crash")
	startClock.tick_busy_loop(50)