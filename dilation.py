import argparse
import math

import pygame

pygame.init()

size = width, height = (700, 700)
screen = pygame.display.set_mode(size)

parser = argparse.ArgumentParser(description='Scrape Google Images')
parser.add_argument('-k', '--factor', default=2,
                    type=str, help='search key')
K = int(parser.parse_args().factor)
class Point:
    def __init__(self, x:int, y:int, radius:int=10, color="red") -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.bound = False
        self.color = color

    @property
    def pos(self):
        return (self.x, self.y)

    def is_hovered(self, mouse_pos):
        dist = math.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2)
        return dist < self.radius


    def set_offset(self, mouse_pos):
        self.x_offset = mouse_pos[0] - self.x
        self.y_offset = mouse_pos[1] - self.y

    def bind(self, mouse_pos):
        
        if self.is_hovered(mouse_pos):
            self.bound = True
            self.set_offset(mouse_pos)
        
        else:
            self.bound = False
    
    def unbind(self):
        self.bound = False

    def draw(self, mouse_pos):

        if self.bound:
            self.x = mouse_pos[0] - self.x_offset
            self.y = mouse_pos[1] - self.y_offset
        
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def bind_points(mouse_pos):
    for point in points:
        point.bind(mouse_pos)
    center.bind(mouse_pos)


def unbind_points():
    for point in points:
        point.unbind()
    center.unbind()


def draw_points(mouse_pos):
    for point in points:
        point.draw(mouse_pos)
    center.draw(mouse_pos)


def draw_lines(points):
    l = len(points)
    for i in range(l):
        start = points[i].pos
        end = points[(i + 1) % l].pos

        pygame.draw.line(screen, "red", start, end)


def dilation(center, k, point):
    x = k * (point[0] - center[0]) + center[0]
    y = k * (point[1] - center[1]) + center[1]
    return (x, y)


def update_images():
    for i in range(len(points)):
        x, y = dilation(center.pos, K, points[i].pos)
        image_points[i].x = x
        image_points[i].y = y



def draw_images():
    for point in image_points:
        point.draw(mouse_pos)


center = Point(width // 2, height // 2, color="black")

points = [
    Point(400, 200, color="blue"),
    Point(300, 400, color="blue"),
    Point(200, 200, color="blue"),
]

image_points = [
    Point(*dilation(center.pos, K, point.pos)) for point in points
]


    
MOUSE = False


while True:
    
    mouse_pos = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        
        if ev.type == pygame.QUIT:
            pygame.quit()
        
        if ev.type == pygame.KEYDOWN:

            if ev.key == pygame.K_q:
                pygame.quit()

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            MOUSE = True
            bind_points(mouse_pos)

        
        elif ev.type == pygame.MOUSEBUTTONUP:
            MOUSE = False
            unbind_points()


    screen.fill("white")

    

    draw_lines(points)
    draw_points(mouse_pos)
    update_images()
    draw_lines(image_points)
    draw_images()


    pygame.display.update()
