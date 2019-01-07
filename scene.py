
import tcod
import gameinput
import win


def handletogglefullscreen(exdata):
	win.togglefullscreen()

def handlequit(exdata):
	self.quit = True

def handleexit(exdata):
	self.exit = True


class Scene:

	def __init__(self):
		self.quit = False # quit game
		self.exit = False # exit this scene
		self.statechanged = False
		self.id = "Unknown Scene"

	def enterscene(self):
		gameinput.setmode(self.id)

	def update(self):
		self.quit = tcod.console_is_window_closed()
		gameinput.processinput()
		

