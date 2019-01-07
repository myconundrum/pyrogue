import tcod
from enum import Flag,auto



class ModeFlags(Flag):
	NOFLAG = 0
	SHIFT = auto()
	ALT  = auto()
	CTRL = auto()


KEY_CURSORUP 			= 1
KEY_CURSORDOWN 			= 2
KEY_CURSORLEFT			= 3
KEY_CURSORRIGHT 		= 4
KEY_ESCAPE				= 5
KEY_ENTER				= 6

_keytranslate = {
	tcod.KEY_UP: 			KEY_CURSORUP,
	tcod.KEY_DOWN: 			KEY_CURSORDOWN,
	tcod.KEY_LEFT: 			KEY_CURSORLEFT,
	tcod.KEY_RIGHT: 		KEY_CURSORRIGHT,
	tcod.KEY_ESCAPE: 		KEY_ESCAPE,
	tcod.KEY_ENTER:			KEY_ENTER,
	tcod.KEY_SPACE: 		' ',
}

_handlers 	= {}
_curmode 	= "None"
_handlers[_curmode] = {}

class _KeyHandler():
	def __init__(self,modename,key,fn,exdata,metaflags):
		self.modename = modename
		self.key = key
		self.handler = fn
		self.exdata = exdata
		self.metaflags = metaflags

def registerhandler(modename,key,fn,exdata,metaflags=ModeFlags.NOFLAG):
	
	if not modename in _handlers:
		_handlers[modename] = {}

	data = _KeyHandler(modename,key,fn,exdata,metaflags)
	datakey = (key,metaflags)
	if datakey in _handlers[modename]:
		print(f"Input: Warning: Replacing key handler for {key}.")
	_handlers[modename][datakey] = data

def unregisterhandler(modename,key,metaflags):
	if (key,metaflags) in _handlers[_curmode]:
		del _handlers[_curmode][(key,metaflags)]
	else:
		print(f"Input: Tried to delete handler for {key} but not found in mode {modename}.")


def setmode(mode):
	global _curmode
	_curmode = mode

def processinput():

	print(_curmode)
	key = tcod.console_wait_for_keypress(True)

	metaflags = ModeFlags.NOFLAG
	if key.lalt or key.ralt:
		metaflags |= ModeFlags.ALT
	if key.shift:
		metaflags |= ModeFlags.SHIFT
	if key.lctrl or key.rctrl:
		metaflags |= ModeFlags.CTRL

	ch = chr(key.c) if key.vk not in _keytranslate else _keytranslate[key.vk]

	if (ch,metaflags) not in _handlers[_curmode]:
		print(f"no keybinding found in mode {_curmode} for {ch}.")
	else:
		kh = _handlers[_curmode][(ch,metaflags)]
		kh.handler(kh.exdata)


	


