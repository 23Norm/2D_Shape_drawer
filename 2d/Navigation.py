from PickColor import ColorPickerToggle
from Save import export_to_file, import_from_file
from customtkinter import CTkFrame, CTkButton
from ButtonShape import ShapeButton
from shapes import Shape

class Navigation(CTkFrame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        color = ColorPickerToggle(self, self.parent)
        color.pack(fill='both', pady=(5, 0), padx=5)

        export = CTkButton(self, text="Export", width=100, command=export_to_file)
        export.pack(fill='both', pady=(5, 0), padx=5)

        import_button = CTkButton(self, text="Import", width=100, command=import_from_file)
        import_button.pack(fill='both', pady=(5, 0), padx=5)

        shapes = {subclass.__name__: subclass for subclass in Shape.__subclasses__()}
        for shape_name, shape_class in shapes.items():
            button = ShapeButton(self, parent, shape_name, shape_class, width=100)
            button.pack(fill='both', pady=(5, 0), padx=5)
