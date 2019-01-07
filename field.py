
#
# creates a field of points that are weighted by distance from the center. 
# the weight formula is 1 / (distance from center + 1)
#
# the field will naturally decay each turn -- the amount of decay is set in the
# decay field. Points are removed when the point weight is less than zero. 
# so a decay of 0 means points are never removed, and 100 means they will be removed
# during the first update. 
#
#
# Note -- the field will be blocked by objects with the A_FLAG_BLOCKLOS flag unless
# the ghost variable is set to true.
#
#
# If you set the "keepOld" flag, the field will keep old points from the last cast.
# otherwise, cast is destructive of the old field.
#
import math

class Field():

	def __init__(self,x,y,radius,decay,ghost,keepold):
		self.radius         = radius                
		self.decay          = decay                
		self.points         = []			# points are stored internally as a tuple containing (x,y,and weight)
		self.x 				= x
		self.y 				= y 
		self.ghost          = ghost
		self.keepold        = keepold

	def dedupepoints(self,oldlist):

		r = []
		
		for p in oldlist:
			(x,y,w) = p
			found = False
			for p2 in r:
				(x2,y2,w2) = p2
				if x == x2 and y == y2:
					found = True 
			if not found:
				r.append(p)

		return r


	def updatelist(self,new):
		old = self.points
		self.points = self.dedupepoints(new)

		if self.keepold:
			for oldp in oldlist:
				(ox,oy,ow) = oldp
				found = False
				for newp in self.points:
					(nx,ny,nw) = newp 
					if ox == nx and oy == ny:
						found = True
						break

				if not found:
					self.points.append(oldp)

	def infield(self,x,y):

		for p in self.points:
			(px,py,pw) = p
			if px == x and py == y:
				return True

		return False


	def cast(self,level): 

		dx = -self.radius
		dy = -self.radius
		n = []

		#
		# cast rays to max range in quarters
		#
		while dx < self.radius: 
			n += self.castray(level,dx,dy)
			dx += 1
		while dy < self.radius:
			n += self.castray(level,dx, dy)
			dy += 1
		while dx > -self.radius:
			n += self.castray(level,dx,dy)
			dx -= 1
		while dy > -self.radius:
			n += self.castray(level,dx, dy)
			dy -= 1

		#
		# update the list of points in self field.
		#
		self.updatelist(n)
	 
	

	def castray(self,level,dirX,dirY):

		x 			= self.x
		y 			= self.y
		dx          = abs(dirX)
		dy          = abs(dirY)
		sx          = 1 if dirX > 0 else -1
		sy 			= 1 if dirY > 0 else -1 
		err         = dx - dy
		xSum        = 0
		ySum        = 0

		touched 	= []

		while True:

			#
			# max range reached?
			#
			if (xSum * xSum + ySum * ySum >= self.radius * self.radius):
				break

			#
			# check for out of bounds.
			#
			if not level.validpos(x,y):
				break

			#
			# Remember that we touched self point.
			#
			weight = 1/(math.sqrt((self.x-x)**2 + (self.y-y)**2) + 1)
			touched.append((x,y,weight))

			#
			# check to see if we should block our LOS
			#
			if not level.map[x][y].passable and not self.ghost:
				break
	
			e2 = (2 * err)

			if (e2 > -dy):
				xSum += 1
				err -= dy
				x += sx

			if (e2 < dx):
				ySum += 1
				err += dx
				y += sy

		return touched

	#
	# see if a point lies in the field and return its weight. Otherwise, return -1
	#
	def getweight(self,x,y):

		for p in self.points:
			(px,py,pw) = p
			if x == px and y == py:
				return pw

		return -1

	#
	# updates a field by decaying weights and pruning any no longer in field
	# tiles.
	#
	def update(self):

		n = []

		for p in self.points:
			(x,y,w) = p
			w -= self.decay 
			if w > 0:
				n.append((x,y,w))

		self.points = n


