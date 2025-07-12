import pygame
import sys
import os # when i will change the map in the same run no need to break the run and edit manually
from tile_map import Tile_Map
from utils import load_img

class Editor:
  # Class Level Attributes
  # Editor settings 
  WIDTH = 720
  HEIGHT = 720
  SIDE_BAR_WIDTH = 200
  FPS = 60
  SCROLL_SPEED = 40
  CONTROLS_WIDTH = 200

  def __init__(self):
    self.current_level = 5 # It Should Be Here For The Window Caption (You Can Change This Variable To Change The Maps Or To Add One)
    # setup pygame
    pygame.init()
    self.screen = pygame.display.set_mode((Editor.WIDTH+Editor.SIDE_BAR_WIDTH+Editor.CONTROLS_WIDTH, Editor.HEIGHT))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Mini-Golf-Editor (Map '+ str(self.current_level) + ')')

    # controls img
    self.controls_img = load_img('controls.png')

    # setup assets
    self.assets = {
      "black_tile": load_img("black_tile.png", set_color_key=False),
      "white_tile": load_img("white_tile.png"), 
      "ball": load_img('Golf_Ball_Body.png', .1),
      'hole': load_img('hole.png', .6),

      # water
      'water': load_img('water.png', .5),
      'top_right_water': load_img('top_right_water.png', .5),
      'top_left_water': load_img('top_left_water.png', .5),
      'right_side_water': load_img('right_side_water.png', .5),
      'left_side_water': load_img('left_side_water.png', .5),
      'bottom_left_water': load_img('bottom_left_water.png', .5),
      'bottom_middle_water': load_img('bottom_middle_water.png', .5),
      'bottom_right_water': load_img('bottom_right_water.png', .5),
      'top_middle_water': load_img('top_middle_water.png', .5),
      'top_left_angle': load_img('top_left_angle.png', .5),
      'top_right_angle': load_img('top_right_angle.png', .5),
      'bottom_left_angle': load_img('bottom_left_angle.png', .5),
      'bottom_right_angle': load_img('bottom_right_angle.png', .5),

      # dirt
      'dirt': load_img('dirt.png', .5),
      'top_right_dirt': load_img('top_right_dirt.png', .5),
      'top_left_dirt': load_img('top_left_dirt.png', .5),
      'right_side_dirt': load_img('right_side_dirt.png', .5),
      'left_side_dirt': load_img('left_side_dirt.png', .5),
      'bottom_left_dirt': load_img('bottom_left_dirt.png', .5),
      'bottom_middle_dirt': load_img('bottom_middle_dirt.png', .5),
      'bottom_right_dirt': load_img('bottom_right_dirt.png', .5),
      'top_middle_dirt': load_img('top_middle_dirt.png', .5),
      'top_left_dirt_angle': load_img('top_left_dirt_angle.png', .5),
      'top_right_dirt_angle': load_img('top_right_dirt_angle.png', .5),
      'bottom_left_dirt_angle': load_img('bottom_left_dirt_angle.png', .5),
      'bottom_right_dirt_angle': load_img('bottom_right_dirt_angle.png', .5),

      # white wall
      'white_wall': load_img('white_wall.png', .5),
      'white_wall_middle': load_img('white_wall_middle.png', .5),
      'white_wall_left': load_img('white_wall_left.png', .5),
      'white_wall_right': load_img('white_wall_right.png', .5),
      'gate': load_img('gate.png', .5),
      'left_edge': load_img('edge.png', .5),
      'right_edge': load_img('edge2.png', .5),

      # black wall
      'black_wall': load_img('black_wall.png', .5),
      'left_black_wall': load_img('left_black_wall.png', .5),
      'right_black_wall': load_img('right_black_wall.png', .5),
      'middle_left_wall': load_img('middle_left_wall.png', .5),
      'middle_right_wall': load_img('middle_right_wall.png', .5),
      'middle_black_wall': load_img('middle_black_wall.png', .5),

      # flag
      'flag': load_img('flag.png'),
      'red_flag': load_img('red_flag.png')
    }

    self.tile_map = Tile_Map(self)

    self.current_level_map = f'Maps/map_{str(self.current_level)}.json'

    try:
      self.tile_map.load(self.current_level_map)
    except FileNotFoundError:
      pass # Don't Load Any Thing No Map Is Going To Be Draw

    self.x_gap = 50
    self.y_gap = 60
    self.side_bar_imgs_positions = self.generate_rects()

    self.current_img = (self.assets['black_tile'], 'black_tile') # self.current_img = (img, key)

    self.clicking = False
    self.right_clicking = False
    
    self.scroll_up = False
    self.scroll_down = False

  def generate_rects(self):
    positions = []
    x = self.x_gap
    y = 20
    cols = 2
    for key in self.assets:
      positions.append((pygame.Rect(Editor.WIDTH+x, y, self.tile_map.tile_size, self.tile_map.tile_size), key))
      x += self.x_gap + self.tile_map.tile_size

      # Check If I Need To Go To Another Row
      cols -= 1
      if cols == 0:
        y += self.y_gap
        x = self.x_gap
        cols = 2
    
    return positions

  def render_side_bar_imgs(self):
    for rect, key in self.side_bar_imgs_positions: # This Is More Safe Rather Than Assuming
      img = self.assets[key]
      self.screen.blit(img, rect)

  def run(self):
    while True:
      self.screen.fill('gray')

      # render controls img
      self.screen.blit(self.controls_img, (Editor.WIDTH+Editor.SIDE_BAR_WIDTH+20, 200))

      pygame.draw.rect(self.screen, (141, 196, 53), pygame.Rect(0, 0, Editor.WIDTH, Editor.HEIGHT))

      self.tile_map.render(self.screen)

      # Draw The Current Choosed Tile On The Top Left Of The Screen
      img = list(self.current_img)[0].copy()
      img.set_alpha(150)
      self.screen.blit(img, (5, 5))

      self.render_side_bar_imgs()

      # Handling Clicking To Add Or Remove Tiles
      mpos = pygame.mouse.get_pos()
      tile_pos = (int(mpos[0] // self.tile_map.tile_size), int(mpos[1] // self.tile_map.tile_size))
      if self.clicking: # Adding Tiles
        balls = []
        if 0 <= mpos[0] <= Editor.WIDTH:
          #make one spawner only (delete the old spawner when putting other one)
          #here we collect balles
          if self.current_img[1] == "ball" :
            for key in self.tile_map.tile_map :
              tile = self.tile_map.tile_map[key]
              if tile['type'] == "ball" :
                balls.append(key)
                
            #here we delete old balls
            for ball in balls :
              del self.tile_map.tile_map[ball]

          self.tile_map.tile_map[str(tile_pos[0])+';'+str(tile_pos[1])] = {'type': list(self.current_img)[1], 'pos': tile_pos}

      if self.right_clicking: # Removing Tiles
        tile_pos_str = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_pos_str in self.tile_map.tile_map:
          del self.tile_map.tile_map[tile_pos_str]

      # Scroll Side Bar If The Tiles I Use Is More Than The Screen Height 
      if self.scroll_up:
        for rect, key in self.side_bar_imgs_positions:
          rect.y -= Editor.SCROLL_SPEED
        self.scroll_up = False
      if self.scroll_down:
        for rect, key in self.side_bar_imgs_positions:
          rect.y += Editor.SCROLL_SPEED
        self.scroll_down = False

      #exit the game
      for event in pygame.event.get():
        # Exit Setup
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN: 
          if event.key == pygame.K_ESCAPE: # If User Clicked On Escape Key He Will Quit Too, Because I'm Too Laze To Move My Hand To Get The Mouse 😅
            pygame.quit()
            sys.exit()

          # save current map
          if event.key == pygame.K_s:
            self.tile_map.save(self.current_level_map)

          # New Map
          if event.key == pygame.K_LSHIFT:
            self.current_level = len(os.listdir('Maps')) + 1  # Make New Map
            pygame.display.set_caption('Mini-Golf-Editor (Map '+ str(self.current_level) + ')')
            self.current_level_map = f'Maps/map_{str(self.current_level)}.json'
            self.tile_map.tile_map = {"12;-1": {"type": "water", "pos": [12, -1]}, "11;-1": {"type": "water", "pos": [11, -1]}, "10;-1": {"type": "water", "pos": [10, -1]}, "9;-1": {"type": "water", "pos": [9, -1]}, "8;-1": {"type": "water", "pos": [8, -1]}, "7;-1": {"type": "water", "pos": [7, -1]}, "6;-1": {"type": "water", "pos": [6, -1]}, "0;0": {"type": "water", "pos": [0, 0]}, "0;2": {"type": "right_side_water", "pos": [0, 2]}, "0;3": {"type": "right_side_water", "pos": [0, 3]}, "0;4": {"type": "right_side_water", "pos": [0, 4]}, "0;5": {"type": "right_side_water", "pos": [0, 5]}, "0;6": {"type": "right_side_water", "pos": [0, 6]}, "0;7": {"type": "right_side_water", "pos": [0, 7]}, "0;10": {"type": "right_side_water", "pos": [0, 10]}, "0;11": {"type": "right_side_water", "pos": [0, 11]}, "0;12": {"type": "right_side_water", "pos": [0, 12]}, "0;13": {"type": "right_side_water", "pos": [0, 13]}, "0;14": {"type": "right_side_water", "pos": [0, 14]}, "0;15": {"type": "right_side_water", "pos": [0, 15]}, "0;16": {"type": "right_side_water", "pos": [0, 16]}, "0;17": {"type": "right_side_water", "pos": [0, 17]}, "0;18": {"type": "right_side_water", "pos": [0, 18]}, "0;19": {"type": "right_side_water", "pos": [0, 19]}, "0;20": {"type": "right_side_water", "pos": [0, 20]}, "0;21": {"type": "right_side_water", "pos": [0, 21]}, "0;22": {"type": "bottom_left_angle", "pos": [0, 22]}, "1;22": {"type": "top_middle_water", "pos": [1, 22]}, "2;22": {"type": "top_middle_water", "pos": [2, 22]}, "3;22": {"type": "top_middle_water", "pos": [3, 22]}, "4;22": {"type": "top_middle_water", "pos": [4, 22]}, "5;22": {"type": "top_middle_water", "pos": [5, 22]}, "6;22": {"type": "top_middle_water", "pos": [6, 22]}, "6;23": {"type": "water", "pos": [6, 23]}, "7;23": {"type": "water", "pos": [7, 23]}, "8;23": {"type": "water", "pos": [8, 23]}, "9;23": {"type": "water", "pos": [9, 23]}, "10;23": {"type": "water", "pos": [10, 23]}, "11;23": {"type": "water", "pos": [11, 23]}, "12;23": {"type": "water", "pos": [12, 23]}, "13;23": {"type": "water", "pos": [13, 23]}, "13;22": {"type": "top_middle_water", "pos": [13, 22]}, "14;22": {"type": "top_middle_water", "pos": [14, 22]}, "12;22": {"type": "top_middle_water", "pos": [12, 22]}, "11;22": {"type": "top_middle_water", "pos": [11, 22]}, "10;22": {"type": "top_middle_water", "pos": [10, 22]}, "9;22": {"type": "top_middle_water", "pos": [9, 22]}, "8;22": {"type": "top_middle_water", "pos": [8, 22]}, "7;22": {"type": "top_middle_water", "pos": [7, 22]}, "15;22": {"type": "top_middle_water", "pos": [15, 22]}, "16;22": {"type": "top_middle_water", "pos": [16, 22]}, "17;22": {"type": "top_middle_water", "pos": [17, 22]}, "18;22": {"type": "top_middle_water", "pos": [18, 22]}, "19;22": {"type": "top_middle_water", "pos": [19, 22]}, "20;22": {"type": "top_middle_water", "pos": [20, 22]}, "21;22": {"type": "top_middle_water", "pos": [21, 22]}, "22;21": {"type": "left_side_water", "pos": [22, 21]}, "22;20": {"type": "left_side_water", "pos": [22, 20]}, "22;19": {"type": "left_side_water", "pos": [22, 19]}, "22;18": {"type": "left_side_water", "pos": [22, 18]}, "22;17": {"type": "left_side_water", "pos": [22, 17]}, "22;16": {"type": "left_side_water", "pos": [22, 16]}, "22;15": {"type": "left_side_water", "pos": [22, 15]}, "22;14": {"type": "left_side_water", "pos": [22, 14]}, "22;13": {"type": "left_side_water", "pos": [22, 13]}, "22;12": {"type": "left_side_water", "pos": [22, 12]}, "22;11": {"type": "left_side_water", "pos": [22, 11]}, "22;8": {"type": "left_side_water", "pos": [22, 8]}, "22;7": {"type": "left_side_water", "pos": [22, 7]}, "22;6": {"type": "left_side_water", "pos": [22, 6]}, "22;5": {"type": "left_side_water", "pos": [22, 5]}, "22;4": {"type": "left_side_water", "pos": [22, 4]}, "22;3": {"type": "left_side_water", "pos": [22, 3]}, "22;2": {"type": "left_side_water", "pos": [22, 2]}, "22;1": {"type": "top_right_angle", "pos": [22, 1]}, "22;0": {"type": "water", "pos": [22, 0]}, "22;9": {"type": "left_side_water", "pos": [22, 9]}, "22;10": {"type": "left_side_water", "pos": [22, 10]}, "0;8": {"type": "right_side_water", "pos": [0, 8]}, "0;9": {"type": "right_side_water", "pos": [0, 9]}, "22;22": {"type": "bottom_right_angle", "pos": [22, 22]}, "19;-1": {"type": "bottom_middle_water", "pos": [19, -1]}, "18;-1": {"type": "bottom_middle_water", "pos": [18, -1]}, "17;-1": {"type": "bottom_middle_water", "pos": [17, -1]}, "16;-1": {"type": "bottom_middle_water", "pos": [16, -1]}, "15;-1": {"type": "bottom_middle_water", "pos": [15, -1]}, "21;0": {"type": "water", "pos": [21, 0]}, "20;0": {"type": "water", "pos": [20, 0]}, "19;0": {"type": "water", "pos": [19, 0]}, "18;0": {"type": "water", "pos": [18, 0]}, "17;0": {"type": "water", "pos": [17, 0]}, "16;0": {"type": "water", "pos": [16, 0]}, "15;0": {"type": "water", "pos": [15, 0]}, "14;0": {"type": "water", "pos": [14, 0]}, "13;0": {"type": "water", "pos": [13, 0]}, "12;0": {"type": "water", "pos": [12, 0]}, "11;0": {"type": "water", "pos": [11, 0]}, "10;0": {"type": "water", "pos": [10, 0]}, "9;0": {"type": "water", "pos": [9, 0]}, "8;0": {"type": "water", "pos": [8, 0]}, "7;0": {"type": "water", "pos": [7, 0]}, "6;0": {"type": "water", "pos": [6, 0]}, "5;0": {"type": "water", "pos": [5, 0]}, "4;0": {"type": "water", "pos": [4, 0]}, "3;0": {"type": "water", "pos": [3, 0]}, "2;0": {"type": "water", "pos": [2, 0]}, "1;0": {"type": "water", "pos": [1, 0]}, "0;1": {"type": "top_left_angle", "pos": [0, 1]}, "21;1": {"type": "bottom_middle_water", "pos": [21, 1]}, "20;1": {"type": "bottom_middle_water", "pos": [20, 1]}, "19;1": {"type": "bottom_middle_water", "pos": [19, 1]}, "18;1": {"type": "bottom_middle_water", "pos": [18, 1]}, "17;1": {"type": "bottom_middle_water", "pos": [17, 1]}, "16;1": {"type": "bottom_middle_water", "pos": [16, 1]}, "15;1": {"type": "bottom_middle_water", "pos": [15, 1]}, "14;1": {"type": "bottom_middle_water", "pos": [14, 1]}, "13;1": {"type": "bottom_middle_water", "pos": [13, 1]}, "12;1": {"type": "bottom_middle_water", "pos": [12, 1]}, "11;1": {"type": "bottom_middle_water", "pos": [11, 1]}, "10;1": {"type": "bottom_middle_water", "pos": [10, 1]}, "9;1": {"type": "bottom_middle_water", "pos": [9, 1]}, "8;1": {"type": "bottom_middle_water", "pos": [8, 1]}, "7;1": {"type": "bottom_middle_water", "pos": [7, 1]}, "6;1": {"type": "bottom_middle_water", "pos": [6, 1]}, "5;1": {"type": "bottom_middle_water", "pos": [5, 1]}, "4;1": {"type": "bottom_middle_water", "pos": [4, 1]}, "3;1": {"type": "bottom_middle_water", "pos": [3, 1]}, "2;1": {"type": "bottom_middle_water", "pos": [2, 1]}, "1;1": {"type": "bottom_middle_water", "pos": [1, 1]}}

          # (switch maps) Go To The Next Map
          if event.key == pygame.K_SPACE: # Change The The Current Map By Space
            self.current_level += 1
            if len(os.listdir('Maps'))+1 <= self.current_level: # Check If any index error will happen
              self.current_level = 1
            self.current_level_map = f'Maps/map_{str(self.current_level)}.json'
            self.tile_map.load(self.current_level_map)
            pygame.display.set_caption('Mini-Golf-Editor (Map '+ str(self.current_level) + ')')

        if event.type == pygame.MOUSEBUTTONDOWN:
          # Left Mouse Button
          if event.button == 1:
            if 0 <= mpos[0] <= Editor.WIDTH: # The User Clicked On The Green Ground
              self.clicking = True
            else: # The User Clicked On The Side Bar
              for rect, key in self.side_bar_imgs_positions:
                if rect.collidepoint(mpos):
                  self.current_img = (self.assets[key], key)
          # Right Mouse Button
          if event.button == 3:
            self.right_clicking = True
          if event.button == 4 and self.side_bar_imgs_positions[0][0].y < 20:
            self.scroll_down = True
          if event.button == 5 and self.side_bar_imgs_positions[-1][0].y > Editor.HEIGHT-100:
            self.scroll_up = True
          if event.button == 2:
            print(pygame.mouse.get_pos()[0]//32, pygame.mouse.get_pos()[1]//32)

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.clicking = False
          if event.button == 3:
            self.right_clicking = False

      self.clock.tick(Editor.FPS)
      pygame.display.update()


mygame = Editor()
mygame.run()
