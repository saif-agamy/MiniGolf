import pygame
import sys
from utils import load_img, draw_background, Distance_2_points
from ball import ball
from tile_map import Tile_Map
import json


class game:
  # Class Level Attributes
  # Game settings 
  WIDTH = 720
  HEIGHT = 720
  FPS = 60
  

  def __init__(self):
    # setup pygame
    pygame.init()
    self.screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT))
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Mini-Golf')

    self.current_level = 5
    self.current_level_strikes = 0

    # texts
    self.MAIN_FONT = pygame.font.SysFont('comicsans', 30)
    
    # setup assets
    self.assets = {
      "black_tile": load_img("black_tile.png", set_color_key=False),
      "white_tile": load_img("white_tile.png"), 
      "ball": load_img('Golf_Ball_Body.png', .1),
      'hole': load_img('hole.png', .6),
      'start_screen': load_img('start_screen.png', set_color_key=False),

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

    self.current_level_map = f'Maps/map_{str(self.current_level)}.json'

    self.tile_map = Tile_Map(self)

    try: 
      self.tile_map.load(self.current_level_map)
    except FileNotFoundError:
      pass # Don't Load Any Thing No Map Is Going To Be Draw

    self.level_4_tiles_pos = [(6, 10), (8, 15), (4, 15), (3, 8), (9, 8), (6, 6), (8, 3), (20, 17), (17, 17), (16, 17), (20, 18), (18, 18)]
    self.level_4_magic_rects = [pygame.Rect(pos[0]*self.tile_map.tile_size, pos[1]*self.tile_map.tile_size, self.tile_map.tile_size, self.tile_map.tile_size) for pos in self.level_4_tiles_pos]

    self.level_5_pos = [(21, 7), (20, 7), (19, 7), (18, 7), (17, 7), (16, 7), (15, 7)] # This Positions If the ball reach this positions the hall will change its position and the player should go to another map to get the key 
    self.level_5_rects = [pygame.Rect(pos[0]*self.tile_map.tile_size, pos[1]*self.tile_map.tile_size, self.tile_map.tile_size, self.tile_map.tile_size) for pos in self.level_5_pos]

    self.gate_pos = [(17, 2), (18, 2), (19, 2)]
    self.gate_rects = [pygame.Rect(pos[0]*self.tile_map.tile_size, pos[1]*self.tile_map.tile_size, self.tile_map.tile_size, self.tile_map.tile_size) for pos in self.gate_pos]

    self.magic_dict = { # Level 4
      (6, 10): (10*self.tile_map.tile_size, 15*self.tile_map.tile_size),
      (8, 15): (2*self.tile_map.tile_size, 19*self.tile_map.tile_size),
      (4, 15): (10*self.tile_map.tile_size, 19*self.tile_map.tile_size),
      (3, 8): (3*self.tile_map.tile_size, 12*self.tile_map.tile_size),
      (9, 8): (9*self.tile_map.tile_size, 13*self.tile_map.tile_size),
      (6, 6): (6*self.tile_map.tile_size, 19*self.tile_map.tile_size),
      (8, 3): (6*self.tile_map.tile_size, 12*self.tile_map.tile_size),
      # The Next Tiles Is Tiles Is Near The Hole And All Of Them Will lead to the same place (4*self.tile_map.tile_size, 10*self.tile_map.tile_size),
      (20, 17): (4*self.tile_map.tile_size, 10*self.tile_map.tile_size),
      (17, 17): (4*self.tile_map.tile_size, 10*self.tile_map.tile_size),
      (16, 17): (4*self.tile_map.tile_size, 10*self.tile_map.tile_size),
      (20, 18): (4*self.tile_map.tile_size, 10*self.tile_map.tile_size),
      (18, 18): (4*self.tile_map.tile_size, 10*self.tile_map.tile_size)
    }

    #setup the ball
    self.beginning_ball_Loc = (100,100)
    for key in self.tile_map.tile_map :
      tile = self.tile_map.tile_map[key]
      if tile['type'] == "ball" :
        self.beginning_ball_Loc = tile['pos']
        self.beginning_ball_Loc = [self.beginning_ball_Loc[0] * self.tile_map.tile_size,self.beginning_ball_Loc[1] * self.tile_map.tile_size]
        del self.tile_map.tile_map[key]
        break
    self.myball = ball(self,self.beginning_ball_Loc,25,28)

    #mouse vars
    self.rightclicking = False

    f = open('best_strikes.json', 'r')
    self.best_strikes = json.load(f) # {level: best_score}
    f.close()

    self.collide_once = True # This Is Needed In Level 5

    self.starting_screen = True

  def lock_player(self): # This Function Is To Lock the Player in level 5
    tiles = {
      1: {
        "14; 10": {'type': "bottom_left_angle", 'pos': (14, 10)},
        "14;11": {'type': "top_left_angle", 'pos': (14, 11)}
        },
      2: {
        "15; 10": {'type': "top_middle_water", 'pos': (15, 10)},
        "15;11": {'type': "bottom_middle_water", 'pos': (15, 11)}
      },
      3: {
        "16; 10": {'type': "top_middle_water", 'pos': (16, 10)},
        "16;11": {'type': "bottom_middle_water", 'pos': (16, 11)}
      },
      4: {
        "17; 10": {'type': "top_middle_water", 'pos': (17, 10)},
        "17;11": {'type': "bottom_middle_water", 'pos': (17, 11)}
      },
      5: {
        "18; 10": {'type': "top_middle_water", 'pos': (18, 10)},
        "18;11": {'type': "bottom_middle_water", 'pos': (18, 11)}
      },
      6: {
        "19; 10": {'type': "top_middle_water", 'pos': (19, 10)},
        "19;11": {'type': "bottom_middle_water", 'pos': (19, 11)}
      },
      7: {
        "20; 10": {'type': "top_middle_water", 'pos': (20, 10)},
        "20;11": {'type': "bottom_middle_water", 'pos': (20, 11)}
      },
      8: {
        "21; 10": {'type': "top_middle_water", 'pos': (21, 10)},
        "21;11": {'type': "bottom_middle_water", 'pos': (21, 11)}
      },
      9: {
        "22; 10": {'type': "bottom_right_angle", 'pos': (22, 10)},
        "22;11": {'type': "top_right_angle", 'pos': (22, 11)}
      }
    }
    for num in tiles:
      pair_of_tiles = tiles[num]
      for pos in pair_of_tiles:
        self.tile_map.tile_map[pos] = pair_of_tiles[pos]
      
      self.tile_map.render(self.screen) # Refresh The Screen Each time we add two tiles
      self.myball.render(self.screen) # and the ball
      pygame.display.update() # Should Be Here

      pygame.time.wait(250) 

  def check_best_strikes(self):
    if self.best_strikes[str(self.current_level)] == 0 or self.current_level_strikes < self.best_strikes[str(self.current_level)]:
        self.best_strikes[str(self.current_level)] = self.current_level_strikes
        with open('best_strikes.json', 'w') as f:
            json.dump(self.best_strikes, f)

  def save() :
    pass

  def start_screen(self):
    while self.starting_screen:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          self.starting_screen = False
          break
      
      img = self.assets['start_screen'].copy()
      img.set_alpha(5)
      self.screen.blit(img, (0,0))

      welcom_text = self.MAIN_FONT.render('Welcome To My Mini-Golf Game!', 1, 'black')
      levels_text = self.MAIN_FONT.render('This Game Is 5 Levels Try to Beat All Best Strikes In Each Level!', 1, 'black')
      press_text = self.MAIN_FONT.render('Press Any Button To Start', 1, 'black')
      level1 = self.MAIN_FONT.render('lv1: You Need To Warmup!', 1, 'black')
      level2 = self.MAIN_FONT.render('lv2: I Think You\'re Ready.', 1, 'black')
      level3 = self.MAIN_FONT.render('lv3: I Will Trick You', 1, 'black')
      level4 = self.MAIN_FONT.render('lv4: Don\'t Trust All The Walls!!', 1, 'black')
      level5 = self.MAIN_FONT.render('lv5: I\'ll Lock You', 1, 'black')
      self.screen.blit(welcom_text, (game.WIDTH/2-welcom_text.get_width()/2, 100))
      self.screen.blit(levels_text, (5, 200))

      self.screen.blit(level1, (game.WIDTH/2-level1.get_width()/2, 300))
      self.screen.blit(level2, (game.WIDTH/2-level1.get_width()/2, 350))
      self.screen.blit(level3, (game.WIDTH/2-level1.get_width()/2, 400))
      self.screen.blit(level4, (game.WIDTH/2-level1.get_width()/2, 450))
      self.screen.blit(level5, (game.WIDTH/2-level1.get_width()/2, 500))

      self.screen.blit(press_text, (game.WIDTH/2-press_text.get_width()/2, 600))

      pygame.display.update()

  def run(self):
    while True:

      self.screen.fill((141, 196, 53)) # Change The Background To This Color To Match The assets

      # Draw Tiles (Walls, Decors, etc..)
      self.tile_map.render(self.screen)

      # Just When The Player Start The Game
      self.start_screen()

      # text setup
      if self.current_level <= 5:
        level_text = self.MAIN_FONT.render('Level: '+str(self.current_level), 1, 'black')
        strikes_text = self.MAIN_FONT.render('Strikes: '+str(self.current_level_strikes), 1, 'black')
        best_score = self.MAIN_FONT.render('Best: '+str(self.best_strikes[str(self.current_level)]), 1, 'black')
        self.screen.blit(level_text, (10, 0))
        self.screen.blit(strikes_text, (self.WIDTH/2-strikes_text.get_width()/2, 0))
        self.screen.blit(best_score, (game.WIDTH-best_score.get_width()-6, 0))
      else:
        pygame.display.update()
        pygame.time.wait(3000)
        break # Break The Game

      #setup the ball 
      next_level = self.myball.update() # If The Ball Is In The Hole .update() will return True

      if next_level:
        # Check If Player Hit The Record
        self.check_best_strikes()

        # Next Level setup
        self.current_level_strikes = 0
        self.current_level += 1
        self.current_level_map = f'Maps/map_{str(self.current_level)}.json'
        self.tile_map.load(self.current_level_map)

        # Set The Ball Position To its respawn in the map
        for key in self.tile_map.tile_map:
          tile = self.tile_map.tile_map[key]
          if tile['type'] == 'ball':
            self.myball.strike_pos = [tile['pos'][0] * self.tile_map.tile_size, tile['pos'][1] * self.tile_map.tile_size]
            self.myball.pos = [tile['pos'][0] * self.tile_map.tile_size, tile['pos'][1] * self.tile_map.tile_size]
            del self.tile_map.tile_map[key] # Remove The Tile Which Is Fixed
            break
      
      # Level 3 Conditions
      if self.current_level == 3: 
        ball_pos = (self.myball.pos[0]//self.tile_map.tile_size, self.myball.pos[1]//self.tile_map.tile_size)
        # gates
        if ball_pos in [(17, 0), (18, 0)]:
          self.myball.pos = [17*self.tile_map.tile_size, 20*self.tile_map.tile_size]
          self.myball.velocity[1] *= -1
        if ball_pos in [(22, 5), (22, 6)]:
          self.myball.pos = [0, 19*self.tile_map.tile_size]
      
      # Level 4 Conditions
      if self.current_level == 4:
        for rect in self.level_4_magic_rects: # Magic Walls
          rect_pos = (rect.x // self.tile_map.tile_size, rect.y // self.tile_map.tile_size)
          if self.myball.Ball_Rect().colliderect(rect):
            self.myball.pos = list(self.magic_dict[rect_pos])
            self.myball.velocity = [0, 0]

      # Level 5 Conditions
      if self.current_level == 5:
        if self.collide_once:
          if self.myball.Ball_Rect().collidelist(self.level_5_rects) != -1:
            # Change Hole Position
            self.tile_map.change_hole_pos((5, 20))
            self.collide_once = False
            self.myball.velocity = [0, 0]
            self.lock_player()

        if self.myball.pos[0] < 0:
          self.myball.reset()

        if self.myball.Ball_Rect().collidelist(self.gate_rects) != -1:
          self.myball.pos = [1*self.tile_map.tile_size, 19*self.tile_map.tile_size]
          self.myball.velocity = [0, 0]

      self.myball.render(self.screen)

      #mouse func
      if self.rightclicking:     
        self.myball.mark(pygame.mouse.get_pos())

      #exit the game
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN: 
          if event.key == pygame.K_ESCAPE: # If User Clicked On Escape Key He Will Quit Too, Because I'm Too Laze To Move My Hand To Get The Mouse 😅
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1 and not(self.myball.moving): # and the ball is not moving
            if Distance_2_points(pygame.mouse.get_pos(),self.myball.centerPoint) <= self.myball.ball_radius :
              self.rightclicking = True

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1 :
              if self.rightclicking :
                self.myball.shoot(pygame.mouse.get_pos())
                self.current_level_strikes += 1
              self.rightclicking = False

      self.clock.tick(game.FPS)
      pygame.display.update()


mygame = game()
mygame.run()
