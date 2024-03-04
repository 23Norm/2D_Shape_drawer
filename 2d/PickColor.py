from customtkinter import CTkButton, CTkFrame
from CTkColorPicker import *
from GlobalVar import Global
from typing import Type

class ColorPickerToggle(CTkButton):
    def __init__(self, parent: Type[CTkFrame], app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(corner_radius=0, fg_color="green", text='Color', width=25, height=25)

        self.app = app

    def _clicked(self, event) -> None:
        super()._clicked(event)
        pick_color: AskColor = AskColor()

        chosen_color = pick_color.get()
        self.configure(fg_color=chosen_color if chosen_color else "white")

        if Global.selected_shape:
            Global.selected_shape.set_new_color_from_hex(chosen_color)