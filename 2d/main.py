from customtkinter import CTk
from Canvas import Canvas
from Navigation import Navigation


class App(CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_widgets()

    def setup_window(self):
        window_width, window_height = 1280, 720
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.title("2D shape proram")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, uniform="nav_col")
        self.grid_columnconfigure(1, weight=1, uniform="nav_col")
        self.bind("<Key>", self.handle_key_press)

    def setup_widgets(self):
        self.opengl_canvas = Canvas(self)
        self.opengl_canvas.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        navigation = Navigation(self)
        navigation.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="nsew")

    def handle_key_press(self, event):
        self.opengl_canvas.key_pressed(event)

if __name__ == '__main__':
    App().mainloop()
