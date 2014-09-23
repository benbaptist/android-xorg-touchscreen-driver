import pymouse, struct, time
touch = open('/dev/input/event2', 'r')
x = 0
y = 0
xB = 0
yB = 0
queryPress = False 
# change this to fit your screen
maxWidth = 800
maxHeight = 480
needReset = False
#maxWidth = 768
#maxHeight = 1280
m = pymouse.PyMouse()
Xorg = [m.position()[0], m.position()[1]]
screenW = m.screen_size()[0]
screenH = m.screen_size()[1]
#def check():
#	while True:
#		m.press(Xorg[0], Xorg[1])
#		time.sleep(0.1)
def hardMax(i, max):
	if i > max:
		return max
	return i
def hardMin(i, min):
	if i < min:
		return min
	return i
while 1:
	touch.read(2)
	event = touch.read(2)
	more = touch.read(4)
	if event == '\x35\x00': # X
		if needReset:
			x = struct.unpack('H', more[:2])[0]/2
		x2 = struct.unpack('H', more[:2])[0]/2
		diff = x - x2
		x = x2
		Xorg[0] = Xorg[0] + diff
		print diff
		#print str(x1) + " | " + str(x)
	if event == '\x36\x00': # Y
		y2 = struct.unpack('I', more)[0] / 2
		diff = y - y2
		y = y2
		Xorg[1] = Xorg[1] + diff
		#print diff
	Xorg[0] = hardMin(Xorg[0], 0)
	Xorg[1] = hardMin(Xorg[1], 0)
	Xorg[0] = hardMax(Xorg[0], screenW)
	Xorg[1] = hardMax(Xorg[1], screenH)
	#print Xorg
	realX = Xorg[1]
	realY = maxHeight - Xorg[0]
	m.move(Xorg[0], Xorg[1])
	if event == '\x39\x00' and more == '\xff\xff\xff\xff':
		print "Finger up"
		needReset = True
		#m.release(Xorg[0], Xorg[1])
	elif event == '\x39\x00':
		print "Finger down"
		#queryPress = True
		needReset = False
	if xB is not x or yB is not yB:
		#print "x: %s | y: %s" % (str(realX), str(realY))
		#m.move(realX, realY)
		xB = x
		yB = y
#m = pymouse.PyMouse()
#m.move(5, 5)
