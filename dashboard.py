import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db
from datetime import date, timedelta
from PIL import Image, ImageTk
import re

BG = "#102A1F"
PANEL = "#16382A"
FG = "#D5EBDD"
ACC = "#4ADE80"

PHONE_REGEX = re.compile(r"^[6-9][0-9]{9}$")
NAME_REGEX = re.compile(r"^[A-Za-z ]+$")

CROP_OPTIONS = [
    "Wheat", "Rice", "Cotton", "Soybean",
    "Maize", "Sugarcane", "Pulses", "Vegetables"
]


class Dashboard:

    def __init__(self, root):
        self.root = root
        root.title("AgroSmart Dashboard")
        root.geometry("1280x720")
        root.configure(bg=BG)

        img = Image.open("farm_bg.jpg")
        img = img.resize((450, 650))
        self.side_img = ImageTk.PhotoImage(img)

        tk.Label(root, image=self.side_img).place(x=820, y=40)

        self.nb = ttk.Notebook(root)
        self.nb.place(x=20, y=20, width=780, height=650)

        self.farmer_tab()
        self.crop_tab()
        self.expense_tab()
        self.income_tab()
        self.dashboard_tab()

    # ================= FARMER TAB =================

    def farmer_tab(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Farmers")

        sub_nb = ttk.Notebook(tab)
        sub_nb.pack(fill="both", expand=True, padx=20, pady=20)

        form_tab = ttk.Frame(sub_nb)
        list_tab = ttk.Frame(sub_nb)

        sub_nb.add(form_tab, text="Farmer Form")
        sub_nb.add(list_tab, text="Farmer List")

        self.fn = tk.StringVar()
        self.ph = tk.StringVar()
        self.vl = tk.StringVar()
        self.ld = tk.StringVar()

        form = tk.Frame(form_tab, bg=PANEL)
        form.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=420,
            height=420
        )

        tk.Label(
            form,
            text="Farmer Details",
            bg=PANEL,
            fg=ACC,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        for t, v in [
            ("Name", self.fn),
            ("Phone", self.ph),
            ("Village", self.vl),
            ("Land Area (Acres)", self.ld)
        ]:
            tk.Label(
                form,
                text=t,
                bg=PANEL,
                fg=FG
            ).pack(anchor="w", padx=40)

            tk.Entry(
                form,
                textvariable=v,
                width=30
            ).pack(pady=6)

        btn_frame = tk.Frame(form, bg=PANEL)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Add",
            bg=ACC,
            width=10,
            command=self.add_farmer
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update",
            width=10,
            command=self.update_farmer
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Delete",
            width=10,
            command=self.delete_farmer
        ).grid(row=0, column=2, padx=5)

        table_frame = tk.Frame(list_tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.ft = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Phone", "Village", "Land"),
            show="headings"
        )

        for c in self.ft["columns"]:
            self.ft.heading(c, text=c)
            self.ft.column(c, width=160)

        self.ft.pack(fill="both", expand=True)
        self.ft.bind("<<TreeviewSelect>>", self.fill_form)

        self.load_farmers()

    # ================= VALIDATION =================

    def validate_farmer(self):

        if not all([
            self.fn.get(),
            self.ph.get(),
            self.vl.get(),
            self.ld.get()
        ]):
            messagebox.showerror("Error", "All fields required")
            return None

        if not NAME_REGEX.match(self.fn.get()):
            messagebox.showerror(
                "Error",
                "Name must contain only letters"
            )
            return None

        if not NAME_REGEX.match(self.vl.get()):
            messagebox.showerror(
                "Error",
                "Village must contain only letters"
            )
            return None

        if not PHONE_REGEX.match(self.ph.get()):
            messagebox.showerror(
                "Error",
                "Invalid phone number"
            )
            return None

        try:
            return float(self.ld.get())

        except:
            messagebox.showerror(
                "Error",
                "Land must be numeric"
            )
            return None

    # ================= CRUD =================

    def add_farmer(self):

        land = self.validate_farmer()

        if land is None:
            return

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO farmers(name,phone,village,land)
        VALUES(?,?,?,?)
        """, (
            self.fn.get(),
            self.ph.get(),
            self.vl.get(),
            land
        ))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Farmer Added Successfully ✅"
        )

        self.clear_farmer_form()
        self.load_farmers()
        self.refresh_farmer_dropdowns()

    def update_farmer(self):

        sel = self.ft.focus()

        if not sel:
            messagebox.showerror("Error", "Select farmer")
            return

        land = self.validate_farmer()

        if land is None:
            return

        farmer_id = self.ft.item(sel, "values")[0]

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        UPDATE farmers
        SET name=?,phone=?,village=?,land=?
        WHERE farmer_id=?
        """, (
            self.fn.get(),
            self.ph.get(),
            self.vl.get(),
            land,
            farmer_id
        ))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Farmer Updated Successfully ✅"
        )

        self.clear_farmer_form()
        self.load_farmers()

    def delete_farmer(self):

        sel = self.ft.focus()

        if not sel:
            messagebox.showerror("Error", "Select farmer")
            return

        if not messagebox.askyesno(
            "Confirm",
            "Delete farmer?"
        ):
            return

        farmer_id = self.ft.item(sel, "values")[0]

        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM crops WHERE farmer_id=?",
            (farmer_id,)
        )

        cur.execute(
            "DELETE FROM expenses WHERE farmer_id=?",
            (farmer_id,)
        )

        cur.execute(
            "DELETE FROM income WHERE farmer_id=?",
            (farmer_id,)
        )

        cur.execute(
            "DELETE FROM farmers WHERE farmer_id=?",
            (farmer_id,)
        )

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Farmer Deleted Successfully ✅"
        )

        self.clear_farmer_form()
        self.load_farmers()

    # ================= FORM =================

    def fill_form(self, _):

        sel = self.ft.focus()

        if not sel:
            return

        _, n, p, v, l = self.ft.item(sel, "values")

        self.fn.set(n)
        self.ph.set(p)
        self.vl.set(v)
        self.ld.set(l)

    def clear_farmer_form(self):

        self.fn.set("")
        self.ph.set("")
        self.vl.set("")
        self.ld.set("")

    def load_farmers(self):

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        SELECT farmer_id,name,phone,village,land
        FROM farmers
        """)

        rows = cur.fetchall()

        con.close()

        self.ft.delete(*self.ft.get_children())

        for r in rows:
            self.ft.insert("", tk.END, values=r)

    # ================= DROPDOWN =================

    def get_farmers(self):

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        SELECT farmer_id,name
        FROM farmers
        """)

        data = [
            f"{i} - {n}"
            for i, n in cur.fetchall()
        ]

        con.close()

        return data

    def refresh_farmer_dropdowns(self):

        farmers = self.get_farmers()

        if hasattr(self, "crop_farmer"):
            self.crop_farmer["values"] = farmers

        if hasattr(self, "exp_farmer"):
            self.exp_farmer["values"] = farmers

        if hasattr(self, "inc_farmer"):
            self.inc_farmer["values"] = farmers

        if hasattr(self, "dash_farmer"):
            self.dash_farmer["values"] = farmers

    # ================= CROPS =================

    def crop_tab(self):

        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Crops")

        frame = tk.Frame(tab)

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.cf = tk.StringVar()
        self.cn = tk.StringVar()
        self.cd = tk.StringVar()

        tk.Label(frame, text="Select Farmer").pack()

        self.crop_farmer = ttk.Combobox(
            frame,
            textvariable=self.cf
        )

        self.crop_farmer.pack()
        self.crop_farmer["values"] = self.get_farmers()

        tk.Label(frame, text="Crop").pack()

        ttk.Combobox(
            frame,
            textvariable=self.cn,
            values=CROP_OPTIONS
        ).pack()

        tk.Label(frame, text="Duration Days").pack()

        tk.Entry(
            frame,
            textvariable=self.cd
        ).pack()

        tk.Button(
            frame,
            text="Add Crop",
            command=self.add_crop
        ).pack(pady=20)

    def add_crop(self):

        if not self.cf.get() or not self.cn.get() or not self.cd.get():
            messagebox.showerror(
                "Error",
                "All fields required"
            )
            return

        farmer_id = self.cf.get().split(" - ")[0]

        start = date.today()
        end = start + timedelta(days=int(self.cd.get()))

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO crops(farmer_id,crop_name,start_date,end_date)
        VALUES(?,?,?,?)
        """, (
            farmer_id,
            self.cn.get(),
            start,
            end
        ))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Crop Added ✅"
        )

    # ================= EXPENSE =================

    def expense_tab(self):

        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Expenses")

        frame = tk.Frame(tab)

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.ef = tk.StringVar()
        self.ea = tk.StringVar()

        tk.Label(frame, text="Select Farmer").pack()

        self.exp_farmer = ttk.Combobox(
            frame,
            textvariable=self.ef
        )

        self.exp_farmer.pack()
        self.exp_farmer["values"] = self.get_farmers()

        tk.Label(frame, text="Amount").pack()

        tk.Entry(
            frame,
            textvariable=self.ea
        ).pack()

        tk.Button(
            frame,
            text="Add Expense",
            command=self.add_expense
        ).pack(pady=20)

    def add_expense(self):

        if not self.ef.get() or not self.ea.get():
            messagebox.showerror(
                "Error",
                "All fields required"
            )
            return

        farmer_id = self.ef.get().split(" - ")[0]

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO expenses(farmer_id,amount,note,date)
        VALUES(?,?,?,?)
        """, (
            farmer_id,
            self.ea.get(),
            'Expense',
            date.today()
        ))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Expense Added ✅"
        )

    # ================= INCOME =================

    def income_tab(self):

        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Income")

        frame = tk.Frame(tab)

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.ifid = tk.StringVar()
        self.ia = tk.StringVar()

        tk.Label(frame, text="Select Farmer").pack()

        self.inc_farmer = ttk.Combobox(
            frame,
            textvariable=self.ifid
        )

        self.inc_farmer.pack()
        self.inc_farmer["values"] = self.get_farmers()

        tk.Label(frame, text="Amount").pack()

        tk.Entry(
            frame,
            textvariable=self.ia
        ).pack()

        tk.Button(
            frame,
            text="Add Income",
            command=self.add_income
        ).pack(pady=20)

    def add_income(self):

        if not self.ifid.get() or not self.ia.get():
            messagebox.showerror(
                "Error",
                "All fields required"
            )
            return

        farmer_id = self.ifid.get().split(" - ")[0]

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO income(farmer_id,amount,date)
        VALUES(?,?,?)
        """, (
            farmer_id,
            self.ia.get(),
            date.today()
        ))

        con.commit()
        con.close()

        messagebox.showinfo(
            "Success",
            "Income Added ✅"
        )

    # ================= DASHBOARD =================

    def dashboard_tab(self):

        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Dashboard")

        self.df = tk.StringVar()

        tk.Label(
            tab,
            text="Select Farmer"
        ).pack(pady=10)

        self.dash_farmer = ttk.Combobox(
            tab,
            textvariable=self.df
        )

        self.dash_farmer.pack()
        self.dash_farmer["values"] = self.get_farmers()

        tk.Button(
            tab,
            text="Load Dashboard",
            command=self.show_dashboard
        ).pack(pady=20)

        self.result = tk.Frame(tab)
        self.result.pack()

    def show_dashboard(self):

        for w in self.result.winfo_children():
            w.destroy()

        if not self.df.get():
            messagebox.showerror(
                "Error",
                "Select Farmer"
            )
            return

        farmer_id = self.df.get().split(" - ")[0]

        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "SELECT name,land FROM farmers WHERE farmer_id=?",
            (farmer_id,)
        )

        name, land = cur.fetchone()

        cur.execute(
            "SELECT SUM(amount) FROM income WHERE farmer_id=?",
            (farmer_id,)
        )

        income = cur.fetchone()[0] or 0

        cur.execute(
            "SELECT SUM(amount) FROM expenses WHERE farmer_id=?",
            (farmer_id,)
        )

        expense = cur.fetchone()[0] or 0

        con.close()

        profit = income - expense

        for t, v in [
            ("Farmer", name),
            ("Land Acres", land),
            ("Income", income),
            ("Profit", profit)
        ]:

            f = tk.Frame(
                self.result,
                bg=PANEL,
                width=220,
                height=100
            )

            f.pack(
                side="left",
                padx=20,
                pady=20
            )

            tk.Label(
                f,
                text=t,
                bg=PANEL,
                fg=FG
            ).pack()

            tk.Label(
                f,
                text=v,
                bg=PANEL,
                fg=ACC,
                font=("Segoe UI", 16, "bold")
            ).pack()