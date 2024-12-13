from pathlib import Path
import tkinter as tk
import subprocess

class AssetPaths:
    def __init__(self, base_path: Path):
        self.paths = {
            'facility3': base_path / "assets" / "frame6",
            'facility2': base_path / "assets" / "frame5",
            'tsp': base_path / "assets" / "frame4",
            'knapsack': base_path / "assets" / "frame3",
            'facility1': base_path / "assets" / "frame2",
            'home': base_path / "assets" / "frame1",
            'about': base_path / "assets" / "frame0"
        }

    def get_asset_path(self, frame_name: str, path: str) -> Path:
        return self.paths[frame_name] / Path(path)

class FrameFactory:
    def __init__(self, window: tk.Tk, assets: AssetPaths):
        self.window = window
        self.assets = assets
        self.frames = {}

    def create_base_frame(self, name: str):
        frame = tk.Frame(self.window, bg="white")
        frame.place(x=0, y=0, width=1200, height=720)
        
        canvas = tk.Canvas(
            frame,
            bg="#C4C4C4",
            height=720,
            width=1200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Create standard rectangle
        canvas.create_rectangle(
            16.0, 110.0, 223.0, 275.0,
            fill="#000000",
            outline=""
        )
        
        return frame, canvas

    def create_standard_buttons(self, frame, canvas, frame_name, special=0):
        # About button
        if special :
            about_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "button_3.png"))
        else:
            about_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "button_1.png"))
        about_btn = tk.Button(
            frame,
            image=about_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.show_frame('about'),
            relief="flat"
        )
        about_btn.place(x=31.0, y=209.0, width=176.0, height=43.0)
        
        # Home button
        if special:
            home_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "button_4.png"))
        else:
            home_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "button_2.png"))
        home_btn = tk.Button(
            frame,
            image=home_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.show_frame('home'),
            relief="flat"
        )
        home_btn.place(x=31.0, y=133.0, width=176.0, height=43.0)
        
        # Store references to prevent garbage collection
        frame.about_img = about_img
        frame.home_img = home_img

    def create_standard_images(self, canvas, frame_name):
        bg_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "image_1.png"))
        header_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "image_2.png"))
        content_img = tk.PhotoImage(file=self.assets.get_asset_path(frame_name, "image_3.png"))
        
        canvas.create_image(600.0, 360.0, image=bg_img)
        canvas.create_image(600.0, 42.0, image=header_img)
        canvas.create_image(703.0, 390.0, image=content_img)
        
        return bg_img, header_img, content_img

    def show_frame(self, frame_name):
        self.frames[frame_name].tkraise()

class MainApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x720")
        self.window.title("Operation Research Project")
        self.window.resizable(False, False)
        
        self.assets = AssetPaths(Path(__file__).parent)
        self.frame_factory = FrameFactory(self.window, self.assets)
        
        self.create_all_frames()
        self.frame_factory.show_frame('home')

    def create_all_frames(self):
        self.create_home_frame()
        self.create_about_frame()
        self.create_knapsack_frame()
        self.create_tsp_frame()
        self.create_facility_frames()

    def create_home_frame(self):
        frame, canvas = self.frame_factory.create_base_frame('home')
        images = self.frame_factory.create_standard_images(canvas, 'home')
        
        # Create home-specific buttons instead of using standard buttons
        about_img = tk.PhotoImage(file=self.assets.get_asset_path('home', "button_3.png"))
        home_img = tk.PhotoImage(file=self.assets.get_asset_path('home', "button_4.png"))
        
        about_btn = tk.Button(
            frame,
            image=about_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.frame_factory.show_frame('about'),
            relief="flat"
        )
        about_btn.place(x=31.0, y=209.0, width=176.0, height=43.0)
        
        home_btn = tk.Button(
            frame,
            image=home_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.frame_factory.show_frame('home'),
            relief="flat"
        )
        home_btn.place(x=31.0, y=133.0, width=176.0, height=43.0)
        
        # Store button image references
        frame.about_img = about_img
        frame.home_img = home_img
        
        other_buttons = self.create_home_buttons(frame)
        
        # Store all image references
        frame.images = images + (about_img, home_img) + other_buttons
        
        self.frame_factory.frames['home'] = frame

    def create_home_buttons(self, frame):
        button_images = []
        
        # Knapsack button
        knapsack_img = tk.PhotoImage(file=self.assets.get_asset_path('home', "button_1.png"))
        tk.Button(
            frame,
            image=knapsack_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.frame_factory.show_frame('knapsack'), subprocess.Popen(["python", str(self.assets.get_asset_path('facility1', "../../../../Problems/Problem Sac A Dos/sacados.py").resolve())])],
            relief="flat"
        ).place(x=282.0, y=381.0, width=250.0, height=241.0)
        button_images.append(knapsack_img)
        
        # TSP button
        tsp_img = tk.PhotoImage(file=self.assets.get_asset_path('home', "button_2.png"))
        tk.Button(
            frame,
            image=tsp_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.frame_factory.show_frame('tsp'), subprocess.Popen(["python", str(self.assets.get_asset_path('facility1', "../../../../Problems/TSP/tspFinal.py").resolve())])],
            relief="flat"
        ).place(x=578.0, y=381.0, width=250.0, height=241.0)
        button_images.append(tsp_img)
        
        # Facility button
        facility_img = tk.PhotoImage(file=self.assets.get_asset_path('home', "button_5.png"))
        tk.Button(
            frame,
            image=facility_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.frame_factory.show_frame('facility1'),
            relief="flat"
        ).place(x=874.0, y=381.0, width=250.0, height=241.0)
        button_images.append(facility_img)
        
        return tuple(button_images)

    def create_about_frame(self):
        frame, canvas = self.frame_factory.create_base_frame('about')
        images = self.frame_factory.create_standard_images(canvas, 'about')
        self.frame_factory.create_standard_buttons(frame, canvas, 'about')
        
        # Additional about image
        extra_img = tk.PhotoImage(file=self.assets.get_asset_path('about', "image_4.png"))
        canvas.create_image(707.0, 467.0, image=extra_img)
        
        # Store image references
        frame.images = images + (extra_img,)
        
        self.frame_factory.frames['about'] = frame

    def create_knapsack_frame(self):
        frame, canvas = self.frame_factory.create_base_frame('knapsack')
        images = self.frame_factory.create_standard_images(canvas, 'knapsack')
        self.frame_factory.create_standard_buttons(frame, canvas, 'knapsack')
        
        frame.images = images
        self.frame_factory.frames['knapsack'] = frame

    def create_tsp_frame(self):
        frame, canvas = self.frame_factory.create_base_frame('tsp')
        images = self.frame_factory.create_standard_images(canvas, 'tsp')
        self.frame_factory.create_standard_buttons(frame, canvas, 'tsp')
        
        frame.images = images
        self.frame_factory.frames['tsp'] = frame

    def create_facility_frames(self):
        # Facility 1
        frame1, canvas1 = self.frame_factory.create_base_frame('facility1')
        images1 = self.frame_factory.create_standard_images(canvas1, 'facility1')
        self.frame_factory.create_standard_buttons(frame1, canvas1, 'facility1', 1)
        
        # Add facility1-specific buttons
        set_coverage_img = tk.PhotoImage(file=self.assets.get_asset_path('facility1', "button_1.png"))
        fixed_charge_img = tk.PhotoImage(file=self.assets.get_asset_path('facility1', "button_2.png"))
        
        tk.Button(
            frame1,
            image=set_coverage_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.frame_factory.show_frame('facility2'), subprocess.Popen(["python", str(self.assets.get_asset_path('facility1', "../../../../Problems/Facility Location Problem/set and max coverage.py").resolve())])],
            relief="flat"
        ).place(x=407.0, y=320.0, width=252.0, height=80.0)
        
        tk.Button(
            frame1,
            image=fixed_charge_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.frame_factory.show_frame('facility3'), subprocess.Popen(["python", str(self.assets.get_asset_path('facility1', "../../../../Problems/Facility Location Problem/Fixed Charged problem.py").resolve())])],
            relief="flat"
        ).place(x=755.0, y=320.0, width=252.0, height=80.0)
        
        frame1.images = images1 + (set_coverage_img, fixed_charge_img)
        self.frame_factory.frames['facility1'] = frame1
        
        # Facility 2
        frame2, canvas2 = self.frame_factory.create_base_frame('facility2')
        images2 = self.frame_factory.create_standard_images(canvas2, 'facility2')
        self.frame_factory.create_standard_buttons(frame2, canvas2, 'facility2')
        
        frame2.images = images2
        self.frame_factory.frames['facility2'] = frame2
        
        # Facility 3
        frame3, canvas3 = self.frame_factory.create_base_frame('facility3')
        images3 = self.frame_factory.create_standard_images(canvas3, 'facility3')
        self.frame_factory.create_standard_buttons(frame3, canvas3, 'facility3')
        
        frame3.images = images3
        self.frame_factory.frames['facility3'] = frame3

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()