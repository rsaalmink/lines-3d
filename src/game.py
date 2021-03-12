import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
import math

def main(d):
	pygame.init()
	display = (1280,920)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0,0, -d*2.5)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_LINE_SMOOTH)
	glLineWidth(4)

	# 3D = 3 player: red,green,blue
	player_colors = [[1,0.0,0.0,0.6], [0.0,1,0.0,0.6], [0.0,0.0,1,0.6]]
	player = 0

	mi,ma = -d//2+1, d//2+1
	cubes = [[[Cube(0.48, i,j,k) for k in range(mi,ma)] for j in range(mi,ma)] for i in range(mi,ma)]
	cursor = [0, 0, 0]
	cubes[cursor[0]][cursor[1]][cursor[2]].select()

	while True:
		# handle input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			glRotatef(1,0,-1,0)
		if keys[pygame.K_w]:
			glRotatef(1,-1,0,0)
		if keys[pygame.K_s]:
			glRotatef(1,1,0,0)
		if keys[pygame.K_d]:
			glRotatef(1,0,1,0)		
		if keys[pygame.K_q]:
			glRotatef(1,0,0,1)		
		if keys[pygame.K_e]:
			glRotatef(1,0,0,-1)			
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_PAGEUP, pygame.K_PAGEDOWN]:
					cubes[cursor[0]][cursor[1]][cursor[2]].deselect()
					if event.key == pygame.K_LEFT:
						cursor[0] = (cursor[0]-1)%d
					if event.key == pygame.K_RIGHT:
						cursor[0] = (cursor[0]+1)%d
					if event.key == pygame.K_UP:
						cursor[2] = (cursor[2]-1)%d
					if event.key == pygame.K_DOWN:
						cursor[2] = (cursor[2]+1)%d
					if event.key == pygame.K_PAGEUP:
						cursor[1] = (cursor[1]+1)%d
					if event.key == pygame.K_PAGEDOWN:
						cursor[1] = (cursor[1]-1)%d
					cubes[cursor[0]][cursor[1]][cursor[2]].select()

				if event.key == pygame.K_SPACE:
					if cubes[cursor[0]][cursor[1]][cursor[2]].claim(player, player_colors[player]):
						# TODO: check win
						print("Player {} owns cubes:\n  {}".format(player, "\n  ".join(map(str, [a for c in cubes for b in c for a in b if a.owned_by == player]))))
						player = (player+1) % len(player_colors)

		# draw scene
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		for cube in [a for c in cubes for b in c for a in b]:
			cube.draw(highlight_color=player_colors[player], filter=1)
		draw_compass(-d/1.7,-d/1.7,d/1.7)
		pygame.display.flip()
		pygame.time.wait(10)


def draw_compass(x,y,z):
	glColor4f(1,0,0,0.5); glBegin(GL_LINES); glVertex3fv([x,y,z-1]); glVertex3fv([x,y,z+1]); glEnd() 
	glColor4f(0,1,0,0.5); glBegin(GL_LINES); glVertex3fv([x-1,y,z]); glVertex3fv([x+1,y,z]); glEnd()
	glColor4f(0,0,1,0.5); glBegin(GL_LINES); glVertex3fv([x,y-1,z]); glVertex3fv([x,y+1,z]); glEnd()


if __name__ == '__main__':
	main(3)