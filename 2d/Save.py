import pickle
from tkinter import filedialog, Tk
from Canvas import Canvas

def export_to_file() -> bool:
    if len(Canvas.shapes) <= 0:
        print("No shapes yet")
        return False

    file_path = save_file_dialog()

    if file_path:
        with open(file_path, 'wb') as file:
            pickle.dump(Canvas.shapes, file)
        return True
    else:
        print("Cancelled")
        return False

def open_file_dialog() -> str | None:
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path if file_path else None

def save_file_dialog() -> str | None:
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[
            ("Pickle", "*.pkl"),
            ("All files", "*.*")
        ]
    )
    return file_path if file_path else None

def import_from_file():
    file_path = open_file_dialog()
    if file_path:
        with open(file_path, 'rb') as file:
            Canvas.shapes = pickle.load(file)
    else:
        print('Cancelled selection')
