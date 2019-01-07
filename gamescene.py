from level import Level, Tile
import gameobject
import dungeon
import win
import scene
import tcod


	
class GameScene(scene.Scene):

	def __init__(self):	
		super().__init__()

		# initialize various windows used in this scene:
		# gamewin -> main map view
		# hudwin -> left stripe wtih key char information
		# msgwin -> basic messages window
		self.gamewin 	= win.Window(10,0,win.screenwidth-10,win.screenheight)
		self.hudwin		= win.Window(0,0,10,win.screenheight)
		self.hudwin.setbg(win.color(50,50,50))
		self.msgwin		= win.Window(self.hudwin.width,win.screenheight-10,win.screenwidth-self.hudwin.width,10)
		self.msgwin.setalpha(1.0,0.0)

		# create player and level object
		self.player 	= gameobject.create('player',50,50)
		self.level 		= Level(self.player,200,200,self.gamewin)
	
		# create initial dungeon and compute the initial player field of view and player position.
		dungeon.createdungeon(self.level,2)
		self.level.computefov()

		self.id = "Game Scene"

		self.keydict = {
			',':(self._handlestairs,'upstair'),
			'.':(self._handlestairs,'downstair'),
			}


	def _handlestairs(self,key,ex):

		o = self.level.featureat(self.player.x,self.player.y)
		if o != None  and o.name == ex:
			self.level = Level(self.player,200,200,self.gamewin)
			dungeon.createdungeon(self.level,50)
			for o in self.level.features:
				if (o.name == 'downstair' and ex == 'upstair') or (o.name =='upstair' and ex =='downstair'):
					self.player.x = o.x
					self.player.y = o.y
					self.level.computefov()
					self.level.win.centercam(self.player.x,self.player.y)
					break



	def handleinput(self):

		key = super().handleinput()
		if tcod.console_is_key_pressed(tcod.KEY_UP):
			self.player.move(self.level, 0,-1)
		elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
			self.player.move(self.level, 0,1)
		elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
			self.player.move(self.level, -1,0)
		elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
			self.player.move(self.level, 1,0)

		elif chr(key.c) in self.keydict:
			(fn,ex) = self.keydict[chr(key.c)]
			fn(key,ex)

		return key

	def _hudupdate(self):
		self.hudwin.print(0,0,"Adventurer")
		self.hudwin.print(0,5,f"Gold: {self.player.gold}")


	def _msgupdate(self):
		self.msgwin.print(0,9,f"Location: ({self.player.x},{self.player.y})")

	def update(self):
		super().update()
		
		# clear active windows
		self.gamewin.clear()
		self.hudwin.clear()
		self.msgwin.clear()

		# do all level updates
		self.level.update()

		# handle all other window updates
		self._hudupdate()
		self._msgupdate()

		# render all windows.
		self.gamewin.render()
		self.hudwin.render()
		self.msgwin.render()








