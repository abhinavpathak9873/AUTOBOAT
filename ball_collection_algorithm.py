import random
import numpy as np
import math
import pygame
import sys

#balls = [("red", (1, 1), 0), ("red", (7, 7), 1), ("red", (-4, 4), 2), ("red", (-6, 3), 3),
#         ("blue", (3, 2), 4), ("blue", (1, 6), 5), ("blue", (-2, 2), 6), ("green", (6, 1), 7),
#         ("green", (4, 5), 8), ("green", (-4, 6), 9), ("green", (-6, 7), 10), ("yellow", (5, 3), 11),
#         ("yellow", (2, 4), 12), ("yellow", (3, 7), 13), ("yellow", (-3, 5), 14), ("yellow", (-7, 5), 15)]

scores = []

pygame.init()
# Set up display
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IFOR CB 23 Simulator")
background_color = (69, 212, 255)


# Define colors and weights
colors = ["red", "blue", "green", "yellow"]
weights = {"red": -1, "blue": 1, "green": 3, "yellow": 2}

# Add two additional circles
extra_circles = [((30.5, 30.5), (0, 150, 45),(128, 0, 128)), ((30.5,769.5), (0, 150, 45),(128, 0, 128))]

# Player position and field of view angle
player_position = (0, 400)
robot_size = (60,30)
fov_angle = 70  # in degrees

# Function to check if a ball is within the field of view

def is_in_field_of_view(ball_position):
    angle_to_ball = math.degrees(math.atan2(ball_position[1] - (player_position[1]+robot_size[1]*0.5), ball_position[0] - (player_position[0]+robot_size[0])))
    angle_difference = abs(angle_to_ball)
    return angle_difference <= fov_angle / 2
# Function to draw the field of view
def draw_field_of_view():
    fov_color = (255, 255, 255)
    fov_radius = 100  # Adjust the radius as needed
    fov_start_angle = math.radians(-fov_angle / 2)
    fov_end_angle = math.radians(fov_angle / 2)
    start_pos = (robot_x(), robot_y())
    end_pos_start = (robot_x() + fov_radius * math.cos(fov_start_angle),
                     robot_y() + fov_radius * math.sin(fov_start_angle))
    end_pos_end = (robot_x() + fov_radius * math.cos(fov_end_angle),
                   robot_y() + fov_radius * math.sin(fov_end_angle))
    pygame.draw.line(screen, fov_color, start_pos, end_pos_start, 2)
    pygame.draw.line(screen, fov_color, start_pos, end_pos_end, 2)
 
def robot_x():
    return player_position[0]+robot_size[0]
def robot_y():  
    return player_position[1]+robot_size[1]*0.5
  
def distance_between_robot_and_ball(ball_position):
    ball_position=world_to_robot(ball_position)
    del_x = (ball_position[0])**2
    del_y = (ball_position[1])**2
    return (del_x+del_y)**0.5 

def calc_score(ball):
    weight = 0
    bias = 1
    if ball[0] == "red":
        weight = -1
        bias = -1
    elif ball[0] == "blue":
        weight = 1
        bias = 1
    elif ball[0] == "yellow":
        weight = 2
        bias = 1
    elif ball[0] == "green":
        weight = 3
        bias = 1

    distance = distance_between_robot_and_ball(ball[1])/100
    ball2 = world_to_robot(ball[1])
    tan = math.degrees(np.arctan(ball2[0] / ball2[1]))
    ball_score = round(bias*abs(weight*10/ (distance * tan)), 10)
    return ball_score
 
def world_to_robot(position):
    x= position[1]-robot_y()
    y = position[0]-robot_x()
    return (x,y)

# Generate 15 balls
balls = []
for i in range(15): 
    color = random.choice(colors)
    position = None
    while position is None or any(distance_between_robot_and_ball(ball[1]) < 20 for ball in balls):
        position = (random.randint(50, width - 50), random.randint(50, height - 50))
        #position = world_to_robot(position)
    
    ball = (color, position, i)
    balls.append(ball)

    
for ball in balls:
    weight = 0
    bias = 1
    if ball[0] == "red":
        weight = -1
        bias = -1
    elif ball[0] == "blue":
        weight = 1
        bias = 1
    elif ball[0] == "yellow":
        weight = 2
        bias = 1
    elif ball[0] == "green":
        weight = 3
        bias = 1

    ball_score = calc_score(ball)
    scores.append((ball_score, ball))
# Sorting based on the first element of the tuple (ball_score)
sorted_balls = [ball for _, ball in sorted(scores, key=lambda x: x[0], reverse=True)]


# Displaying the sorted balls
for ball in sorted_balls:
    print(ball[0], ball[1], ball[2], "Score: ",calc_score(ball))
  

#def robot_to_world():  
# Main game loop
while True:
   
    screen.fill(background_color)
    # Robot
    pygame.draw.rect(screen, (0, 0, 0), (player_position[0], player_position[1], robot_size[0], robot_size[1]))
     # Draw the balls on the screen
    #for ball in balls:
    #    pygame.draw.circle(screen, ball[0], ball[1], 6.5)

    # Draw the balls within the field of view
    for ball in balls:
        ball_position = ball[1]
        if is_in_field_of_view(ball_position):
            pygame.draw.circle(screen, ball[0], (int(ball_position[0]), int(ball_position[1])), 6.5)
        #else:
        #    # Draw balls outside the field of view with 50% opacity
        #    pygame.draw.circle(screen, (colors[ball[0]][0], colors[ball[0]][1], colors[ball[0]][2], 128),
        #                       (int(ball_position[0]), int(ball_position[1])), 6.5)
            
    for circle in extra_circles:
        pygame.draw.circle(screen, circle[1], (int(circle[0][0]), int(circle[0][1])), 30.5)
        pygame.draw.circle(screen, circle[2], (int(circle[0][0]), int(circle[0][1])), 30.5, 5)


    draw_field_of_view()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.update()