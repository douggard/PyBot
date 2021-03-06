import sys
from time import sleep
try:
	import win32com.client
	import win32con
	import win32api
except ImportError:
	import Xlib.display
	import Xlib.ext.xtest as xtest
	import Xlib.XK

class robot:	
	opsys = sys.platform

	if opsys.find('linux') != -1:
		def __init__(self):
			self.keyboard = {
				'`':'`', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '0':'0', '-':'minus', '=':'equal',
				'q':'q', 'w':'w', 'e':'e', 'r':'r', 't':'t', 'y':'y', 'u':'u', 'i':'i', 'o':'o', 'p':'p', '[':'braceleft', ']':'braceright', '\\':'backslash', 
				'a':'a', 's':'s', 'd':'d', 'f':'f', 'g':'g', 'h':'h', 'j':'j', 'k':'k', 'l':'l', ';':'semicolon', '\'':'apostrophe', 
				'z':'z', 'x':'x', 'c':'c', 'v':'v', 'b':'b', 'n':'n', 'm':'m', ',':'comma', '.':'period', '/':'slash', 
				'~':['Shift_L', '`'], '!':['Shift_L', '1'], '@':['Shift_L', '2'], '#':['Shift_L', '3'], '$':['Shift_L', '4'], '%':['Shift_L', '5'], '^':['Shift_L', '6'], '&':['Shift_L', '7'], '*':['Shift_L', '8'], '(':['Shift_L', '9'], ')':['Shift_L', '0'], '_':['Shift_L', 'minus'], '+':['Shift_L', 'equal'], 
				'Q':['Shift_L', 'q'], 'W':['Shift_L', 'w'], 'E':['Shift_L', 'e'], 'R':['Shift_L', 'r'], 'T':['Shift_L', 't'], 'Y':['Shift_L', 'y'], 'U':['Shift_L', 'u'], 'I':['Shift_L', 'i'], 'O':['Shift_L', 'o'], 'P':['Shift_L', 'p'], '{':['Shift_L','braceleft'], '}':['Shift_L','braceright'], '|':['Shift_L', 'backslash'], 
				'A':['Shift_L', 'a'], 'S':['Shift_L', 's'], 'D':['Shift_L', 'd'], 'F':['Shift_L', 'f'], 'G':['Shift_L', 'g'], 'H':['Shift_L', 'h'], 'J':['Shift_L', 'j'], 'K':['Shift_L', 'k'], 'L':['Shift_L', 'l'], ':':['Shift_L', 'semicolon'], '"':['Shift_L', "apostrophe"], 
				'Z':['Shift_L', 'z'], 'X':['Shift_L', 'x'], 'C':['Shift_L', 'c'], 'V':['Shift_L', 'v'], 'B':['Shift_L', 'b'], 'N':['Shift_L', 'n'], 'M':['Shift_L', 'm'], '<':['Shift_L', 'comma'], '>':['Shift_L', 'period'], '?':['Shift_L', 'slash'],
				' ':'space', '\n':'Return', '\t':'Tab', 
				'\x00':'leftarrow', '\x01':'uparrow', '\x02':'rightarrow', '\x03':'downarrow', '\x04':'Shift_L', '\x05':'Shift_R', '\x06':'Control_L', '\x07':'Control_R', 
				'\x08':'Backspace', '\x09':'Tab', '\x0A':'Return', '\x0B':'vt', '\x0C':'ff', '\x0D':'cr', '\x0E':'Alt_L', '\x0F':'Alt_R', 
				'\x10':'Super_L', '\x11':'Super_R', '\x12':'Menu', '\x13':'Insert', '\x14':'Scroll_Lock', '\x15':'Page_Up', '\x16':'Page_Down', '\x17':'Num_Lock', 
				'\x18':'Pause', '\x19':'Printscreen', '\x1A':'F1', '\x1B':'Escape', '\x1C':'Delete', '\x1D':'Home', '\x1E':'End', '\x1F':'F12', }

			#basic set of free chars needed to not interfere with python escapes (can't find BEL char \x07)
			#mappings are found in file: cat /usr/include/X11/keysymdef.h | grep -i KEYNAME
			#'\x00':'', '\x01':'', '\x02':'', '\x03':'', '\x04':'', '\x05':'', '\x06':'', '\x07':'', 
			#'\x08':'Backspace', '\x09':'Tab', '\x0A':'Return', '\x0B':'vt', '\x0C':'ff', '\x0D':'cr' '\x0E':'', '\x0F':'', 
			#'\x10':'', '\x11':'', '\x12':'', '\x13':'', '\x14':'', '\x15':'', '\x16':'', '\x17':'', 
			#'\x18':'', '\x19':'', '\x1A':'', '\x1B':'', '\x1C':'', '\x1D':'', '\x1E':'', '\x1F':'', }

			self.disp = Xlib.display.Display()

		'''method for sending a character without modifiers'''
		def sendSingle(self, char):
			disp = self.disp
			ksym = Xlib.XK.string_to_keysym(char)
			kcode = disp.keysym_to_keycode(ksym)
			xtest.fake_input(disp, Xlib.X.KeyPress, kcode)
			xtest.fake_input(disp, Xlib.X.KeyRelease, kcode)
			disp.flush()

		'''method for sending character with modifiers'''
		def sendCombo(self, chars):
			kcodes = []
			disp = self.disp
			for char in chars:
				ksym = Xlib.XK.string_to_keysym(char)
				kcode = disp.keysym_to_keycode(ksym)
				kcodes.append(kcode)
			
			for kcode in kcodes:
				xtest.fake_input(disp, Xlib.X.KeyPress, kcode)
			kcodes.reverse()
			for kcode in kcodes:
				xtest.fake_input(disp, Xlib.X.KeyRelease, kcode)

			disp.flush()	

	elif opsys.find('win32') != -1:
		def __init__(self):
			self.shell = win32com.client.Dispatch("WScript.Shell")
			
			self.keyboard = {
				"`":"`", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", "0":"0", "-":"-", "=":"=", 
				"q":"q", "w":"w", "e":"e", "r":"r", "t":"t", "y":"y", "u":"u", "i":"i", "o":"o", "p":"p", "[":"[", "]":"]", "\\":"\\", 
				"a":"a", "s":"s", "d":"d", "f":"f", "g":"g", "h":"h", "j":"j", "k":"k", "l":"l", ";":";", "'":"'", 
				"z":"z", "x":"x", "c":"c", "v":"v", "b":"b", "n":"n", "m":"m", ",":",", ".":".", "/":"/", 
				"~":"~", "!":"{!}", "@":"@", "#":"{#}", "$":"$", "%":"%", "^":"{^}", "&":"&", "*":"*", "(":"(", ")":")", "_":"_", "+":"{+}", 
				"Q":"Q", "W":"W", "E":"E", "R":"R", "T":"T", "Y":"Y", "U":"U", "I":"I", "O":"O", "P":"P", "{":"{{}", "}":"{}}", "|":"|", 
				"A":"A", "S":"S", "D":"D", "F":"F", "G":"G", "H":"H", "J":"J", "K":"K", "L":"L", ":":":", "\"":"\"", 
				"Z":"Z", "X":"X", "C":"C", "V":"V", "B":"B", "N":"N", "M":"M", "<":"<", ">":">", "?":"?", " ":"{SPACE}", 
				"\n":"{ENTER}", "\t":"{TAB}", 
				"\x00":"{LEFT}", "\x01":"{UP}", "\x02":"{RIGHT}", "\x03":"{DOWN}", "\x04":"{ESC}", "\x05":"{PRINTSCREEN}", "\x06":"", "\x07":"", 
				"\x08":"{BACKSPACE}", "\x09":"{TAB}", "\x0a":"{ENTER}", "\x0b":"", "\x0c":"", "\x0d":"", "\x0e":"", "\x0f":"^f", 
				"\x10":"", "\x11":"", "\x12":"", "\x13":"", "\x14":"", "\x15":"", "\x16":"", "\x17":"", 
				"\x18":"", "\x19":"", "\x1a":"", "\x1b":"", "\x1c":"", "\x1d":"", "\x1e":"", "\x1f":""}
			
		def sendSingle(self, char):
			self.shell.SendKeys(char)

		def sendModified(self, char, modifiers):
			CTRL = 1
			SHIFT = 2
			ALT = 4
			modList = [CTRL,SHIFT,ALT]
			lookup = {0:'', 1:'^', 2:'+', 4:'!'}
			sendStr = ''

			for modMask in modList:
				sendStr += lookup[modifiers&modMask]

			sendStr += self.keyboard[char]
			print sendStr
			self.sendSingle(sendStr)

		def moveMouse(self, x, y):
			swidth = win32api.GetSystemMetrics(0) + 0.0
			sheight =  win32api.GetSystemMetrics(1) + 0.0
			win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
			                     int(x/swidth*65535.0), int(y/sheight*65535.0))
			

		def slowMoveMouse(self, x, y):
			x=1

		def clickMouse(self, button):
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

		def moveClickMouse(self, x, y, button):
			buttons = [[2,4], [8,16], [32, 64]]
			LEFT = 0
			#RIGHT = 1
			#MIDDLE = 2
			swidth = win32api.GetSystemMetrics(0) + 0.0
			sheight =  win32api.GetSystemMetrics(1) + 0.0
			win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/swidth*65535.0), int(y/sheight*65535.0))
			#win32api.SetCursorPos([250,250])
			sleep(0.5)
			win32api.mouse_event(buttons[LEFT][0], 0, 0, 0, 0)
			sleep(0.1)
			win32api.mouse_event(buttons[LEFT][1], 0, 0, 0, 0)
			sleep(0.1)
			

	'''os independent methods'''
	def sendChar(self, char):
		expanded_char = self.keyboard[char]
		if type(expanded_char) is list:
			self.sendCombo(expanded_char)
		else:
			self.sendSingle(expanded_char)

	def typeOut(self, string):
		variance = 0
		for char in string:
			self.sendChar(char)
			stime = 0.1 + variance
			variance = (0x7 & ord(char)) / 100.0
			sleep(stime)

			
kittens = robot()
sleep(2)
kittens.moveClickMouse(250, 250, 1)
quit()
