import pygame
import math
import numpy as np 

def uncertainty_add(distance, angle, sigma):
    mean=np.array([distance, angle])
    covanriance=np.diag(sigma**2)
    distance, angle=np.random.multivariate_normal(mean, covanriance)
    distance=max(distance, 0)
    angle=max(angle, 0)
    return [distance , angle]

class CameraScan:
    def __init__(self, Range, map, uncertentity, screen, robot_direction, fov):
        self.Range=Range
        self.sigma=np.array([uncertentity[0], uncertentity[1]])
        self.position=(0,0)
        self.map=map 
        self.w, self.h=pygame.display.get_surface().get_size()
        self.sensedObstacles=[]
        self.screen = screen
        self.robot_direction = robot_direction
        self.fov = fov
    def distance(self, ObstaclePosition):
        px=(ObstaclePosition[0]-self.position[0])**2
        py=(ObstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)
    def sense_obstacles(self, balls):
        data = []
        x1, y1 = self.position[0], self.position[1]
        for angle in np.linspace(self.robot_direction, (self.robot_direction + 2*math.pi), 100, endpoint=False):
            # Adjust negative angles to fall within [0, 2π)
            if angle < 0:
                angle += 2 * math.pi

            x2, y2 = (x1 + self.Range * math.cos(angle), y1 + self.Range * math.sin(angle))
              # Draw scan line
            
            start_angle = 95
            end_angle =  225
            for ball in balls:
                ball_position = ball[1]
                ball_color = ball[0]
                ball_radius = 6.5  # Adjust according to your ball size
                if not (math.degrees(angle-self.robot_direction)>=start_angle and math.degrees(angle-self.robot_direction)<=end_angle):
                     pygame.draw.line(self.screen, (0, 0, 255), self.position, (int(x2), int(y2)), 2)
                
                if self.circle_line_collision(x1, y1, x2, y2, ball_position[0], ball_position[1], ball_radius) and not (math.degrees(angle-self.robot_direction)>=start_angle and math.degrees(angle-self.robot_direction)<=end_angle):
                    # Collision detected between the ray and the ball
                   
                    distance = self.distance(ball_position)
                    output = uncertainty_add(distance, math.degrees(angle - self.robot_direction), self.sigma)
                    output.append(self.position)
                    output.append(ball_color)  # Add ball color to the output
                    data.append(output)
                    for d in data:
                        print(d[1])
                    break  # Break out of the loop to ensure each ray detects only one ball

        if len(data) > 0:
            return data
        else:
            return False

    def circle_line_collision(self, x1, y1, x2, y2, cx, cy, cr):
        dx = x2 - x1
        dy = y2 - y1
        fx = x1 - cx
        fy = y1 - cy
        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - cr * cr
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False
        else:
            discriminant = math.sqrt(discriminant)
            t1 = (-b + discriminant) / (2 * a)
            t2 = (-b - discriminant) / (2 * a)
            if 0 <= t1 <= 1 or 0 <= t2 <= 1:
                return True
            else:
                return False
        