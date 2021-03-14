from OpenGL.GL import *
from OpenGL.GLU import *
import time

class Cube:
	def __init__(self, size, x, y, z, initial_color=[0.3,0.3,0.3,0.3] ):
		self.size = size
		self.position = [x,y,z]
		s = size / 2
		self.vertices = (	(s+x, -s+y, -s+z),
							(s+x, s+y, -s+z),
							(-s+x, s+y, -s+z),
							(-s+x, -s+y, -s+z),
							(s+x, -s+y, s+z),
							(s+x, s+y, s+z),
							(-s+x, -s+y, s+z),
							(-s+x, s+y, s+z)
						)

		self.edges = (	(0,1),
						(0,3),
						(0,4),
						(2,1),
						(2,3),
						(2,7),
						(6,3),
						(6,4),
						(6,7),
						(5,1),
						(5,4),
						(5,7))

		self.color = initial_color
		self.is_selected = False
		self.owned_by = None

	def set_color(self, color):
		self.color = color

	def deselect(self):
		self.is_selected = False

	def select(self):
		self.is_selected = True

	def claim(self, player):
		if self.owned_by is None:
			self.set_color(player.color)
			self.owned_by = player
			return True
		return False

	def __repr__(self):
		return "{}".format(self.position)

	def draw(self, highlight_color, uid_filter, method="wireframe"):
		if self.owned_by is None or self.owned_by and self.owned_by.uid not in uid_filter:
			if method == "wireframe":
				if self.is_selected:
					# blink with quadratic interpolation
					t = time.time() % 1
					glColor4f(*[c[0]*(t**2) + c[1]*((1.0-t**2)) for c in zip(self.color, highlight_color if highlight_color != self.color else [1,1,1,0.5])])
				else:
					glColor4f(*self.color)
				glBegin(GL_LINES)
				for edge in self.edges:
					for vertex in edge:
						glVertex3fv(self.vertices[vertex])
				glEnd()
			elif method == "volumetric":
				pass
			else:
				raise
