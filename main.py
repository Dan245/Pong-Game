# import the necessary modules
import pygame
import sys
from random import uniform
from math import sqrt
 
#initialize pygame
pygame.init()
screen = pygame.display.set_mode((500, 300), pygame.NOFRAME)
pygame.display.set_caption("Template")

clock = pygame.time.Clock()
FPS = 60   # set the frames per second 

# define colours you will be using
WHITE = (255, 255, 255)
GREEN = (0,204,0)
ORANGE = (255,165,0)
BLUE = (0,165,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
CYAN = (0, 255, 255)

# init fonts
title_font = pygame.font.Font("bit5x3.ttf",round(screen.get_width()/7.5+screen.get_height()/7.5))
sub_font = pygame.font.Font("bit5x3.ttf",round(screen.get_width()/30+screen.get_height()/30))
main_font = pygame.font.Font("bit5x3.ttf",round(screen.get_width()/15+screen.get_height()/15))
sub_font = pygame.font.Font("bit5x3.ttf",round(screen.get_width()/30+screen.get_height()/30))

# ball class
class Ball:
  # init vars that are the same for every ball (class vars)
  s = screen
  c = WHITE
  def __init__(self): # init stuff that is unique to each object
    self.r = round(screen.get_width()/100) + round(screen.get_height()/100)
    self.x = screen.get_width()/2
    self.y = uniform(screen.get_height()/4, screen.get_height()/4*3)
    self.circle = (self.x, self.y)
    self.min_speed = 2
    self.max_speed = 10
    self.cur_speed = self.min_speed
    self.xDir = 1
    self.dx = self.cur_speed*self.xDir
    self.iy = 8
    self.dy = uniform(1, -1)

  # draw the ball
  def draw(self, win):
    pygame.draw.circle(win, self.c, self.circle, self.r)
  
  # reset the speed and location of ball
  def reset(self):
    self.x = screen.get_width()/2
    self.y = uniform(screen.get_height()/4, screen.get_height()/4*3)
    self.circle = (self.x, self.y)
    self.cur_speed = self.min_speed
    self.xDir = 1
    self.dx = self.cur_speed*self.xDir
  
  # check if the ball is in contact with the edges of the screen. If it hits the left or right edge, add a point to whoever scored, and reset the ball
  def keep_inbounds(self, win, p1, p2):
    s_w = win.get_width()
    s_h = win.get_height()
    if self.x + self.r >= s_w:
      self.reset()
      p1.score += 1
    elif self.x - self.r <= 0:
      self.reset()
      p2.score += 1
    if self.y - self.r <= 0:
      self.y = 0 + self.r
    elif self.y + self.r >= s_h:
      self.y = s_h - self.r
  
  # move the ball, and call functions to determine how the ball moves
  def move(self, win, p1, p2):
      self.x += self.dx
      self.y += self.dy
      self.circle = (self.x, self.y)
      self.keep_inbounds(win, p1, p2)
      self.bounce_ball(win)

  # bounce ball off edges of the screen
  def bounce_ball(self, win):
    s_w = win.get_width()
    s_h = win.get_height()
    if self.x == s_w - self.r or self.x == 0 + self.r:
      self.xDir = self.xDir*-1
    if self.y == s_h - self.r or self.y == 0 + self.r:
      self.dy = self.dy*-1


# player class
class Player():
    def __init__(self, x, y, w, h, c, ctrls): # initing object vars
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.rect = (x,y,w,h)
        self.vel = 4
        self.ctrls = ctrls
        self.score = 0

    # draw player
    def draw(self, win):
        pygame.draw.rect(win, self.c, self.rect)

    # move player based on their keys pressed, and snure they stay inbounds
    def move(self, win):
        keys = pygame.key.get_pressed()
        if keys[self.ctrls[0]]:
            self.y -= self.vel
        if keys[self.ctrls[1]]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.w, self.h)
        self.keep_inbounds(win)

    # check if player is in contact with the edges of the screen, and ensure they don't surpass it
    def keep_inbounds(self, win):
      s_w = win.get_width()
      s_h = win.get_height()
      if self.x + self.w >= s_w:
        self.x = s_w - self.w
      elif self.x <= 0:
        self.x = 0
      if self.y <= 0:
        self.y = 0
      elif self.y + self.h >= s_h:
        self.y = s_h - self.h
      self.rect = (self.x, self.y, self.w, self.h)

# check hit between rect and circle
def hitDetection(rect, circle):
  center_x = circle.x
  center_y = circle.y
  x = []
  y = []
  # get every possible point on a rect (per pixel)
  for i in range(int(rect.w)):
    x.append(rect.x + i)
  for i in range(int(rect.h)):
    y.append(rect.y + i)
  
  # check distance between each point and center point of the circle
  for i in x:
    for j in y:
      if circle.r > get_distance(i, j, center_x, center_y):
        # if they are colliding, bounce the ball off the paddle
        if circle.dx > 0:
          circle.x = rect.x - circle.r
        else:
          circle.x = rect.x + rect.w + circle.r
        
        circle.dy = circle.iy*((circle.y - rect.y-rect.h/2) / rect.h) # change dy based on where it hit the paddle (allows for some strategy)
        circle.dx = circle.dx * 1.1 if circle.dx * 1.1 <= circle.max_speed else circle.max_speed # slowly increase speed of ball
        return True
  return False

# get distance between 2 points
def get_distance(x1, y1, x2, y2):
  return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# display a given text with a given font, color and position
def display_text(win, string, font, color, center_x, center_y):
  text = font.render(string, True, color)
  
  rect = text.get_rect()
  rect.center = (center_x, center_y)

  win.blit(text, rect)

# getting screen dimensions
screen_width = screen.get_width()
screen_height = screen.get_height()
print(screen_width, screen_height)

# width and height of paddles
paddle_w = screen_width/60
paddle_h = screen_height/5

# setting up the different objects
p1 = Player(0+paddle_w*2, screen_height/2 - paddle_h/2, paddle_w, paddle_h, BLUE, [pygame.K_w, pygame.K_s])
p2 = Player((screen_width-paddle_w)-paddle_w*2, screen_height/2 - paddle_h/2, paddle_w, paddle_h, ORANGE, [pygame.K_UP, pygame.K_DOWN])
ball = Ball()

# initing bools
play = False
main = True

# main game loop
while main:
    for event in pygame.event.get():
        # if player wants to quit
        if event.type == pygame.QUIT:
            main = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
              main = False
              continue

    # init stuff
    clock.tick(FPS)                        
    screen.fill(BLACK)

    # if playing the main game
    if play:

      # line in the middle
      line_w = screen_width/120
      line_h = screen_height
      pygame.draw.rect(screen, WHITE, (screen_width/2 - line_w/2, 0, line_w, line_h))

      # if no one has won yet
      if p1.score < 10 and p2.score < 10:

        # move both players
        p1.move(screen)
        p2.move(screen)

        # move ball
        ball.move(screen, p1, p2)

        # check if ball hits either of the paddles
        if hitDetection(p1, ball) or hitDetection(p2, ball):
          #flip direction if so
          ball.dx = ball.dx*-1
        # draw the ball
        ball.draw(screen)
      else: # if someone won

        # display winning text (on the screen of whoever won) and user options
        display_text(screen, "Winner!", main_font, WHITE, screen_width/4 if p1.score == 10 else screen_width/4*3, screen_height/2)
        display_text(screen, "Play Again [SPACE]", sub_font, WHITE, screen_width/4 if p1.score != 10 else screen_width/4*3, screen_height/2)
        display_text(screen, "Quit [Q]", sub_font, WHITE, screen_width/4 if p1.score != 10 else screen_width/4*3, screen_height/8*5)
        # grab current keys being pressed
        keys = pygame.key.get_pressed()
        # if space is being presed, reset the score and start again
        if keys[ord(' ')]:
          p1.score = 0
          p2.score = 0
          play = True
      # display score text
      display_text(screen, str(p1.score), main_font, WHITE, screen_width/4, screen_height/8)
      display_text(screen, str(p2.score), main_font, WHITE, screen_width/4*3, screen_height/8)

      # draw both paddles
      p1.draw(screen)
      p2.draw(screen)
    else: # if on title screen (not playing game)

      # display title and options texts
      display_text(screen, "PONG", title_font, WHITE, screen_width/2, screen_height/4)

      display_text(screen, "PLAY [SPACE]", sub_font, WHITE, screen_width/2, screen_height/2)

      display_text(screen, "QUIT [Q]", sub_font, WHITE, screen_width/2, screen_height/8*5)

      # grab current keys being pressed
      keys = pygame.key.get_pressed()
      # if space is being pressed, start the game
      if keys[ord(' ')]:
        play = True


    # update screen
    pygame.display.flip()
    
# quit pygame
pygame.quit()
# quit python script
sys.exit()