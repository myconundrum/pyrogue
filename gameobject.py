import win
from enum import Flag,auto

class ObjectFlags(Flag):
	NOFLAGS = 0
	TREASURE = auto()
	CANCARRY = auto()


class GameObject():

	def __init__(self,x,y,name, rep,color,fl=ObjectFlags.NOFLAGS):
		self.rep = rep
		self.color = color
		self.x = x
		self.y = y
		self.name = name
		self.flags = fl 
		self.gold = 0 if not self.flags & ObjectFlags.TREASURE else 10


	def move(self,level,dx,dy):
		if (level.map[self.x+dx][self.y+dy].passable):
			self.x += dx
			self.y += dy

	def update(self,level):
		pass

	def draw(self,win):
		win.putchar(self.x,self.y,self.rep,self.color)



class CreatureState(Flag):
	NOFLAGS 		= 0
	ASLEEP 			= auto()
	AWAKE 			= auto()
	FOLLOWING		= auto()


class CreatureObject(GameObject):

	def __init__(self,x,y,name, rep,color,fl=ObjectFlags.NOFLAGS):

		super().__init__(x,y,name, rep,color,fl)
		self.state = CreatureState.ASLEEP

	def update(self,level):
		
		super().update(level)





class PlayerObject(GameObject):

	def __init__(self,x,y,name, rep,color,fl=ObjectFlags.NOFLAGS):

		super().__init__(x,y,name, rep,color,fl)

	
		self.camboundary = 5			# How close to the edge of a camera view before we recenter
		

	def move(self,level,dx,dy):

		super().move(level,dx,dy)
		
		# recompute player fov
		level.computefov()

		o = level.objectat(self.x,self.y)
		if (o != None and o.flags & ObjectFlags.TREASURE):
			self.gold += o.gold
			level.objects = [x for x in level.objects if x != o]


		# recompute camera parameters.
		(cx,cy,cw,ch) = level.win.getcamrect()
		if (self.x - cx < self.camboundary or cx+cw - self.x < self.camboundary or 
			self.y - cy < self.camboundary or cy+ch - self.y < self.camboundary):
			level.win.centercam(self.x,self.y)


gobjecttemplates = {

	'player' 		: (PlayerObject,'@',win.white,ObjectFlags.NOFLAGS),
	'downstair'		: (GameObject,'>',win.white,ObjectFlags.NOFLAGS),
	'upstair'		: (GameObject,'<',win.white,ObjectFlags.NOFLAGS),
	'gold'			: (GameObject,'$',win.gold,ObjectFlags.CANCARRY | ObjectFlags.TREASURE),

}


def create(name,x,y):

	o = None

	if name in gobjecttemplates:
		(base,rep,color,fl) = gobjecttemplates[name]
		o = base(x,y,name,rep,color,fl)
	else:
		print(f'Unknown object type named {name}.')

	return o



		
