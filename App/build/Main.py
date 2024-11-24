from pathlib import Path
import tkinter as tk

HOME_ASSETS_PATH = Path(__file__).parent / Path(r"C:\Users\tiger\Desktop\BAC INFO\My Fac (INSAT)\RT3\Recherche Operationnelle\Projet\App\build\assets\frame1")
ABOUT_ASSETS_PATH = Path(__file__).parent / Path(r"C:\Users\tiger\Desktop\BAC INFO\My Fac (INSAT)\RT3\Recherche Operationnelle\Projet\App\build\assets\frame0")

def home_relative_to_assets(path: str) -> Path:
    return HOME_ASSETS_PATH / Path(path)

def about_relative_to_assets(path: str) -> Path:
    return ABOUT_ASSETS_PATH / Path(path)

def show_frame(frame):
    frame.tkraise()


# Main window
window = tk.Tk()
window.geometry("1200x720")
window.title("OP_RECH_Project")

# Home Frame
home_frame = tk.Frame(window, bg="white")
home_frame.place(x=0, y=0, width=1200, height=720)

home_canvas = tk.Canvas(
    home_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

home_canvas.place(x = 0, y = 0)
image_image_1 = tk.PhotoImage(
    file=home_relative_to_assets("image_1.png"))
image_1 = home_canvas.create_image(
    600.0,
    360.0,
    image=image_image_1
)

image_image_2 = tk.PhotoImage(
    file=home_relative_to_assets("image_2.png"))
image_2 = home_canvas.create_image(
    600.0,
    42.0,
    image=image_image_2
)

home_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

image_image_3 = tk.PhotoImage(
    file=home_relative_to_assets("image_3.png"))
image_3 = home_canvas.create_image(
    703.0,
    404.0,
    image=image_image_3
)

button_image_1 = tk.PhotoImage(
    file=home_relative_to_assets("button_1.png"))
button_1 = tk.Button(
    home_frame,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=874.0,
    y=381.0,
    width=250.0,
    height=241.0
)

button_image_2 = tk.PhotoImage(
    file=home_relative_to_assets("button_2.png"))
button_2 = tk.Button(
    home_frame,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=282.0,
    y=381.0,
    width=250.0,
    height=241.0
)

button_image_3 = tk.PhotoImage(
    file=home_relative_to_assets("button_3.png"))
button_3 = tk.Button(
    home_frame,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=578.0,
    y=381.0,
    width=250.0,
    height=241.0
)

# About us Button
button_image_4 = tk.PhotoImage(
    file=home_relative_to_assets("button_4.png"))
button_4 = tk.Button(
    home_frame,
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_4.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

# Home Button
button_image_5 = tk.PhotoImage(
    file=home_relative_to_assets("button_5.png"))
button_5 = tk.Button(
    home_frame,
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_5.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# -------------------------- End of home_frame --------------------------}

# About us Frame
about_frame = tk.Frame(window, bg="white")
about_frame.place(x=0, y=0, width=1200, height=720)

about_canvas = tk.Canvas(
    about_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

about_canvas.place(x = 0, y = 0)
image_image_5 = tk.PhotoImage(
    file=about_relative_to_assets("image_1.png"))
image_5 = about_canvas.create_image(
    600.0,
    360.0,
    image=image_image_5
)

image_image_6 = tk.PhotoImage(
    file=about_relative_to_assets("image_2.png"))
image_6 = about_canvas.create_image(
    600.0,
    42.0,
    image=image_image_6
)

image_image_7 = tk.PhotoImage(
    file=about_relative_to_assets("image_3.png"))
image_7 = about_canvas.create_image(
    703.0,
    404.0,
    image=image_image_7
)

image_image_8 = tk.PhotoImage(
    file=about_relative_to_assets("image_4.png"))
image_8 = about_canvas.create_image(
    707.0,
    467.0,
    image=image_image_8
)

about_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

# About us Button
button_image_9 = tk.PhotoImage(
    file=about_relative_to_assets("button_1.png"))
button_9 = tk.Button(
    about_frame,
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_9.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

# Home Button
button_image_10 = tk.PhotoImage(
    file=about_relative_to_assets("button_2.png"))
button_10 = tk.Button(
    about_frame,
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_10.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)

show_frame(home_frame)

window.resizable(False, False)
window.mainloop()