import win
import gameobject
import field


# add to the background color for "lighted area"
LIGHT = win.color(50,50,0)



class Tile():

	def __init__(self,passable=True,transparent=True,color = None):
		
		self.passable 		= passable
		self.transparent 	= transparent
		self.explored		= False
		self.color 			= color

gTerrain = {
	'wall': Tile(False,False,win.color(0, 0, 100)),
	'floor': Tile(True,True,win.color(50,50,150)),
}

def gettile(name):
	t = gTerrain[name]
	return Tile(t.passable,t.transparent,t.color)

class Level():

	def __init__(self,player,width,height,win):
				
		self.width = width
		self.height = height

		self.map = [
			[gettile('wall') for y in range(height)]
			for x in range(width) 
		]

		self.objects 		= [] 	# look aside list for objects (like treasure)
		self.creatures 		= []    # look aside list for creatures (like the player or monsterss)
		self.features 		= []	# look aside list for features (like a trap, door, or stairs)

		self.player = player
		self.creatures.append(player)

		self.win = win	

		self.fov = field.Field(self.player.x,self.player.y,5,0,False,False)


	def anyat(self,x,y):
		for o in self.objects + self.creatures + self.features:
			if o.x == x and o.y == y:
				return o
		return None

	def validpos(self,x,y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height


	def objectat(self,x,y):
		for o in self.objects:
			if o.x == x and o.y == y:
				return o
		return None

	def featureat(self,x,y):
		for o in self.features:
			if o.x == x and o.y == y:
				return o
		return None

	def creatureat(self,x,y):
		for o in self.creatures:
			if o.x == x and o.y == y:
				return o
		return None


	def computefov(self):

		_lightradius = 5 # replace with lighting code later.	
		self.fov.x = self.player.x
		self.fov.y = self.player.y
		self.fov.radius = _lightradius 
		self.fov.cast(self)

	def update(self):
		
		# get the camera view of the map, and draw those objects that are within range.
		(cx,cy,cw,ch) = self.win.getcamrect()

		for y in range(cy,min(cy+ch,self.height)):
			for x in range(cx,min(cx+cw,self.width)):

				infield = self.fov.infield(x,y)

				if infield:
					self.map[x][y].explored = True

				if (self.map[x][y].explored):
					self.win.putblock(x,y,self.map[x][y].color + LIGHT if infield else self.map[x][y].color)

		for object in self.features:
			if self.win.incam(object.x,object.y) and self.map[object.x][object.y].explored:
				object.draw(self.win)

		for object in self.objects:
			if self.win.incam(object.x,object.y) and self.fov.infield(object.x,object.y):
				object.draw(self.win)

		for object in self.creatures:
			if self.win.incam(object.x,object.y) and self.fov.infield(object.x,object.y):
				object.draw(self.win)

		for object in self.creatures + self.objects + self.features:
			object.update(self)



		



   