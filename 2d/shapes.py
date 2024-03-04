from typing import List, Tuple
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

class Shape():

    def __init__(
        self,
        number_of_sides: int,
        start_x_y: List[int],
        end_x_y: List[int]
    ) -> None:

        self.number_of_sides: int = number_of_sides
        self.start_x_y: List[int] = start_x_y
        self.end_x_y: List[int] = end_x_y
        self.angle = 0
        self.selected = False

        self.center_x: int|float = (self.start_x_y[0] + self.end_x_y[0]) / 2
        self.center_y: int|float = (self.start_x_y[1] + self.end_x_y[1]) / 2
        self.half_size: int|float = min(self.width, self.height) / 2
        self.background_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
        self.border_width = 15

    def draw_to_canvas(self) -> None:
        glPushMatrix()
        glTranslatef(self.center_x, self.center_y, 0)
        glRotatef(self.angle, 0, 0, 1)
        glTranslatef(-self.center_x, -self.center_y, 0)

        self.draw()

        glPopMatrix()
        glFlush()

    @property
    def width(self) -> int:
        return abs(self.start_x_y[0] - self.end_x_y[0])

    @property
    def height(self) -> int:
        return abs(self.start_x_y[1] - self.end_x_y[1])

    def draw(self) -> None:
        if self.selected:
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.17, 0.17, 0.17)

        vertices=[]

        glBegin(GL_LINE_LOOP)
        for index in range(self.number_of_sides):
            angle = 2 * pi * index / self.number_of_sides + pi
            x: int|float = self.center_x + (self.half_size + self.border_width) * cos(angle)
            y: int|float = self.center_y + (self.half_size + self.border_width) * sin(angle)
            glVertex2f(x, y)
            vertices.append((x,y))
        glEnd()

        glColor3f(*self.background_color)
        glBegin(GL_POLYGON)
        for index in range(self.number_of_sides):
            angle = 2 * pi * index / self.number_of_sides + pi
            x: int|float = self.center_x + self.half_size * cos(angle)
            y: int|float = self.center_y + self.half_size * sin(angle)
            glVertex2f(x, y)
        glEnd()

        if self.selected and self.__class__.__name__ != 'Circle':
            for vertex in vertices:
                self.point_vertices(*vertex)

    def point_vertices(self, x, y):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for index in range(100):
            theta = 2.0 * 3.1415926 * index / 100
            glVertex2f(x + 4 * cos(theta), y + 4 * sin(theta))
        glEnd()

    def within_bounds(self, mouse_x: int, mouse_y: int) -> bool:
        vertices = []

        for index in range(self.number_of_sides):
            angle = 2 * pi * index / self.number_of_sides + radians(self.angle)
            x = self.center_x + self.half_size * cos(angle)
            y = self.center_y + self.half_size * sin(angle)
            endpoint = (x, y)
            vertices.append(endpoint)

        crossings: int = 0

        for index in range(self.number_of_sides):
            start_x, start_y = vertices[index]
            end_x, end_y = vertices[(index + 1) % self.number_of_sides]

            if (start_y > mouse_y) != (end_y > mouse_y):
                if mouse_x < (end_x - start_x) * (mouse_y - start_y) / (end_y - start_y) + start_x:
                    crossings += 1

        return crossings % 2 == 1

    def set_new_color_from_hex(self, hex_color: str) -> None:
        hex_color = hex_color.lstrip('#')

        rgb: Tuple[int] = tuple(int(hex_color[index: index + 2], 16) / 255.0 for index in (0, 2, 4))

        self.background_color = rgb

    def __change_shape(self, increment: bool=True) -> None:
        end_x = self.end_x_y[0]
        end_y = self.end_x_y[1]

        self.end_x_y = (
            end_x + 5 if increment else end_x - 5,
            end_y + 5 if increment else end_y - 5
        )

        self.half_size = min(self.width, self.height) / 2

    def expand(self) -> None:
        self.__change_shape()

    def shrink(self) -> None:
        if self.width > 10:
            self.__change_shape(False)

    def move_left(self):
        self.center_x -= 5

    def move_right(self):
        self.center_x += 5

    def move_up(self):
        self.center_y -= 5

    def move_down(self):
        self.center_y += 5
    
    def rotate(self, left = False ) -> None:
        if not left:
            self.angle += 1
        else:
            self.angle -= 1

class Square(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(4, start_coordinates, end_coordinates)

class Triangle(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(3, start_coordinates, end_coordinates)

class Hexagon(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(6, start_coordinates, end_coordinates)
  
class Pentagon(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(5, start_coordinates, end_coordinates)

class Octagon(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(8, start_coordinates, end_coordinates)

class Circle(Shape):
    def __init__(self, start_coordinates, end_coordinates):
        super().__init__(100, start_coordinates, end_coordinates)
