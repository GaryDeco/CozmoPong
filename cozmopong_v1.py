import pygame as pg
import numpy as np

pg.init()

#constants
WIDTH = 1280
HEIGHT = 960
SCREEN_SIZE = [WIDTH, HEIGHT]
FPS = 60
TITLE = 'CozmoPong'

# assign speeds
BALL_SPEED = 5
SET_PADDLE1_SPEED = 7
SET_AI_PADDLE_SPEED = 6

# assign keyboard buttons
# paddle 1 (left)
PAD1_UP_KEY = pg.K_w # w key
PAD1_DOWN_KEY = pg.K_s # s key

#---------------------------
#colors  RGB (R  , G  , B  )
#---------------------------
RGB = pg.Color
#---------------------------

BACKGROUND_COLOR = RGB('black')
fps_clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)
screen_size = np.array([WIDTH, HEIGHT])
pg.display.set_caption(TITLE)

# define flags
game_over = False

def get_paddle(surface, pad_size, side=None):
    '''
    Initialize an empty paddle object
    Params: get_paddle(surface, pad_size(list[x,y]), side=(Optional: 'left', 'right')
    No side parameter creates a paddle centered on left side of screen. 
    '''
    screen_size = np.array(surface.get_size())
    screen_size = [screen_size[0], screen_size[1]]
    screen_center = [int(xy/2) for xy in screen_size]
    pad_center = [int(xy/2) for xy in pad_size]
    if side is not None and side == "left":
        print(f"Adding left paddle at (x= {pad_size[0]}, y= {screen_center[1]-pad_center[1]})") 
        return pg.Rect(pad_size[0],
                       screen_center[1]-pad_center[1], 
                       pad_size[0], 
                       pad_size[1]
                      )
    elif side is not None and side == "right":
        print(f"Adding right paddle at (x= {screen_size[0]-int(2*pad_size[0])}, y= {screen_center[1] - pad_center[1]})")
        return pg.Rect(screen_size[0]-int(2*pad_size[0]),
                       screen_center[1] - pad_center[1], 
                       pad_size[0], 
                       pad_size[1]
                      ) 
    else:
        print(f"Adding left paddle at (x= {pad_size[0]}, y= {screen_center[1]-pad_center[1]})") 
        return pg.Rect(pad_size[0],
                       screen_center[1]-pad_center[1], 
                       pad_size[0], 
                       pad_size[1]
                      )

def draw_paddle(surface, color, paddle):
    '''
    Draws a paddle using pygame.Rect(). Mut be initialized with get_paddle()
    Params: set_paddle(surface(pygame.Suface), RGB_color(tuple), paddle_object)
            called in game loop. 
    '''
    pg.draw.rect(surface, RGB(color), paddle)
    
def get_ball(surface, ball_size):
    '''
    Initalize a ball in the center of the screen with the desired dimentions
    Params: get_ball(surface, ball_size(list[x,y]))
    Note: Uses pygame.Rect to create a rect object to draw ball
    '''
    screen_size = np.array(surface.get_size())
    screen_size = [screen_size[0], screen_size[1]]
    screen_center = [int(xy/2) for xy in screen_size]
    ball_center = [int(xy/2) for xy in ball_size]
    print(f"Adding ball to center at (x= {screen_center[0]-ball_center[0]}, y= {screen_center[1]- ball_center[1]})")
    return pg.Rect( 
                   screen_center[0]-ball_center[0], 
                   screen_center[1]- ball_center[1], 
                   ball_size[0], 
                   ball_size[1]
                  )

def animate_ball(ball):
    '''
    Set ball speed and collision boundaries
    '''
    global ball_speedx, ball_speedy
    
    ball.x += ball_speedx
    ball.y += ball_speedy
    
    if ball.top <=0 or ball.bottom >=screen_size[1]:
        ball_speedy *= -1
        
    if ball.left <=0 or ball.right >= screen_size[0]:
        ball_speedx *= -1
        
    if ball.colliderect(pad1) or ball.colliderect(pad2):
        ball_speedx *= -1


def draw_ball(surface, color, ball):
    '''
    Draw a ball center screen with the desired color
    Params: set_ball(surface, color(RGB_tuple), ball_object)
    called in game loop
    '''
    pg.draw.ellipse(surface, RGB(color), ball)

def animate_paddles():  
    pad1.y += PADDLE1_SPEED
    paddle_speed = SET_AI_PADDLE_SPEED
    if pad1.top <= 0:
        pad1.top = 0
    if pad1.bottom >= screen_size[1]:
        pad1.bottom = screen_size[1]
    # keep paddle within y axis screen limits
      
    # ai animation    
    if pad2.top < ball.y:
        pad2.y += SET_AI_PADDLE_SPEED
    if pad2.bottom > ball.y:
        pad2.y -= SET_AI_PADDLE_SPEED

    if pad2.top <= 0:
        pad2.top = 0
    if pad2.bottom >= screen_size[1]:
        pad2.bottom = screen_size[1]
        
        
print(f"Ball Speed set to {BALL_SPEED}")
print(f"Paddle 1 Speed set to {SET_PADDLE1_SPEED}")
print(f"AI speed set to {SET_AI_PADDLE_SPEED}")

# create paddles
pad1 = get_paddle(screen, [10,140], side='left')
pad2 = get_paddle(screen, [10,140], side='right')

# create ball
ball = get_ball(screen, [30, 30])

# set inital states
PADDLE1_SPEED = 0
ball_speedx = BALL_SPEED
ball_speedy = ball_speedx

############################## Game Loop ####################################

while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
            
        if event.type == pg.KEYDOWN:
            if event.key == PAD1_DOWN_KEY:
                    PADDLE1_SPEED += SET_PADDLE1_SPEED
            if event.key == PAD1_UP_KEY:
                    PADDLE1_SPEED -= SET_PADDLE1_SPEED
        if event.type == pg.KEYUP:
            if event.key == PAD1_DOWN_KEY:
                    PADDLE1_SPEED -= SET_PADDLE1_SPEED
            if event.key == PAD1_UP_KEY:
                    PADDLE1_SPEED += SET_PADDLE1_SPEED
     

    # fill screen background on each frame     
    screen.fill(BACKGROUND_COLOR) 
    
    # animate the ball and paddles
    animate_ball(ball)
    animate_paddles()

    #draw paddles and ball
    draw_paddle(screen, 'red', pad1)
    draw_paddle(screen, 'blue', pad2)
    draw_ball(screen, 'white', ball)
    
    pg.draw.aaline(screen, RGB('grey'), (screen_size[0] / 2, 0),(screen_size[0] / 2, screen_size[1]))
    
    # update the screen
    pg.display.flip()
    fps_clock.tick(FPS) 
    
pg.quit()

