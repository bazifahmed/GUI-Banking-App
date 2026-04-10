import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class Account:
    def __init__(self, account_number, owner, student_id, password, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.student_id = student_id
        self.password = password
        self.balance = balance

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Bank Portal")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.center_window()

        self.accounts = {}
        self.current_user = None

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.show_login_screen()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_styles(self):
        # Color palette inspired by logo
        self.bg_color = "#ffc8bf"
        self.primary = "#c62828"     # deep red
        self.dark = "#1a1a1a"        # black
        self.light = "#ffffff"

        self.root.configure(bg=self.bg_color)

        self.style.configure('TFrame', background=self.bg_color)

        self.style.configure('Title.TLabel',
                             font=('Arial', 20, 'bold'),
                             foreground=self.primary,
                             background=self.bg_color)

        self.style.configure('Bank.TLabel',
                             font=('Arial', 12, 'bold'),
                             foreground=self.dark,
                             background=self.bg_color)

        self.style.configure('Bank.TButton',
                             font=('Arial', 11, 'bold'),
                             foreground='white',
                             background=self.primary,
                             padding=10)

        self.style.map('Bank.TButton',
                       background=[('active', "#da5050")])

    def add_footer(self):
        footer = tk.Frame(self.root, bg=self.dark, height=30)
        footer.pack(side='bottom', fill='x')

        label = tk.Label(footer,
                         text="Project by Bazif & Sawaira",
                         fg="white",
                         bg=self.dark,
                         font=('Arial', 9, 'bold'))
        label.pack(pady=5)

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="50")
        main_frame.pack(expand=True, fill='both')

        title_label = ttk.Label(main_frame, text="Student Bank Portal",
                               style='Title.TLabel')
        title_label.pack(pady=30)

        # Logo-style circle
        canvas = tk.Canvas(main_frame, width=100, height=100,
                           bg=self.bg_color, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 90, 90, fill=self.primary, outline="")
        canvas.create_text(50, 50, text='🏦', font=('Arial', 30, 'bold'), fill="white")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=50)

        ttk.Button(btn_frame, text="Create Account",
                   command=self.show_create_account,
                   style='Bank.TButton').pack(pady=10, ipadx=50)

        ttk.Button(btn_frame, text="Login",
                   command=self.show_login,
                   style='Bank.TButton').pack(pady=10, ipadx=80)

        self.add_footer()

    def show_create_account(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="50")
        main_frame.pack(expand=True, fill='both')

        ttk.Label(main_frame, text="Create New Account",
                  style='Title.TLabel').pack(pady=20)

        form_frame = ttk.LabelFrame(main_frame, text="Account Info", padding="20")
        form_frame.pack(pady=20, padx=50, fill='x')

        ttk.Label(form_frame, text="Full Name:", style='Bank.TLabel').grid(row=0, column=0, pady=10)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Student ID:", style='Bank.TLabel').grid(row=1, column=0, pady=10)
        self.student_id_entry = ttk.Entry(form_frame)
        self.student_id_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Password:", style='Bank.TLabel').grid(row=2, column=0, pady=10)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)

        ttk.Button(btn_frame, text="Done", command=self.create_account,
                   style='Bank.TButton').pack(side='left', padx=10)

        ttk.Button(btn_frame, text="Back", command=self.show_login_screen,
                   style='Bank.TButton').pack(side='left', padx=10)

        self.add_footer()

    def generate_account_number(self):
        while True:
            num = ''.join(random.choices(string.digits, k=10))
            if num not in self.accounts:
                return num

    def create_account(self):
        name = self.name_entry.get()
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()

        if not all([name, student_id, password]):
            messagebox.showerror("Error", "Fill all fields!")
            return

        acc = self.generate_account_number()
        self.accounts[acc] = Account(acc, name, student_id, password)

        messagebox.showinfo("Success", f"Account Created!\nAccount No: {acc}")
        self.show_login_screen()

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="50")
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Login", style='Title.TLabel').pack(pady=20)

        ttk.Label(frame, text="Account No:", style='Bank.TLabel').pack()
        self.login_acc = ttk.Entry(frame)
        self.login_acc.pack()

        ttk.Label(frame, text="Password:", style='Bank.TLabel').pack()
        self.login_pass = ttk.Entry(frame, show="*")
        self.login_pass.pack()

        ttk.Button(frame, text="Login", command=self.login,
                   style='Bank.TButton').pack(pady=20)

        ttk.Button(frame, text="Back", command=self.show_login_screen,
                   style='Bank.TButton').pack()

        self.add_footer()

    def login(self):
        acc = self.login_acc.get()
        pw = self.login_pass.get()

        if acc in self.accounts and self.accounts[acc].password == pw:
            self.current_user = self.accounts[acc]
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid login!")

    def dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text=f"Welcome {self.current_user.owner}",
                  style='Title.TLabel').pack(pady=20)

        ttk.Button(frame, text="Check Balance",
                   command=self.check_balance,
                   style='Bank.TButton').pack(pady=10)

        ttk.Button(frame, text="Deposit",
                   command=self.show_deposit,
                   style='Bank.TButton').pack(pady=10)

        ttk.Button(frame, text="Withdraw",
                   command=self.show_withdraw,
                   style='Bank.TButton').pack(pady=10)

        ttk.Button(frame, text="Logout",
                   command=self.show_login_screen,
                   style='Bank.TButton').pack(pady=20)

        self.add_footer()

    def check_balance(self):
        messagebox.showinfo("Balance", f"${self.current_user.balance:.2f}")

    def show_deposit(self):
        self.transaction("Deposit", self.deposit)

    def show_withdraw(self):
        self.transaction("Withdraw", self.withdraw)

    def transaction(self, title, func):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("300x200")

        ttk.Label(win, text=title, style='Title.TLabel').pack(pady=10)

        entry = ttk.Entry(win)
        entry.pack()

        def go():
            try:
                amt = float(entry.get())
                func(amt)
                win.destroy()
            except:
                messagebox.showerror("Error", "Invalid amount")

        ttk.Button(win, text="Confirm", command=go,
                   style='Bank.TButton').pack(pady=10)

    def deposit(self, amt):
        if amt > 0:
            self.current_user.balance += amt
            messagebox.showinfo("Success", "Deposited")

    def withdraw(self, amt):
        if 0 < amt <= self.current_user.balance:
            self.current_user.balance -= amt
            messagebox.showinfo("Success", "Withdrawn")
        else:
            messagebox.showerror("Error", "Insufficient funds")

def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()