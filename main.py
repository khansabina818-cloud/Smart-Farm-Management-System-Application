from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from login import Login
from db import init_db

BG = "#0F2A1D"
FG = "#4ADE80"
SUB = "#DFF5EA"


class Splash:
    def __init__(self, root):
        self.root = root

        root.geometry("800x450")
        root.overrideredirect(True)
        root.config(bg=BG)

        # Background Image
        img = Image.open("farm_bg.jpg")
        img = img.resize((800, 450))

        self.bg = ImageTk.PhotoImage(img)

        bg = tk.Label(root, image=self.bg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        tk.Label(
            root,
            text="🌾 Smart Farm Management Application",
            fg="#00FF7F",
            bg="#000000",
            font=("Segoe UI", 24, "bold")
        ).place(x=90, y=40)

        # Loading Text
        tk.Label(
            root,
            text="Loading Digital Agriculture System...",
            fg="white",
            bg="#000000",
            font=("Segoe UI", 12, "bold")
        ).place(x=250, y=300)

        # Progress Bar
        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=420,
            mode="determinate"
        )

        self.progress.place(x=190, y=340)

        self.load = 0
        self.animate()

    def animate(self):
        if self.load < 100:
            self.load += 5
            self.progress["value"] = self.load
            self.root.after(80, self.animate)
        else:
            self.open_login()

    def open_login(self):
        self.root.destroy()

        root = tk.Tk()
        Login(root)
        root.mainloop()


if __name__ == "__main__":
    init_db()

    root = tk.Tk()
    Splash(root)
    root.mainloop()