import pygame as pg
import numpy as np
import random as rand 
import os

pg.init()

#constants
WIDTH = 1280
HEIGHT = 960
SCREEN_SIZE = [WIDTH, HEIGHT]
SCREEN_CENTER = [int(xy/2) for xy in SCREEN_SIZE]
FPS = 60
TITLE = 'CozmoPong!'

# assign speeds
BALL_SPEED = 5
SET_PADDLE1_SPEED = 7
SET_AI_PADDLE_SPEED = 6

# set max score
MAX_SCORE = 5

# assign keyboard buttons
# paddle 1 (left)
PAD1_UP_KEY = pg.K_w # w key
PAD1_DOWN_KEY = pg.K_s # s key

# Sound effects volume (0-10)
PLAYER_SCORED = 2
PADDLE_STRIKE = 8

#---------------------------
#colors  RGB (R  , G  , B  )
#---------------------------
RGB = pg.Color
#---------------------------

BACKGROUND_COLOR = RGB('black')
fps_clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)
screen_size = np.array([WIDTH, HEIGHT])
pg.display.set_caption(TITLE + " FPS: " + str(fps_clock.get_fps()))


# define flags
game_over = False

# set initial score
PAD1_SCORE = 0
PAD2_SCORE = 0

def get_paddle(surface, pad_size, side):
    '''
    Initialize an empty paddle object
    Params: get_paddle(surface, pad_size(list[x,y]), side=(Optional: 'left', 'right')
    No side parameter creates a paddle centered on left side of screen. 
    '''
    screen_size = np.array(surface.get_size())
    screen_size = [screen_size[0], screen_size[1]]
    screen_center = [int(xy/2) for xy in screen_size]
    pad_center = [int(xy/2) for xy in pad_size]
    if side  == "left":
        print(f"Adding left paddle at (x= {pad_size[0]}, y= {screen_center[1]-pad_center[1]})") 
        return pg.Rect(pad_size[0],
                       screen_center[1] - pad_center[1], 
                       pad_size[0], 
                       pad_size[1]
                      )
    elif side  == "right":
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

def ball_start():
	global ball_speedx, ball_speedy

	ball.center = (SCREEN_CENTER[0],SCREEN_CENTER[1]) 
	ball_speedy *= rand.choice((1,-1))
	ball_speedx *= rand.choice((1,-1))  

def animate_ball(ball):
    '''
    Set ball speed and collision boundaries
    '''
    global ball_speedx, ball_speedy, PAD1_SCORE, PAD2_SCORE
    
    ball.x += ball_speedx
    ball.y += ball_speedy

 

    if ball.top <=0 or ball.bottom >=screen_size[1]:
        ball_speedy *= -1
        
    if ball.left <=0: 
        score.set_volume(PLAYER_SCORED/10)
        play_sound(score)
        ball_start()
        PAD2_SCORE += 1


    if ball.right >= screen_size[0]:
        score.set_volume(PLAYER_SCORED/10)
        play_sound(score)
        ball_start()
        PAD1_SCORE +=1

        
    if ball.colliderect(pad1) or ball.colliderect(pad2):
        pad_strike.set_volume(PADDLE_STRIKE/10)
        play_sound(pad_strike)
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
      
    # ai animation    
    if pad2.top < ball.y:
        pad2.y += SET_AI_PADDLE_SPEED
    if pad2.bottom > ball.y:
        pad2.y -= SET_AI_PADDLE_SPEED

    if pad2.top <= 0:
        pad2.top = 0
    if pad2.bottom >= screen_size[1]:
        pad2.bottom = screen_size[1]
        
def draw_scores():
    global PAD1_SCORE, PAD2_SCORE, p1_win, p2_win

    MSG1 = PAD1_SCORE
    MSG2 = PAD2_SCORE
    p1_win = False
    p2_win = False
    COLOR1 = 'red'
    COLOR2 = 'blue'

    if PAD1_SCORE < 10:
        p1_offset = 20
    else:
        p1_offset = 35
    p2_offset = 7

    if PAD1_SCORE == MAX_SCORE:
        MSG1 = 'WIN'
        MSG2 = 'LOSE'
        COLOR1 = 'green'
        COLOR2 = 'red'
        pg.time.delay(1000)
        screen.fill(BACKGROUND_COLOR) 
        draw_paddle(screen, 'red', pad1)
        draw_paddle(screen, 'blue', pad2)
        draw_centerline()
        pad1_text = game_font.render(f"{MSG1}", False, RGB(COLOR1))
        pad2_text = game_font.render(f"{MSG2}", False, RGB(COLOR2))
        screen.blit(pad1_text, (SCREEN_CENTER[0] - p1_offset - 40, SCREEN_CENTER[1]) )
        screen.blit(pad2_text, (SCREEN_CENTER[0] + p2_offset, SCREEN_CENTER[1]) )
        pg.display.flip() # have to update here because we are stuck in this loop 
        pg.time.delay(1000)
        PAD1_SCORE = 0
        PAD2_SCORE = 0

    if PAD2_SCORE == MAX_SCORE:
        MSG1 = 'LOSE'
        MSG2 = 'WIN'
        COLOR1 = 'red'
        COLOR2 = 'green'
        pg.time.delay(1000)
        screen.fill(BACKGROUND_COLOR) 
        draw_paddle(screen, 'red', pad1)
        draw_paddle(screen, 'blue', pad2)
        draw_centerline()
        pad1_text = game_font.render(f"{MSG1}", False, RGB(COLOR1))
        pad2_text = game_font.render(f"{MSG2}", False, RGB(COLOR2))
        screen.blit(pad1_text, (SCREEN_CENTER[0] - p1_offset - 60, SCREEN_CENTER[1]) )
        screen.blit(pad2_text, (SCREEN_CENTER[0] + p2_offset, SCREEN_CENTER[1]) )
        pg.display.flip() # have to update here because we are stuck in this loop 
        pg.time.delay(1000)
        PAD1_SCORE = 0
        PAD2_SCORE = 0
    else:
        pad1_text = game_font.render(f"{MSG1}", False, RGB(COLOR1))
        pad2_text = game_font.render(f"{MSG2}", False, RGB(COLOR2))
        screen.blit(pad1_text, (SCREEN_CENTER[0] - p1_offset, SCREEN_CENTER[1]) )
        screen.blit(pad2_text, (SCREEN_CENTER[0] + p2_offset, SCREEN_CENTER[1]) )

def draw_centerline():
    pg.draw.aaline(screen, RGB('grey'), (screen_size[0] / 2, 0),(screen_size[0] / 2, screen_size[1]))

def play_music(music, loop):

    basedir = os.getcwd()
    filedir = (str(basedir) + "\\assets\\music\\")
    path_to_file = (str(filedir) + str(music) + ".mp3")
    music = pg.mixer.music.load(path_to_file)
    pg.mixer.music.play(loop)

def get_sound(sound):

    basedir = os.getcwd()
    filedir = (str(basedir) + "\\assets\\sound\\")
    path_to_file = (str(filedir) + str(sound) + ".mp3")
    return pg.mixer.Sound(path_to_file)

def play_sound(sound):
    pg.mixer.Sound.play(sound)



print(f"Ball Speed set to {BALL_SPEED}")
print(f"Paddle 1 Speed set to {SET_PADDLE1_SPEED}")
print(f"AI speed set to {SET_AI_PADDLE_SPEED}")

# scale the paddles and ball to screen size
pad_size = [int(SCREEN_SIZE[0]*0.008), int(SCREEN_SIZE[1]*0.15)]
ball_size = [int(SCREEN_SIZE[0]*0.02), int(SCREEN_SIZE[0]*0.02)]

# create paddles and ball
pad1 = get_paddle(screen, pad_size, side='left')
pad2 = get_paddle(screen, pad_size, side='right')

ball = get_ball(screen, ball_size)

# set inital states
PADDLE1_SPEED = 0

# add text font
game_font = pg.font.Font(None, 40)

ball_speedx = BALL_SPEED * rand.choice((1, -1))
ball_speedy = ball_speedx * rand.choice((1, -1))

#play background music and get sound effects
play_music('bkg_music1', loop=True)
score = get_sound('score')
pad_strike = get_sound('pad_strike')

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
    
    # draw center line
    draw_centerline()

    #draw text
    draw_scores()
    
    # update the screen and add FPS display out of curiousity
    pg.display.set_caption(TITLE + " FPS: " + str(round(fps_clock.get_fps(),2)))
    pg.display.flip()
    fps_clock.tick(FPS) 

###########################################################################
    
pg.quit()

