import random
import pygame
import sys
import math
import lidar_sim as lidar
import camera_sim as camera

# Create obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define constants
# Constants in meters and meters per second
MOVE_SPEED_MPS = 1.0  # Initial speed of forward movement in meters per second
TURN_ANGLE_DEG = 0.25  # Initial angle of turning in degrees
ACCELERATION_MPS2 = 2.0  # Acceleration rate for both forward movement and turning in meters per second squared
FORWARD_FRICTION = 0.15  # Coefficient of friction for forward movement
TURN_FRICTION = 0.05 # Coefficient of friction for turning
STEERING_SENSITIVITY = 0.002  # Sensitivity of steering
ACCELERATION_TURN_MPS2 = 0.05  # Acceleration rate for turning in meters per second squared
MAX_SPEED_MPS = 1.0  # Maximum speed limit for the robot in meters per second
MAX_TURN_SPEED_RADPS = math.radians(180)  # Maximum turning speed in radians per second\
MOTOR_SPEED = 70

# Convert constants from meters per second to pixels per frame
PIXELS_PER_METER = 100  # Assuming 1 pixel represents 1 cm
MOVE_SPEED = MOVE_SPEED_MPS * PIXELS_PER_METER
ACCELERATION = ACCELERATION_MPS2 * PIXELS_PER_METER
ACCELERATION_TURN = ACCELERATION_TURN_MPS2 * PIXELS_PER_METER

# Initialize robot direction (angle in radians)
robot_direction = random.randint(0,360)  # Initially facing right
# Initialize robot velocity
robot_velocity = [0, 0]  # [x_velocity, y_velocity]
# Initialize turning angle velocity
turning_velocity = 0

# Set up display
pygame.init()
width, height = 1216, 816
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IFOR CB 23 Simulator")
background = pygame.image.load("map.jpg")

running = True

colors = ["red", "blue", "green", "yellow"]
weights = {"red": -1, "blue": 1, "green": 3, "yellow": 2}

# Points for the Collection Bins == Coordinates, Color, Border Color
collection_points = [((width-30.5, 30.5), (0, 150, 45),(128, 0, 128)), ((width-30.5,769.5), (0, 150, 45),(128, 0, 128))]

# Player position and field of view angle
random_variance_x= random.randint(0,200) - 100
random_variance_y= random.randint(0,200)
player_position = [width/2 + random_variance_x, height - random_variance_y]
robot_size = (80, 60)  # Adjusted to match the size of the robot image
fov_angle = 70  # in degrees

# Generate Balls
balls = []
for i in range(random.randint(10, 30)): 
    color = random.choice(colors)
    position = (random.randint(50, width - 50), random.randint(50, height - 50))
    ball = (color, position, i)
    balls.append(ball)

def draw_rotated_robot(x, y, angle):
    # Create a rotated version of the robot image
    rotated_robot = pygame.transform.rotate(robot_image, -angle)  # Adjust rotation angle
    # Get the rect of the rotated image for positioning
    robot_rect = rotated_robot.get_rect(center=(x, y))
    # Draw the rotated robot onto the screen
    screen.blit(rotated_robot, robot_rect)

# Load robot imag
robot_image = pygame.image.load('robot.png')
base_image = pygame.image.load('base.jpg')
# Font for displaying FPS
font = pygame.font.Font(None, 36)

# Clock for tracking time
clock = pygame.time.Clock()

# Track time elapsed since last frame
delta_time = 0

kill = 0  # Initialize the kill variable

laser=lidar.LaserSensor(1200, background, uncertentity=(0.5,0.01), screen=screen, robot_direction=robot_direction)
cam = camera.CameraScan(80, background, uncertentity=(0.5,0.01), screen=screen, robot_direction=robot_direction, fov = 70)

while running:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    #screen.blit(base_image,(width//2, height//2))
    # Create sprite group for obstacles

    # Create a Rect object for the rectangle    
    # rectangle_rect = pygame.Rect(width//2, height//2, 160, 110)
    #pygame.draw.rect(screen, (0,0,0), rectangle_rect)
    # Calculate delta time
    delta_time = clock.tick(120) / 1000.0  # Convert milliseconds to seconds

    # Draw the Robot
    player_position[0] = max(0, min(width - robot_size[0], player_position[0] + robot_velocity[0] * delta_time))
    player_position[1] = max(0, min(height - robot_size[1], player_position[1] + robot_velocity[1] * delta_time))
    laser.position = ( ((player_position[0] + robot_size[0] / 2) + 30 * math.cos(robot_direction)), ((player_position[1] + robot_size[1] / 2) + 30 * math.sin(robot_direction)))
    cam.position = ( ((player_position[0] + robot_size[0] / 2) + 30 * math.cos(robot_direction)), ((player_position[1] + robot_size[1] / 2) + 30 * math.sin(robot_direction)))
    #laser.position = pygame.mouse.get_pos()
    sensor_data=laser.sense_obstacles()
    cam_data = cam.sense_obstacles(balls)
    #laser.robot_direction = robot_direction
    player_position2 = player_position[0] + robot_size[0] / 2, player_position[1] + robot_size[1] / 2
    end_point = (player_position2[0] + 150 * math.cos(robot_direction), player_position2[1] + 150 * math.sin(robot_direction))
    #pygame.draw.line(screen, (255, 0, 0), (player_position2), end_point, 2)  

    draw_rotated_robot(player_position[0] + robot_size[0] / 2, player_position[1] + robot_size[1] / 2, math.degrees(robot_direction))
    # Draw the red line
    laser.robot_direction = robot_direction
    cam.robot_direction = robot_direction
    
    #laser.draw_line(screen)
    #print(sensor_data)
    #if sensor_data != False:
    #for data in sensor_data:
    #    if int(data[1])==0:
    #        print(data[0]/100)
    #print(sensor_data)
    #laser.draw_line(screen)

    
    # Print the speed and turn values
    linear_speed = math.sqrt(robot_velocity[0] ** 2 + robot_velocity[1] ** 2) / PIXELS_PER_METER
    turn_speed = math.degrees(turning_velocity)
    SPEED_CONTROL = round((linear_speed/MAX_SPEED_MPS)*MOTOR_SPEED,1)
    TURN_CONTROL = round((turn_speed/math.degrees(MAX_TURN_SPEED_RADPS))*MOTOR_SPEED,1)
    if SPEED_CONTROL <=5:
        SPEED_CONTROL =5
    if abs(TURN_CONTROL) <=5:
        TURN_CONTROL =5
    #print(SPEED_CONTROL, TURN_CONTROL, kill)
    
    # Draw the balls within the field of view
    for ball in balls:
        ball_position = ball[1]
        pygame.draw.circle(screen, ball[0], (int(ball_position[0]), int(ball_position[1])), 6.5)

    # Draw the Collection Bins
    for circle in collection_points:
        pygame.draw.circle(screen, circle[1], (int(circle[0][0]), int(circle[0][1])), 30.5)
        pygame.draw.circle(screen, circle[2], (int(circle[0][0]), int(circle[0][1])), 30.5, 5)

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Continuous movement when keys are held down
    if keys[pygame.K_w] and kill==0:
        # Accelerate the robot forwards
        robot_velocity[0] += math.cos(robot_direction) * ACCELERATION * delta_time
        robot_velocity[1] += math.sin(robot_direction) * ACCELERATION * delta_time

    # Apply friction to slow down forward movement
    robot_velocity[0] *= FORWARD_FRICTION ** delta_time
    robot_velocity[1] *= FORWARD_FRICTION ** delta_time

    if keys[pygame.K_d] and kill==0:
        # Accelerate the turning of the robot clockwise
        turning_velocity += ACCELERATION_TURN * delta_time
    elif turning_velocity > 0 and kill ==0:
        # Apply friction to slow down turning
        turning_velocity *= TURN_FRICTION ** delta_time
    if keys[pygame.K_a] and kill==0:
        # Accelerate the turning of the robot counterclockwise
        turning_velocity -= ACCELERATION_TURN * delta_time
    elif turning_velocity < 0 and kill==0:
        # Apply friction to slow down turning
        turning_velocity *= TURN_FRICTION ** delta_time

    if kill==1:
        robot_velocity[0] = 0
        robot_velocity[1] = 0 
        turning_velocity =  0

    # Limit the maximum turning speed of the robot
    if abs(turning_velocity) > MAX_TURN_SPEED_RADPS and kill==0:
        turning_velocity = math.copysign(MAX_TURN_SPEED_RADPS, turning_velocity)

    # Limit the maximum speed of the robot
    speed = math.sqrt(robot_velocity[0] ** 2 + robot_velocity[1] ** 2)
    if speed > MAX_SPEED_MPS * PIXELS_PER_METER and kill == 0:
        scale_factor = MAX_SPEED_MPS * PIXELS_PER_METER / speed
        robot_velocity[0] *= scale_factor
        robot_velocity[1] *= scale_factor

    # Update the direction of the robot based on turning velocity
    robot_direction += turning_velocity * delta_time

    # Update the position of the robot based on its velocity
    player_position[0] += robot_velocity[0] * delta_time
    player_position[1] += robot_velocity[1] * delta_time

    # Check if the 'K' key is pressed
    if keys[pygame.K_k]:
        kill = 1
    
    # Draw FPS
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, pygame.Color('white'))
    screen.blit(fps_text, (width - 150, height - 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
