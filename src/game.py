import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from player import Player
import math

def game(d, players):
	pg.init()
	display = (1280,960)
	pg.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0,0, -d*2.5)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glLineWidth(4)

	turn = 0
	player_filter = set([])

	mi,ma = -d//2+1, d//2+1
	cubes = [[[Cube(0.97, i,j,k) for k in range(mi,ma)] for j in range(mi,ma)] for i in range(mi,ma)]
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
				if event.key in [pg.K_LEFT, pg.K_RIGHT, pg.K_PAGEDOWN, pg.K_PAGEUP, pg.K_UP, pg.K_DOWN]:
					cubes[cursor[0]][cursor[1]][cursor[2]].deselect()
					cursor[0] = (cursor[0]-(event.key == pg.K_LEFT)+(event.key == pg.K_RIGHT))%d
					cursor[1] = (cursor[1]-(event.key == pg.K_PAGEDOWN)+(event.key == pg.K_PAGEUP))%d
					cursor[2] = (cursor[2]-(event.key == pg.K_UP)+(event.key == pg.K_DOWN))%d
					cubes[cursor[0]][cursor[1]][cursor[2]].select()

				if event.key in range(pg.K_1, pg.K_1+len(players)):
					k = int(event.unicode)
					player_filter.discard(k) if k in player_filter else player_filter.add(k)

				if event.key == pg.K_SPACE:
					if cubes[cursor[0]][cursor[1]][cursor[2]].claim(players[turn]):
						# TODO: check win
						print("{} owns cubes:\n  {}".format(players[turn], "\n  ".join(map(str, [a for c in cubes for b in c for a in b if a.owned_by == players[turn]]))))
						turn = (turn+1) % len(players)

		# draw scene
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		for cube in [a for c in cubes for b in c for a in b]:
			cube.draw(players[turn].color, player_filter)
		draw_compass(players, -d/1.7,-d/1.7,d/1.7)
		pg.display.flip()
		pg.time.wait(10)


def draw_compass(players, x,y,z):
	glColor4f(*players[0].color); glBegin(GL_LINES); glVertex3fv([x-1,y,z]); glVertex3fv([x+1,y,z]); glEnd()
	glColor4f(*players[1].color); glBegin(GL_LINES); glVertex3fv([x,y-1,z]); glVertex3fv([x,y+1,z]); glEnd()
	glColor4f(*players[2].color); glBegin(GL_LINES); glVertex3fv([x,y,z-1]); glVertex3fv([x,y,z+1]); glEnd() 


if __name__ == '__main__':
	dimension_size = 3
	players = (	Player(1, [1,0,0,0.5]), 
				Player(2, [0,1,0,0.5]), 
				Player(3, [0,0,1,0.5]))
	game(dimension_size, players)
	print(pg.K_1)
	print(dir(pg.K_1))