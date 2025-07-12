import pygame
import os

ASSETS = r'assets/'

BACKGROUND_COLORS = [(107, 190, 50), (154, 230, 78)] # There Are Two Colors Which Is 0 and 1 Indices Which Is True And False Too!!

def load_img(path, scale = 1, set_color_key=(0,0,0)):
	img = pygame.image.load(ASSETS+path).convert()
	if set_color_key:
		img.set_colorkey((0,0,0))
	return pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))

def get_maps() :
	maps_dict = {}
	for filename in os.listdir(r"Maps/") :
		maps_dict[str(filename[4])] = filename

def draw_background(window, rows=9, cols=9):
	square_size = 80
	color_index = False # False -> 0, True -> 1
	for row in range(rows):
		for col in range(cols):
			pygame.draw.rect(window, BACKGROUND_COLORS[color_index], 
								pygame.Rect(col*square_size, row*square_size, square_size, square_size))
			color_index = not color_index # Here I Just Change The Color So If Its index is 0 it will be 1 and if 1 it will be 0

#returning the distance between 2 points (I could use the فيثاغورز rule but that one is much easier)
def Distance_2_points(point1,point2) :
	point1 = pygame.Vector2(point1[0],point1[1])
	point2 = pygame.Vector2(point2[0],point2[1])
	return point1.distance_to(point2)