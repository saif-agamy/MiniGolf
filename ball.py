import pygame
import math
from utils import Distance_2_points


class ball:
  # class level attributes
  RECTS_AROUND = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(0,0)]
  REDUCING_RATE = 0.04
  STOP_SPEED = 0.15
  SHOOT_POWER = 2.5

  def __init__(self, game, pos, ball_Size, radius):
    # ball setup
    self.game = game
    self.pos = list(pos)
    self.velocity = [0, 0]
    self.ball_Size = ball_Size
    # self.start_Pos = list(pos)
    self.strike_pos = list(pos) # when the ball stop in valid position i will set this variable to new position
    self.centerPoint = [
        self.pos[0] + self.ball_Size / 2,
        self.pos[1] + self.ball_Size / 2,
    ]
    self.moving = False  # To Don't Move The Ball Unless The Ball Stop

    # ball collision setup
    self.ball_radius = radius



  def Ball_Rect(self) :
    return pygame.Rect(self.pos[0],self.pos[1],self.ball_Size,self.ball_Size)
  
  def interact_circle(self,surface, color, center, radius, alpha) :
    temp_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(temp_surface, color + (alpha,), (radius, radius), radius)
    surface.blit(temp_surface, (center[0] - radius, center[1] - radius))

  def rects_around(self,ball_Location):
    tile_around = {
      'water' : [],
      'wall' : [],
      'dirt' : [],
      'hole' : [],
      'ball' : []
    } #here we gonna save the rects
    #convert pixels to tiles as location
    ball_Location_Tiles = (int(ball_Location[0] // self.game.tile_map.tile_size),int(ball_Location[1] // self.game.tile_map.tile_size))
    for Pos in self.RECTS_AROUND :
      for key in self.game.tile_map.tile_map :
          tile = self.game.tile_map.tile_map[key]
          if tuple(tile['pos']) == (Pos[0] + ball_Location_Tiles[0],Pos[1] + ball_Location_Tiles[1]) :
            if tile['type'] == 'ball' :   
              tile_around['ball'].append(pygame.Rect(tile['pos'][0] * self.game.tile_map.tile_size,tile['pos'][1] * self.game.tile_map.tile_size,self.game.tile_map.tile_size,self.game.tile_map.tile_size))
            elif tile['type'] == 'hole' :
               tile_around['hole'].append(pygame.Rect(tile['pos'][0] * self.game.tile_map.tile_size,tile['pos'][1] * self.game.tile_map.tile_size,self.game.tile_map.tile_size,self.game.tile_map.tile_size))
            elif tile['type'] in ['white_wall' , 'white_wall_left' , 'white_wall_right' , 'gate' , 'left_edge', 'right_edge', "black_tile","white_tile","black_wall", "left_black_wall" , "right_black_wall" , "middle_left_wall" , "middle_right_wall" , "middle_black_wall"] :
               tile_around['wall'].append(pygame.Rect(tile['pos'][0] * self.game.tile_map.tile_size,tile['pos'][1] * self.game.tile_map.tile_size,self.game.tile_map.tile_size,self.game.tile_map.tile_size))
            elif tile['type'] in ['dirt_top_right_dirt','top_left_dirt','right_side_dirt','left_side_dirt','bottom_left_dirt','bottom_middle_dirt','bottom_right_dirt','top_middle_dirt'] :
               tile_around['dirt'].append(pygame.Rect(tile['pos'][0] * self.game.tile_map.tile_size,tile['pos'][1] * self.game.tile_map.tile_size,self.game.tile_map.tile_size,self.game.tile_map.tile_size))
            elif tile['type'] in ['water','top_right_water','top_left_water','right_side_water','left_side_water','bottom_left_water','bottom_middle_water','bottom_right_water','top_middle_water'] :
               tile_around['water'].append(pygame.Rect(tile['pos'][0] * self.game.tile_map.tile_size,tile['pos'][1] * self.game.tile_map.tile_size,self.game.tile_map.tile_size,self.game.tile_map.tile_size))
    return tile_around
    

  def update(self):
    # print(self.REDUCING_RATE)
  #reset reducing rate
    self.REDUCING_RATE = 0.04

  # draw the circle hitbox
    if not self.moving :
        self.interact_circle(self.game.screen, (1, 50, 32), self.centerPoint, self.ball_radius, 128)

    self.centerPoint = [
        self.pos[0] + self.ball_Size / 2,
        self.pos[1] + self.ball_Size / 2,
    ]

    #bounce the ball 
    bounce_str = 0.7
    for key in self.rects_around(self.pos) :
      rects_dict = self.rects_around(self.pos)

      if key == 'wall' :
        if len(rects_dict[key]) > 0 :
          for rect in rects_dict[key] :
            if self.Ball_Rect().colliderect(rect):
                  ball_rect = self.Ball_Rect()
                  # Calculate overlap on each axis
                  # Find the leftmost and rightmost edges of the overlap
                  left_edge = max(ball_rect.left, rect.left)
                  right_edge = min(ball_rect.right, rect.right)
                  overlap_x = right_edge - left_edge  # How much they overlap horizontally

                  # Find the topmost and bottommost edges of the overlap
                  top_edge = max(ball_rect.top, rect.top)
                  bottom_edge = min(ball_rect.bottom, rect.bottom)
                  overlap_y = bottom_edge - top_edge  # How much they overlap vertically
                  # Bounce on the axis with the least overlap
                  if abs(overlap_x) < abs(overlap_y):
                      # Horizontal collision (left/right wall)
                      if self.velocity[0] != 0:
                          self.velocity[0] = -self.velocity[0] * bounce_str
                      # Move ball out of collision (if the ball is on the left move it more in left and if its on the right move it more to right)
                      if ball_rect.centerx < rect.centerx:
                          self.pos[0] -= abs(overlap_x)
                      else:
                          self.pos[0] += abs(overlap_x)
                  else:
                      # Vertical collision (top/bottom wall)
                      if self.velocity[1] != 0:
                          self.velocity[1] = -self.velocity[1] * bounce_str
                      # Move ball out of collision
                      if ball_rect.centery < rect.centery:
                          self.pos[1] -= abs(overlap_y)
                      else:
                          self.pos[1] += abs(overlap_y)
  
      elif key == 'water' :
        if len(rects_dict[key]) > 0:
          for rect in rects_dict[key]:
              ball_rect = self.Ball_Rect()
              # Calculate intersection area
              intersection = ball_rect.clip(rect)
              intersection_area = intersection.width * intersection.height
              ball_area = ball_rect.width * ball_rect.height
              # If more than half the ball is inside the water tile, sink it
              if intersection_area > ball_area * 0.5:
                  self.reset()
                  break  # No need to check other water tiles
      
      elif key == 'dirt':
        if len(rects_dict[key]) > 0 :
          for rect in rects_dict[key] :
              if self.Ball_Rect().colliderect(rect) :
                ball_rect = self.Ball_Rect()

                lowerRight = min(ball_rect.right , rect.right)
                highestLeft = max(ball_rect.left , rect.left)
                overlap_x = lowerRight - highestLeft

                lowerbottom = min(ball_rect.bottom , rect.bottom)
                highesttop = max(ball_rect.top , rect.top)
                overlap_y = lowerbottom - highesttop

                if abs(overlap_x) < abs(overlap_y) :
                    if abs(overlap_x) > self.game.tile_map.tile_size / 3 :
                      self.REDUCING_RATE = 0.3

                else : 
                  if abs(overlap_y) > self.game.tile_map.tile_size / 3 :
                    self.REDUCING_RATE = 0.3

      elif key == 'hole':
        for rect in rects_dict[key]: # There's just one key so i think we don't need a loop here but i will change it later just focus on making the code work for now
          rect.width += 10
          rect.height += 10
          ball_rect = self.Ball_Rect()
          intersection = ball_rect.clip(rect)
          # Calculate The Ball And Intersection Areas To Compare them 
          intersection_area = intersection.width * intersection.height
          ball_area = ball_rect.width * ball_rect.height
          # if the intersection area is bigger than or equal ball intersection that mean the ball is in the hall
          if intersection_area >= ball_area: # The Ball Is In The Hole
            self.velocity = [0,0]
            return True # The Player Won (The Ball Is In The Hole)

    # reducing ball speed
    speed = math.hypot(self.velocity[0], self.velocity[1])

    if speed > self.STOP_SPEED:  # Slowing The Ball (Ball Is Moving)
      self.velocity[0] -= self.REDUCING_RATE * (self.velocity[0] / speed)
      self.velocity[1] -= self.REDUCING_RATE * (self.velocity[1] / speed)
      self.moving = True
    else:  # The Ball Is Stopped
      self.velocity = [0, 0]
      self.moving = False
      self.strike_pos = list(self.pos)

    self.pos[0] = self.pos[0] + self.velocity[0]
    self.pos[1] = self.pos[1] + self.velocity[1]

  def mark(self, mousePos):
      Dist = Distance_2_points(mousePos, self.centerPoint)
      green = max(0, 255 - Dist)
      red = min(255, 0 + Dist)
      pygame.draw.line(
          self.game.screen, (red, green, 0), self.centerPoint, mousePos, 3
      )

  def shoot(self, mousePos):
      Xdist = mousePos[0] - self.centerPoint[0]
      Ydist = mousePos[1] - self.centerPoint[1]
      self.decreaseRate = 0
      self.velocity[0] = (Xdist / 100) * -self.SHOOT_POWER
      self.velocity[1] = (Ydist / 100) * -self.SHOOT_POWER

  def render(self, screen):
      screen.blit(self.game.assets["ball"], self.pos)

  def reset(self):
    self.pos = list(self.strike_pos)
    self.velocity = [0, 0]
    self.moving = False
