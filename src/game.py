import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from player import Player

def game(size, players, turn = 0, player_filter=set([])):
	pg.init()
	display = (1280,960)
	pg.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0,0, -size*2.5)

	glEnable(GL_BLEND)
	glEnable(GL_LINE_SMOOTH)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glLineWidth(4)

	# Create a collection of size*size*size cubes, centering around 0,0,0 in scene
	minpos,maxpos = -size//2+1, size//2+1
	cubes = [[[Cube(0.97, i,j,k) for k in range(minpos,maxpos)] for j in range(minpos,maxpos)] for i in range(minpos,maxpos)]
	cursor = [0, 0, 0]
	cubes[cursor[0]][cursor[1]][cursor[2]].select()

	while True:
		# handle continuous input (rotating)
		keys = pg.key.get_pressed()
		glRotatef(1, keys[pg.K_s]-keys[pg.K_w],keys[pg.K_d]-keys[pg.K_a],keys[pg.K_q]-keys[pg.K_e])
		# handle discrete input	
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				pg.quit()
				quit()
			if event.type == pg.KEYDOWN:
				# move cursor around
				if event.key in [pg.K_LEFT, pg.K_RIGHT, pg.K_PAGEDOWN, pg.K_PAGEUP, pg.K_UP, pg.K_DOWN]:
					cubes[cursor[0]][cursor[1]][cursor[2]].deselect()
					cursor[0] = (cursor[0]-(event.key == pg.K_LEFT)+(event.key == pg.K_RIGHT))%size
					cursor[1] = (cursor[1]-(event.key == pg.K_PAGEDOWN)+(event.key == pg.K_PAGEUP))%size
					cursor[2] = (cursor[2]-(event.key == pg.K_UP)+(event.key == pg.K_DOWN))%size
					cubes[cursor[0]][cursor[1]][cursor[2]].select()
				# claim cube for current player
				if event.key == pg.K_SPACE:
					if cubes[cursor[0]][cursor[1]][cursor[2]].claim(players[turn]):
						if check_win([c for a in cubes for b in a for c in b], players, turn, minpos, maxpos-1):
							print("{} has won, showing solution!".format(players[turn]))
							cubes[cursor[0]][cursor[1]][cursor[2]].deselect()
							player_filter = set([p.uid for p in players if p != players[turn]])
						turn = (turn+1) % len(players)
				# filter which players' cubes are being shown
				if event.key in range(pg.K_1, pg.K_1+len(players)):
					p = players[event.key - pg.K_1].uid
					if p in player_filter:
						player_filter.discard(p) 
					else:
						player_filter.add(p)

		# draw scene
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		for cube in [a for c in cubes for b in c for a in b]:
			cube.draw(players[turn].color, player_filter)
		draw_compass(players, -size/1.7,-size/1.7,size/1.7)
		pg.display.flip()
		pg.time.wait(10)


def draw_compass(players, x,y,z):
	glColor4f(*players[0].color); glBegin(GL_LINES); glVertex3fv([x-1,y,z]); glVertex3fv([x+1,y,z]); glEnd()
	glColor4f(*players[1].color); glBegin(GL_LINES); glVertex3fv([x,y-1,z]); glVertex3fv([x,y+1,z]); glEnd()
	glColor4f(*players[2].color); glBegin(GL_LINES); glVertex3fv([x,y,z-1]); glVertex3fv([x,y,z+1]); glEnd() 


def check_win(cubes, players, idx, minpos, maxpos):
	# e.g. for a 5x5x5 game, players[1] wins if a path exists from any cube[p][-2][q] to a cube[r][2][s]
	queue = [c.position for c in cubes if c.owned_by == players[idx] and c.position[idx] == minpos]
	rest  = [c.position for c in cubes if c.owned_by == players[idx] and c.position[idx] != minpos]
	while len(queue) > 0:
		c = queue.pop(0)
		if c[idx] == maxpos:
			return True
		neighbours = [r for r in rest if sum([(x-y)**2 for x,y in zip(c,r)]) == 1]
		queue += neighbours
		rest = [r for r in rest if r not in neighbours]
	return False


if __name__ == '__main__':
	size = 4
	players = (	Player(1, [1,0,0,0.6]), 	# Red
				Player(2, [0,1,0,0.6]), 	# Green
				Player(3, [0,0,1,0.6]))		# Blue
	game(size, players)