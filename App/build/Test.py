import tkinter as tk

def show_frame(frame):
    frame.tkraise()

# Main window
window = tk.Tk()
window.geometry("400x300")
window.title("Frame Switch Example")

# Yellow Frame
yellow_frame = tk.Frame(window, bg="yellow")
yellow_frame.place(x=0, y=0, width=400, height=300)

yellow_button = tk.Button(
    yellow_frame, 
    text="Go to White Frame", 
    command=lambda: show_frame(white_frame)
)
yellow_button.pack(pady=20)

# White Frame
white_frame = tk.Frame(window, bg="white")
white_frame.place(x=0, y=0, width=400, height=300)

white_button = tk.Button(
    white_frame, 
    text="Go to Yellow Frame", 
    command=lambda: show_frame(yellow_frame)
)
white_button.pack(pady=20)

# Show Yellow Frame initially
show_frame(yellow_frame)

window.mainloop()
