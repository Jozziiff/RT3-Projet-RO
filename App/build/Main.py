from pathlib import Path
import tkinter as tk
import subprocess

FACILITY3_ASSETS_PATH = Path(__file__).parent / "assets" / "frame6"
FACILITY2_ASSETS_PATH = Path(__file__).parent / "assets" / "frame5"
TSP_ASSETS_PATH = Path(__file__).parent / "assets" / "frame4"
KNAPSACK_ASSETS_PATH = Path(__file__).parent / "assets" / "frame3"
FACILITY1_ASSETS_PATH = Path(__file__).parent / "assets" / "frame2"
HOME_ASSETS_PATH = Path(__file__).parent / "assets" / "frame1"
ABOUT_ASSETS_PATH = Path(__file__).parent / "assets" / "frame0"

def facility3_relative_to_assets(path: str) -> Path:
    return FACILITY3_ASSETS_PATH/ Path(path)

def facility2_relative_to_assets(path: str) -> Path:
    return FACILITY2_ASSETS_PATH/ Path(path)

def tsp_relative_to_assets(path: str) -> Path:
    return TSP_ASSETS_PATH/ Path(path)

def knapsack_relative_to_assets(path: str) -> Path:
    return KNAPSACK_ASSETS_PATH/ Path(path)

def facility1_relative_to_assets(path: str) -> Path:
    return FACILITY1_ASSETS_PATH/ Path(path)

def home_relative_to_assets(path: str) -> Path:
    return HOME_ASSETS_PATH / Path(path)

def about_relative_to_assets(path: str) -> Path:
    return ABOUT_ASSETS_PATH / Path(path)

def show_frame(frame):
    frame.tkraise()


# Main window
window = tk.Tk()
window.geometry("1200x720")
window.title("Operation Research Project")

# Knapsack frame
knapsack_frame = tk.Frame(window, bg="white")
knapsack_frame.place(x=0, y=0, width=1200, height=720)

knapsack_canvas = tk.Canvas(
    knapsack_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

knapsack_canvas.place(x = 0, y = 0)
knapsack_image_1 = tk.PhotoImage(
    file=knapsack_relative_to_assets("image_1.png"))
image_21 = knapsack_canvas.create_image(
    600.0,
    360.0,
    image=knapsack_image_1
)

knapsack_image_2 = tk.PhotoImage(
    file=knapsack_relative_to_assets("image_2.png"))
image_22 = knapsack_canvas.create_image(
    600.0,
    42.0,
    image=knapsack_image_2
)

knapsack_image_3 = tk.PhotoImage(
    file=knapsack_relative_to_assets("image_3.png"))
image_23 = knapsack_canvas.create_image(
    703.0,
    365.0,
    image=knapsack_image_3
)

knapsack_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

button_image_21 = tk.PhotoImage(
    file=knapsack_relative_to_assets("button_1.png"))
button_21 = tk.Button(
    knapsack_frame,
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_21.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

button_image_22 = tk.PhotoImage(
    file=knapsack_relative_to_assets("button_2.png"))
button_22 = tk.Button(
    knapsack_frame,
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_22.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# end of knapsack_frame ==========================

# TSP Frame
tsp_frame = tk.Frame(window, bg="white")
tsp_frame.place(x=0, y=0, width=1200, height=720)

tsp_canvas = tk.Canvas(
    tsp_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

tsp_canvas.place(x = 0, y = 0)
tsp_image_1 = tk.PhotoImage(
    file=tsp_relative_to_assets("image_1.png"))
image_31 = tsp_canvas.create_image(
    600.0,
    360.0,
    image=tsp_image_1
)

tsp_image_2 = tk.PhotoImage(
    file=tsp_relative_to_assets("image_2.png"))
image_32 = tsp_canvas.create_image(
    600.0,
    42.0,
    image=tsp_image_2
)

tsp_image_3 = tk.PhotoImage(
    file=tsp_relative_to_assets("image_3.png"))
image_33 = tsp_canvas.create_image(
    703.0,
    360.0,
    image=tsp_image_3
)

tsp_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

button_image_31 = tk.PhotoImage(
    file=tsp_relative_to_assets("button_1.png"))
button_31 = tk.Button(
    tsp_frame,
    image=button_image_31,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_31.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

button_image_32 = tk.PhotoImage(
    file=tsp_relative_to_assets("button_2.png"))
button_32 = tk.Button(
    tsp_frame,
    image=button_image_32,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_32.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# -------------------------- End of tsp_frame --------------------------}

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

# KNAPSACK <==============================
def open_knapsack_app():
    subprocess.Popen(["python", str(Path(__file__).parent.parent.parent / "Problems" / "Problem Sac a dos" / "sacados.py")])

button_image_1 = tk.PhotoImage(
    file=home_relative_to_assets("button_1.png"))
button_1 = tk.Button(
    home_frame,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    #command=open_knapsack_app,
    command=lambda: show_frame(knapsack_frame),
    relief="flat"
)
button_1.place(
    x=282.0,
    y=381.0,
    width=250.0,
    height=241.0
)

# TSP <==============================
def open_tsp_app():
    subprocess.Popen(["python", str(Path(__file__).parent.parent.parent / "Problems" / "TSP" / "tspfinal.py")])
    
button_image_2 = tk.PhotoImage(
    file=home_relative_to_assets("button_2.png"))
button_2 = tk.Button(
    home_frame,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    #command=open_tsp_app,
    command=lambda: show_frame(tsp_frame),
    relief="flat"
)
button_2.place(
    x=578.0,
    y=381.0,
    width=250.0,
    height=241.0
)

# Facility Location
button_image_3 = tk.PhotoImage(
    file=home_relative_to_assets("button_5.png"))
button_3 = tk.Button(
    home_frame,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(facility1_frame),
    relief="flat"
)
button_3.place(
    x=874.0,
    y=381.0,
    width=250.0,
    height=241.0
)

# About us Button
button_image_4 = tk.PhotoImage(
    file=home_relative_to_assets("button_3.png"))
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
    file=home_relative_to_assets("button_4.png"))
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
# -------------------------- End of about_frame --------------------------}
# Facility Location Frame 1
facility1_frame = tk.Frame(window, bg="white")
facility1_frame.place(x=0, y=0, width=1200, height=720)


facility1_canvas = tk.Canvas(
    facility1_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

facility1_canvas.place(x = 0, y = 0)
facility1_image_1 = tk.PhotoImage(
    file=facility1_relative_to_assets("image_1.png"))
image_11 = facility1_canvas.create_image(
    600.0,
    360.0,
    image=facility1_image_1
)

facility1_image_2 = tk.PhotoImage(
    file=facility1_relative_to_assets("image_2.png"))
image_12 = facility1_canvas.create_image(
    600.0,
    42.0,
    image=facility1_image_2
)

facility1_image_3 = tk.PhotoImage(
    file=facility1_relative_to_assets("image_3.png"))
image_13 = facility1_canvas.create_image(
    703.0,
    390.0,
    image=facility1_image_3
)

# Set & Max Coverage Button
button_image_11 = tk.PhotoImage(
    file=facility1_relative_to_assets("button_1.png"))
button_11 = tk.Button(
    facility1_frame,
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(facility2_frame),
    relief="flat"
)
button_11.place(
    x=407.0,
    y=320.0,
    width=252.0,
    height=80.0
)

# Fixed Charge Button
button_image_12 = tk.PhotoImage(
    file=facility1_relative_to_assets("button_2.png"))
button_12 = tk.Button(
    facility1_frame,
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(facility3_frame),
    relief="flat"
)
button_12.place(
    x=755.0,
    y=320.0,
    width=252.0,
    height=80.0
)

facility1_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

# About us Button
button_image_13 = tk.PhotoImage(
    file=facility1_relative_to_assets("button_3.png"))
button_13 = tk.Button(
    facility1_frame,
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_13.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

# Home Button
button_image_14 = tk.PhotoImage(
    file=facility1_relative_to_assets("button_4.png"))
button_14 = tk.Button(
    facility1_frame,
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_14.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# end of facility1_frame ==========================================

# Facility Location Frame 2 ( set coverage )
facility2_frame = tk.Frame(window, bg="white")
facility2_frame.place(x=0, y=0, width=1200, height=720)

facility2_canvas = tk.Canvas(
    facility2_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

facility2_canvas.place(x = 0, y = 0)
facility2_image_1 = tk.PhotoImage(
    file=facility2_relative_to_assets("image_1.png"))
image_111 = facility2_canvas.create_image(
    600.0,
    360.0,
    image=facility2_image_1
)

facility2_image_2 = tk.PhotoImage(
    file=facility2_relative_to_assets("image_2.png"))
image_112 = facility2_canvas.create_image(
    600.0,
    42.0,
    image=facility2_image_2
)

facility2_image_3 = tk.PhotoImage(
    file=facility2_relative_to_assets("image_3.png"))
image_113 = facility2_canvas.create_image(
    717.0,
    390.0,
    image=facility2_image_3
)

facility2_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")

# About us Button
button_image_111 = tk.PhotoImage(
    file=facility2_relative_to_assets("button_1.png"))
button_111 = tk.Button(
    facility2_frame,
    image=button_image_111,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_111.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)

# Home Button
button_image_112 = tk.PhotoImage(
    file=facility2_relative_to_assets("button_2.png"))
button_112 = tk.Button(
    facility2_frame,
    image=button_image_112,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_112.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# end of facility2_frame ==========================

# Begin facility3_frame ( fixed charge )
facility3_frame = tk.Frame(window, bg="white")
facility3_frame.place(x=0, y=0, width=1200, height=720)

facility3_canvas = tk.Canvas(
    facility3_frame,
    bg = "#C4C4C4",
    height = 720,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

facility3_canvas.place(x = 0, y = 0)
facility3_image_1 = tk.PhotoImage(
    file=facility3_relative_to_assets("image_1.png"))
image_1111 = facility3_canvas.create_image(
    600.0,
    360.0,
    image=facility3_image_1
)

facility3_image_2 = tk.PhotoImage(
    file=facility3_relative_to_assets("image_2.png"))
image_1112 = facility3_canvas.create_image(
    600.0,
    42.0,
    image=facility3_image_2
)

facility3_image_3 = tk.PhotoImage(
    file=facility3_relative_to_assets("image_3.png"))
image_1113 = facility3_canvas.create_image(
    703.0,
    390.0,
    image=facility3_image_3
)

facility3_canvas.create_rectangle(
    16.0,
    110.0,
    223.0,
    275.0,
    fill="#000000",
    outline="")
# About us button
button_image_1111 = tk.PhotoImage(
    file=facility3_relative_to_assets("button_1.png"))
button_1111 = tk.Button(
    facility3_frame,
    image=button_image_1111,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(about_frame),
    relief="flat"
)
button_1111.place(
    x=31.0,
    y=209.0,
    width=176.0,
    height=43.0
)
# Home button
button_image_1112 = tk.PhotoImage(
    file=facility3_relative_to_assets("button_2.png"))
button_1112 = tk.Button(
    facility3_frame,
    image=button_image_1112,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(home_frame),
    relief="flat"
)
button_1112.place(
    x=31.0,
    y=133.0,
    width=176.0,
    height=43.0
)
# end of facility3_frame ==========================




show_frame(home_frame)

window.resizable(False, False)
window.mainloop()