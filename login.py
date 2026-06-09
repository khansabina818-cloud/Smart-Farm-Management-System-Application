import tkinter as tk
from tkinter import messagebox
from db import connect_db
from dashboard import Dashboard
from PIL import Image, ImageTk

BG = "#0F2A1D"
PANEL = "#173F2F"
FG = "#DFF5EA"
ACCENT = "#4ADE80"


class Login:
    def __init__(self, root):
        self.root = root

        root.title("Smart Farm Management Login")
        root.geometry("1280x720")
        root.resizable(False, False)

        # Background Image
        img = Image.open("farm_bg.jpg")
        img = img.resize((1280, 720))

        self.bg = ImageTk.PhotoImage(img)

        bg_label = tk.Label(root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # LOGIN FRAME
        box = tk.Frame(root, bg=PANEL)
        box.place(
            relx=0.80,
            rely=0.5,
            anchor="center",
            width=320,
            height=280
        )

        # Title
        tk.Label(
            box,
            text="LOGIN",
            bg=PANEL,
            fg=ACCENT,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        # Username
        tk.Label(
            box,
            text="Username",
            bg=PANEL,
            fg=FG,
            font=("Segoe UI", 11)
        ).pack()

        tk.Entry(
            box,
            textvariable=self.username,
            width=28,
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # Password
        tk.Label(
            box,
            text="Password",
            bg=PANEL,
            fg=FG,
            font=("Segoe UI", 11)
        ).pack(pady=(10, 0))

        tk.Entry(
            box,
            textvariable=self.password,
            show="*",
            width=28,
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # Login Button
        tk.Button(
            box,
            text="Login",
            bg=ACCENT,
            fg="black",
            font=("Segoe UI", 11, "bold"),
            width=15,
            cursor="hand2",
            command=self.check_login
        ).pack(pady=25)

    def check_login(self):

        if not self.username.get() or not self.password.get():
            messagebox.showerror("Error", "All fields required")
            return

        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (self.username.get(), self.password.get())
        )

        user = cur.fetchone()
        con.close()

        if user:
            self.root.destroy()

            root = tk.Tk()
            Dashboard(root)
            root.mainloop()

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid credentials"
            )