import random
from level import gettile
import gameobject


#parameters for dungeon generator
ROOMMAXSIZE = 10
ROOMMINSIZE = 6


class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		centerx = (self.x1 + self.x2) // 2
		centery = (self.y1 + self.y2) // 2
		return (centerx, centery)
 
	def intersect(self, other):
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)


def _createroom(level,room):
		for x in range(room.x1 + 1 ,room.x2):
			for y in range(room.y1 + 1,room.y2):
				level.map[x][y] = gettile('floor')

def _createhtunnel(level,x1, x2, y):
	for x in range(min(x1, x2), max(x1, x2) + 1):
		level.map[x][y] = gettile('floor')

def _createvtunnel(level,y1, y2, x):
	for y in range(min(y1, y2), max(y1, y2) + 1):
		level.map[x][y] = gettile('floor')

def _placestairs(level):

	for i in range(5):
		placed = False
		while (not placed):
			x = random.randint(0,level.width-1)
			y = random.randint(0,level.height-1)
			if (level.map[x][y].passable):
				level.features.append(gameobject.create('downstair',x,y))
				placed = True

	for i in range(3):
		placed = False
		while (not placed):

			x = random.randint(0,level.width-1)
			y = random.randint(0,level.height-1)
			if (level.map[x][y].passable):
				level.features.append(gameobject.create('upstair',x,y))
				placed = True
			

def _placetreasure(level):

	for i in range(20):
		placed = False
		while (not placed):

			x = random.randint(0,level.width-1)
			y = random.randint(0,level.height-1)
			if (level.map[x][y].passable and level.anyat(x,y) == None):
				level.objects.append(gameobject.create('gold',x,y))
				placed = True


			

def createdungeon(level,maxrooms):
	
	rooms = []
	numrooms = 0
 
	for r in range(maxrooms):
		#random width and height
		w = random.randint(ROOMMINSIZE, ROOMMAXSIZE)
		h = random.randint(ROOMMINSIZE, ROOMMAXSIZE)

		#random position without going out of the boundaries of the map

		x = random.randint(0, level.width - w - 1)
		y = random.randint(0, level.height - h - 1)
 
		#"Rect" class makes rectangles easier to work with
		newroom = Rect(x, y, w, h)
 
		#run through the other rooms and see if they intersect with this one
		failed = False
		for otherroom in rooms:
			if newroom.intersect(otherroom):
				failed = True
				break
 
		if not failed:
			#this means there are no intersections, so this room is valid
 
			#"paint" it to the map's tiles
			_createroom(level,newroom)
 
			#center coordinates of new room, will be useful later
			(newx, newy) = newroom.center()
 
			if numrooms == 0:
				#this is the first room, where the player starts at
				level.player.x = newx
				level.player.y = newy
				level.win.centercam(newx,newy)
			else:
				#all rooms after the first:
				#connect it to the previous room with a tunnel
 
				#center coordinates of previous room
				(prevx, prevy) = rooms[numrooms-1].center()
 
				#draw a coin (random number that is either 0 or 1)
				if random.randint(0, 1) == 1:
					#first move horizontally, then vertically
					_createhtunnel(level, prevx, newx, prevy)
					_createvtunnel(level, prevy, newy, newx)
				else:
					#first move vertically, then horizontally
					_createvtunnel(level, prevy, newy, prevx)
					_createhtunnel(level, prevx, newx, newy)
 
			#finally, append the new room to the list
			rooms.append(newroom)
			numrooms += 1

	_placestairs(level)
	_placetreasure(level)





