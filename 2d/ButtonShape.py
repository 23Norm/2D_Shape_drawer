from customtkinter import CTkButton
from GlobalVar import Global

class ShapeButton(CTkButton):
    def __init__(self, parent, app, shape_name, shape_class, *args, **kwargs):
        super().__init__(parent, text=shape_name, *args, **kwargs)
        self.shape_name = shape_name
        self.shape_class = shape_class
        self.app = app

    def _clicked(self, event):
        Global.shape_name = self.shape_name
        Global.shape_class = self.shape_class
        self.app.configure(cursor="crosshair")
