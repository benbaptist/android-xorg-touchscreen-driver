import pymouse, struct, threading, signal, os
class Touch:
	def __init__(self):
		self.touch = open('/dev/input/event5', 'r')
		self.side = open('/dev/input/event4', 'r')
		self.mouse = pymouse.PyMouse()
		self.x, self.y = self.mouse.position()
		self.width, self.height = (480, 800)
		self.finger = False
		self.landscape = True
		self.abort = False
		self.power = True
		self.backlight = 10
	def handleButtons(self): # power, volume buttons
		while not self.abort:
			self.side.read(2)
			event = self.side.read(2)
			more = self.side.read(4)
			
			power = False
			if more == '\x01\x00\x00\x00':
				power = True
			if event == '\x73\x00': # volume up
				if power:
					self.mouse.press(self.x, self.y, button=2)
				else:
					self.mouse.release(self.x, self.y, button=2)
			if event == '\x74\x00': # power button
				if power:
					if self.power:
						backlight = open('/sys/class/lcd/s5p_lcd/lcd_power', 'w')
						backlight.write('0')
						backlight.close()
						backlight = open('/sys/class/backlight/s5p_bl/brightness', 'w')
						backlight.write('0')
						backlight.close()
					else:
						backlight = open('/sys/class/lcd/s5p_lcd/lcd_power', 'w')
						backlight.write('1')
						backlight.close()
						backlight = open('/sys/class/backlight/s5p_bl/brightness', 'w')
						backlight.write(str(self.backlight))
						backlight.close()
					self.power = not self.power
	def handle(self):
		#self.mouse.press(5,5)
		#self.mouse.release(5,5)
		
		while not self.abort:
			self.touch.read(2)
			event = self.touch.read(2)
			more = self.touch.read(4)
			
			if event == '\x35\x00':
				self.y = struct.unpack('I', more)[0]
				#print "x packet"
			if event == '\x36\x00': # Y
				self.x = self.height - struct.unpack('I', more)[0]
				#print 'y packet'
				if self.finger == True:
					self.finger = False
					self.mouse.press(self.x, self.y)
			if event == '\x30\x00' and more == '\x00\x00\x00\x00':
				#print "Finger up"
				self.finger = False
				self.mouse.release(self.x, self.y)
			elif event == '\x30\x00':
				#print "Finger down"
				self.finger = True
				#m.press(realX, realY)
			#if event == '\x8b\x00' and more == '\x01\x00\x00\x00':
				#print "pressed menu"
			if event == '\x8b\x00' and more == '\x01\x00\x00\x00':
				self.mouse.press(self.x, self.y, button=2)
				#print "pressed back"
			if event == '\x8b\x00' and more == '\x00\x00\x00\x00':
				self.mouse.release(self.x, self.y, button=2)
				#print "pressed back"
			#print [self.x, self.y]
def signal_handler(signal, frame):
	t.abort = True
signal.signal(signal.SIGINT, signal_handler)
t = Touch()
thr = threading.Thread(target=t.handleButtons, args=())
thr.start()
t.handle()
