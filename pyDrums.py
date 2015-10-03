import os, sys
import pygame
import threading
import time

exitFlag = 0

pygame.mixer.pre_init(48000,-16,2,2048)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
pygame.init()

size = 200,200
screen = pygame.display.set_mode(size)

class myThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		self.threadID - threadID
		self.name = name
		self.counter = counter
	def run(self):
		print "Starting " + self.name
		# Synch Threads
		threadLock.acquire()
		print_time(self.name, self.counter, 3)
		threadLock.release()
		
def print_time(threadName, delay, counter):
	while counter:
		if exitFlag:
			threadName.exit()
		time.sleep(delay)
		print "%s: %s" %(threadName, time.ctime(time.time()))
		counter -= 1
		
threadLock = threading.Lock()
threads = []

# create threads
quitThread = myThread(1, "quitThread", 1)
hihatThread = myThread(2, "hihatThread", 2)
bassThread = mythread(3, "bassThread", 3)
snareThread = myThred(4, "snareThread", 4)
tommidThread = mythread(5, "tommidThread, 5)
tomlowThread = mythread(6, "tomlowThread", 6)
crashThread = mythread(7, "creashThread", 7)

#add threads to list
threads.append(quitThread)
threads.append(hihatThread)
threads.append(bassThread)
threads.append(snareThread)
threads.append(tommidThread)
threads.append(tomlowThread)
threads.append(crashThread)

def playSound(sound):
	soundLocation = os.path.join("SoundBank",sound+".wav")
	soundObject = pygame.mixer.Sound(soundLocation)
	soundObject.play()

for t in threads:
	t.join()
print "Exiting Main Thread"

# startClock = pygame.time.Clock()
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
	time.sleep(.06)
