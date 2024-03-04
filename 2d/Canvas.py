from pyopengltk import OpenGLFrame
from OpenGL.GLU import *
from OpenGL.GL import *

from KeyPress import get_pressed_status
from GlobalVar import Global

class Canvas(OpenGLFrame):
    shapes = []

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<ButtonPress-1>", self._on_mouse_press)
        self.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.parent = parent
        self.dragging = False

    def initgl(self) -> None:
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.17, 0.17, 0.17, 1.0)
        self.animate = 1
        self.dragging = False
        self.start_coordinates = None
        self.current_coordinates = None
        self.end_coordinates = None

    def key_pressed(self, event):
        pressed_status = get_pressed_status(event)
        key = event.keysym

        if not Global.selected_shape:
            print("Select a shape first")
            return

        state = pressed_status.get('state', None)

        if state is not None and state != '0x40000':
            if 'Control' in state:
                if key == 'minus':
                    Global.selected_shape.shrink()
                    return
                if key == 'equal':
                    Global.selected_shape.expand()
                    return

        if key == 'Up':
            Global.selected_shape.move_up()
        elif key == 'Down':
            Global.selected_shape.move_down()
        elif key == 'Left':
            Global.selected_shape.move_left()
        elif key == 'Right':
            Global.selected_shape.move_right()
        elif key == 'r' or key == 'R':  
            Global.selected_shape.rotate()
            print('shape rotating')
        elif key == 't' or key == 'T':  
            Global.selected_shape.rotate(True)
            print('shape rotating')
        

    def _on_mouse_move(self, event):
        self.current_coordinates = (event.x, event.y)

    def _on_mouse_press(self, event):
        self.dragging = True
        self.start_coordinates = (event.x, event.y)
        self.current_coordinates = self.start_coordinates

        if not self.dragging == None and len(Canvas.shapes) > 0:
            for shape in Canvas.shapes[::-1]:
                if shape.within_bounds(event.x, event.y):
                    shape.selected = True
                    Global.selected_shape = shape
                    break

            for shape in Canvas.shapes:
                if shape != Global.selected_shape:
                    shape.selected = False

    def _on_mouse_release(self, event):
        self.dragging = False
        self.end_coordinates = self.current_coordinates
        self.current_coordinates = None

        if Global.shape_class:
            Canvas.shapes.append(Global.shape_class(self.start_coordinates, self.end_coordinates))
            Global.shape_name = None
            Global.shape_class = None
            self.parent.configure(cursor="arrow")

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if len(Canvas.shapes) > 0:
            for shape in Canvas.shapes:
                shape.draw_to_canvas()

        if self.dragging:
            glBegin(GL_LINES)
            glVertex2f(*self.start_coordinates)
            glVertex2f(*self.current_coordinates)
            glEnd()
