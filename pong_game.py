# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 700
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    #initialize ball_pos at centre of table
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    #calculate random horizontal and vertical velocities    
    horizontal = random.randrange(120, 240) / 60
    vertical = random.randrange(60, 180) * -1 / 60

    #add randomization to ball velocity
    if(direction):
        ball_vel = [horizontal, vertical]
    else:
        ball_vel = [horizontal * -1, vertical]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    #reset the scores, and other variables
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    
    #call spawn_ball to initialize game
    spawn_ball(random.choice([LEFT, RIGHT]))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if(ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] *= -1
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #check if ball has touched gutter or paddle
    if(ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH):
        if((ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] *= -1 * 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    elif(ball_pos[0] - BALL_RADIUS <= PAD_WIDTH):
        if((ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] *= -1 * 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
  
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
                  
    # update paddle's vertical position, keep paddle on the screen
    if((paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT <= HEIGHT) and (paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT >= 0)):
        paddle1_pos += paddle1_vel
    if((paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT <= HEIGHT) and (paddle2_pos + paddle2_vel - HALF_PAD_HEIGHT >= 0)):
        paddle2_pos += paddle2_vel
    
    # draw paddles
    c.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)], 1, "Black", "White")
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)], 1, "Black", "White")
    
    # draw scores
    c.draw_text(str(score1), (WIDTH / 4, 100), 60, "White")
    c.draw_text(str(score2), (WIDTH / 4 * 3, 100), 60, "White")    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel = -3
    elif(key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 3
    elif(key == simplegui.KEY_MAP["up"]):
        paddle2_vel = -3
    elif(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]) or (key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 0
    elif(key == simplegui.KEY_MAP["up"]) or (key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 0

def restart_game():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

#instructions to play
blank_line = " "
instruction_title = "HOW TO PLAY"
player_1 = "To control the paddle on the left of your screen: use the 'w' and 's' keyboard keys to move your paddle up/down, respectively."
player_2 = "To control the paddle on the right of your screen: use the up/down arrow keys to move your paddle up/down, respectively."
restart = "If you would like to reset the game, simply click the Restart Game button below. This will reset the score"

label = frame.add_label(instruction_title)
label = frame.add_label(player_1)
label = frame.add_label(blank_line)
label = frame.add_label(player_2)
label = frame.add_label(blank_line)
label = frame.add_label(restart)

#restart button to start new game
restart = frame.add_button("Restart Game", restart_game)

# start frame
new_game()
frame.start()
