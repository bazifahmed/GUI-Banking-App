import tkinter as tk
from tkinter import ttk, messagebox
import random
import string


# ─────────────────────────── Data Models ────────────────────────────

class Account:
    def __init__(self, account_number, owner, student_id, password, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.student_id = student_id
        self.password = password
        self.balance = balance
        self.transactions = []


# ──────────────────────────── App Core ──────────────────────────────

class BankApp:

    # ── Palette ──────────────────────────────────────────────────────
    BG        = "#0d1117"   # near-black canvas
    PANEL     = "#161b22"   # card surface
    BORDER    = "#21262d"   # subtle border
    GOLD      = "#c9a84c"   # warm gold accent
    GOLD_LT   = "#e8c96e"   # hover gold
    TEXT_HI   = "#f0f6fc"   # primary text
    TEXT_MID  = "#8b949e"   # secondary text
    TEXT_DIM  = "#484f58"   # muted text
    GREEN     = "#2ea043"   # success
    RED_ERR   = "#da3633"   # error

    FONT_HEAD = ("Georgia", 22, "bold")
    FONT_SUB  = ("Georgia", 13, "italic")
    FONT_LBL  = ("Helvetica", 10, "bold")
    FONT_VAL  = ("Helvetica", 11)
    FONT_BTN  = ("Helvetica", 11, "bold")
    FONT_TINY = ("Helvetica", 8)
    FONT_BIG  = ("Helvetica", 28, "bold")

    # ── Init ─────────────────────────────────────────────────────────

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Bank Portal")
        self.root.geometry("820x640")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.accounts: dict[str, Account] = {}
        self.current_user: Account | None = None

        self._center()
        self._apply_ttk_styles()
        self.show_home()

    def _center(self):
        self.root.update_idletasks()
        w, h = 820, 640
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _apply_ttk_styles(self):
        s = ttk.Style(self.root)
        s.theme_use("clam")

        s.configure(".",
                     background=self.BG,
                     foreground=self.TEXT_HI,
                     fieldbackground=self.PANEL,
                     font=self.FONT_VAL)

        s.configure("TFrame", background=self.BG)
        s.configure("Card.TFrame", background=self.PANEL)

        s.configure("TLabel", background=self.BG, foreground=self.TEXT_HI)
        s.configure("Dim.TLabel",  background=self.BG,   foreground=self.TEXT_MID, font=self.FONT_TINY)
        s.configure("Card.TLabel", background=self.PANEL, foreground=self.TEXT_HI)

        # Gold primary button
        s.configure("Gold.TButton",
                     background=self.GOLD,
                     foreground=self.BG,
                     font=self.FONT_BTN,
                     padding=(0, 10),
                     relief="flat",
                     borderwidth=0)
        s.map("Gold.TButton",
              background=[("active", self.GOLD_LT), ("pressed", self.GOLD)],
              foreground=[("active", self.BG)])

        # Ghost button
        s.configure("Ghost.TButton",
                     background=self.PANEL,
                     foreground=self.GOLD,
                     font=self.FONT_BTN,
                     padding=(0, 9),
                     relief="flat",
                     borderwidth=1)
        s.map("Ghost.TButton",
              background=[("active", self.BORDER)],
              foreground=[("active", self.GOLD_LT)])

        # Entry
        s.configure("TEntry",
                     fieldbackground="#1c2128",
                     foreground=self.TEXT_HI,
                     insertcolor=self.GOLD,
                     borderwidth=0,
                     relief="flat",
                     padding=8)

    # ── Helpers ───────────────────────────────────────────────────────

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _divider(self, parent, pady=0):
        tk.Frame(parent, bg=self.BORDER, height=1).pack(fill="x", pady=pady)

    def _entry(self, parent, show=None, placeholder=None):
        """A styled entry with an underline-only border feel."""
        container = tk.Frame(parent, bg="#1c2128", highlightbackground=self.BORDER,
                              highlightthickness=1)
        e = tk.Entry(container,
                     bg="#1c2128", fg=self.TEXT_HI,
                     insertbackground=self.GOLD,
                     relief="flat", bd=0,
                     font=self.FONT_VAL,
                     show=show or "")
        e.pack(fill="x", padx=10, pady=8)

        # Placeholder support
        _show_char = show or ""
        if placeholder:
            e.insert(0, placeholder)
            e.configure(fg=self.TEXT_DIM, show="")

            def on_focus_in(_):
                container.configure(highlightbackground=self.GOLD)
                if e.get() == placeholder:
                    e.delete(0, "end")
                    e.configure(fg=self.TEXT_HI, show=_show_char)

            def on_focus_out(_):
                container.configure(highlightbackground=self.BORDER)
                if e.get() == "":
                    e.configure(fg=self.TEXT_DIM, show="")
                    e.insert(0, placeholder)
        else:
            def on_focus_in(_):
                container.configure(highlightbackground=self.GOLD)
            def on_focus_out(_):
                container.configure(highlightbackground=self.BORDER)

        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)

        # Helper to get only real (non-placeholder) value
        def get_real():
            val = e.get()
            return "" if val == placeholder else val
        e.get_real = get_real

        return container, e

    def _label(self, parent, text, font=None, fg=None, bg=None, anchor="w"):
        return tk.Label(parent,
                        text=text,
                        font=font or self.FONT_LBL,
                        fg=fg or self.TEXT_MID,
                        bg=bg or self.BG,
                        anchor=anchor)

    def _btn(self, parent, text, command, style="gold", width=200):
        """style: 'gold' | 'ghost'"""
        if style == "gold":
            bg, fg, hbg = self.GOLD, self.BG, self.GOLD_LT
        else:
            bg, fg, hbg = self.PANEL, self.GOLD, self.BORDER

        btn = tk.Button(parent,
                        text=text,
                        command=command,
                        font=self.FONT_BTN,
                        bg=bg, fg=fg,
                        activebackground=hbg,
                        activeforeground=fg,
                        relief="flat", bd=0,
                        cursor="hand2",
                        width=width)
        btn.pack(fill="x", pady=5, ipady=9)
        return btn

    def _card(self, parent, padx=40, pady=30):
        frm = tk.Frame(parent, bg=self.PANEL,
                        highlightbackground=self.BORDER,
                        highlightthickness=1)
        frm.pack(padx=padx, pady=pady, fill="x")
        return frm

    def _logo_canvas(self, parent, size=80):
        c = tk.Canvas(parent, width=size, height=size,
                      bg=self.BG, highlightthickness=0)
        c.pack(pady=(0, 6))
        r = 8
        x0, y0, x1, y1 = 6, 6, size - 6, size - 6
        # rounded rect background
        c.create_oval(x0, y0, x0 + 2*r, y0 + 2*r, fill=self.GOLD, outline="")
        c.create_oval(x1 - 2*r, y0, x1, y0 + 2*r, fill=self.GOLD, outline="")
        c.create_oval(x0, y1 - 2*r, x0 + 2*r, y1, fill=self.GOLD, outline="")
        c.create_oval(x1 - 2*r, y1 - 2*r, x1, y1, fill=self.GOLD, outline="")
        c.create_rectangle(x0 + r, y0, x1 - r, y1, fill=self.GOLD, outline="")
        c.create_rectangle(x0, y0 + r, x1, y1 - r, fill=self.GOLD, outline="")
        mid = size // 2
        c.create_text(mid, mid, text="🏦", font=("Arial", size // 3))
        return c

    def _footer(self, parent=None):
        p = parent or self.root
        bar = tk.Frame(p, bg=self.PANEL, height=28)
        bar.pack(side="bottom", fill="x")
        tk.Label(bar,
                 text="Project by Bazif & Sawaira  •  Student Bank Portal",
                 font=self.FONT_TINY,
                 fg=self.TEXT_DIM,
                 bg=self.PANEL).pack(pady=6)

    def _generate_account_number(self):
        while True:
            num = "".join(random.choices(string.digits, k=10))
            if num not in self.accounts:
                return num

    # ── Screens ───────────────────────────────────────────────────────

    # ---------- Home / Landing ----------

    def show_home(self):
        self._clear()
        self._footer()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(expand=True, fill="both", padx=0, pady=0)

        # Left decorative strip
        strip = tk.Frame(outer, bg=self.GOLD, width=5)
        strip.pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=self.BG)
        inner.pack(expand=True, fill="both")

        # Vertical centering spacer
        tk.Frame(inner, bg=self.BG, height=80).pack()

        self._logo_canvas(inner, size=90)

        tk.Label(inner, text="Student Bank Portal",
                 font=self.FONT_HEAD, fg=self.GOLD, bg=self.BG).pack()

        tk.Label(inner, text="Secure  ·  Simple  ·  Student-First",
                 font=self.FONT_SUB, fg=self.TEXT_MID, bg=self.BG).pack(pady=(4, 40))

        btn_frame = tk.Frame(inner, bg=self.BG)
        btn_frame.pack()

        def _wide_btn(text, cmd, style):
            b = tk.Button(btn_frame, text=text, command=cmd,
                          font=self.FONT_BTN, width=22,
                          bg=self.GOLD if style == "gold" else self.PANEL,
                          fg=self.BG  if style == "gold" else self.GOLD,
                          activebackground=self.GOLD_LT,
                          activeforeground=self.BG,
                          relief="flat", bd=0, cursor="hand2")
            b.pack(pady=7, ipady=11)

        _wide_btn("  Create Account  ", self.show_create_account, "gold")
        _wide_btn("  Login  ",           self.show_login,          "ghost")

    # ---------- Create Account ----------

    def show_create_account(self):
        self._clear()
        self._footer()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(expand=True, fill="both")

        strip = tk.Frame(outer, bg=self.GOLD, width=5)
        strip.pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=self.BG)
        inner.pack(expand=True, fill="both")

        tk.Frame(inner, bg=self.BG, height=40).pack()

        tk.Label(inner, text="Create Account",
                 font=self.FONT_HEAD, fg=self.GOLD, bg=self.BG).pack()
        tk.Label(inner, text="Fill in your details below",
                 font=self.FONT_SUB, fg=self.TEXT_MID, bg=self.BG).pack(pady=(2, 24))

        card = self._card(inner, padx=140, pady=0)
        card_inner = tk.Frame(card, bg=self.PANEL)
        card_inner.pack(fill="x", padx=30, pady=24)

        fields = {}

        PLACEHOLDERS = {
            "name":     "John Doe",
            "sid":      "202xx-12345",
            "password": None,
        }

        def field(label, key, show=None):
            tk.Label(card_inner, text=label,
                     font=self.FONT_LBL, fg=self.TEXT_MID, bg=self.PANEL,
                     anchor="w").pack(fill="x", pady=(10, 2))
            cont, ent = self._entry(card_inner, show=show, placeholder=PLACEHOLDERS[key])
            cont.configure(highlightbackground=self.BORDER)
            cont.pack(fill="x")
            return ent

        fields["name"]     = field("FULL NAME",   "name")
        fields["sid"]      = field("STUDENT ID",  "sid")
        fields["password"] = field("PASSWORD",    "password", show="•")

        self._divider(card_inner, pady=16)

        def _get(key):
            e = fields[key]
            return e.get_real().strip() if hasattr(e, "get_real") else e.get().strip()

        def do_create():
            n, s, p = _get("name"), _get("sid"), _get("password")
            if not all([n, s, p]):
                messagebox.showerror("Missing Fields", "Please fill in all fields.", parent=self.root)
                return

            # Duplicate Student ID check
            existing_sids = {acc.student_id for acc in self.accounts.values()}
            if s in existing_sids:
                messagebox.showerror(
                    "Student ID Already Registered",
                    f"An account with Student ID  '{s}'  already exists.\n"
                    "Each student may only hold one account.",
                    parent=self.root)
                return

            acc_no = self._generate_account_number()
            self.accounts[acc_no] = Account(acc_no, n, s, p)
            messagebox.showinfo(
                "Account Created",
                f"Welcome, {n}!\n\nYour Account Number:\n{acc_no}\n\nKeep it safe.",
                parent=self.root)
            self.show_home()

        tk.Button(card_inner, text="Create Account", command=do_create,
                  font=self.FONT_BTN, bg=self.GOLD, fg=self.BG,
                  activebackground=self.GOLD_LT, activeforeground=self.BG,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=10, pady=(0, 4))

        tk.Button(card_inner, text="← Back", command=self.show_home,
                  font=self.FONT_BTN, bg=self.PANEL, fg=self.TEXT_MID,
                  activebackground=self.BORDER, activeforeground=self.TEXT_HI,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=8)

    # ---------- Login ----------

    def show_login(self):
        self._clear()
        self._footer()

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(expand=True, fill="both")

        strip = tk.Frame(outer, bg=self.GOLD, width=5)
        strip.pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=self.BG)
        inner.pack(expand=True, fill="both")

        tk.Frame(inner, bg=self.BG, height=60).pack()

        tk.Label(inner, text="Welcome Back",
                 font=self.FONT_HEAD, fg=self.GOLD, bg=self.BG).pack()
        tk.Label(inner, text="Sign in to your account",
                 font=self.FONT_SUB, fg=self.TEXT_MID, bg=self.BG).pack(pady=(2, 28))

        card = self._card(inner, padx=160, pady=0)
        ci = tk.Frame(card, bg=self.PANEL)
        ci.pack(fill="x", padx=30, pady=24)

        tk.Label(ci, text="ACCOUNT NUMBER",
                 font=self.FONT_LBL, fg=self.TEXT_MID, bg=self.PANEL,
                 anchor="w").pack(fill="x", pady=(0, 2))
        _, acc_e = self._entry(ci)
        acc_e.master.pack(fill="x")

        tk.Label(ci, text="PASSWORD",
                 font=self.FONT_LBL, fg=self.TEXT_MID, bg=self.PANEL,
                 anchor="w").pack(fill="x", pady=(12, 2))
        _, pass_e = self._entry(ci, show="•")
        pass_e.master.pack(fill="x")

        self._divider(ci, pady=16)

        def do_login():
            acc, pw = acc_e.get().strip(), pass_e.get().strip()
            if acc in self.accounts and self.accounts[acc].password == pw:
                self.current_user = self.accounts[acc]
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed",
                                     "Invalid account number or password.",
                                     parent=self.root)

        # bind Enter key
        self.root.bind("<Return>", lambda _: do_login())

        tk.Button(ci, text="Login", command=do_login,
                  font=self.FONT_BTN, bg=self.GOLD, fg=self.BG,
                  activebackground=self.GOLD_LT, activeforeground=self.BG,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=10, pady=(0, 4))

        tk.Button(ci, text="← Back", command=lambda: [self.root.unbind("<Return>"), self.show_home()],
                  font=self.FONT_BTN, bg=self.PANEL, fg=self.TEXT_MID,
                  activebackground=self.BORDER, activeforeground=self.TEXT_HI,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=8)

    # ---------- Dashboard ----------

    def show_dashboard(self):
        self._clear()
        self.root.unbind("<Return>")

        # Top nav bar
        nav = tk.Frame(self.root, bg=self.PANEL, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        tk.Label(nav, text="🏦  Student Bank Portal",
                 font=("Helvetica", 12, "bold"),
                 fg=self.GOLD, bg=self.PANEL).pack(side="left", padx=20, pady=14)

        tk.Button(nav, text="Logout",
                  command=self.show_home,
                  font=self.FONT_TINY,
                  bg=self.BG, fg=self.TEXT_MID,
                  activebackground=self.RED_ERR,
                  activeforeground="white",
                  relief="flat", bd=0, cursor="hand2",
                  padx=12).pack(side="right", padx=16, pady=12)

        tk.Label(nav, text=f"  {self.current_user.owner}",
                 font=("Helvetica", 10), fg=self.TEXT_MID, bg=self.PANEL).pack(side="right")

        self._footer()

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(expand=True, fill="both", padx=40, pady=24)

        # ── Balance card ─────────────────────────────────────────────
        bal_card = tk.Frame(body, bg=self.GOLD,
                             highlightbackground=self.GOLD, highlightthickness=1)
        bal_card.pack(fill="x", pady=(0, 20))

        inner_bc = tk.Frame(bal_card, bg=self.GOLD)
        inner_bc.pack(padx=28, pady=20)

        tk.Label(inner_bc, text="AVAILABLE BALANCE",
                 font=self.FONT_LBL, fg=self.BG, bg=self.GOLD).pack(anchor="w")

        self.balance_var = tk.StringVar(value=f"${self.current_user.balance:,.2f}")
        tk.Label(inner_bc, textvariable=self.balance_var,
                 font=self.FONT_BIG, fg=self.BG, bg=self.GOLD).pack(anchor="w")

        tk.Label(inner_bc,
                 text=f"Acct  •  {self.current_user.account_number[:4]} ···· {self.current_user.account_number[-4:]}",
                 font=("Helvetica", 9), fg="#7a6024", bg=self.GOLD).pack(anchor="w", pady=(4, 0))

        # ── Action buttons ────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=self.BG)
        btn_row.pack(fill="x", pady=(0, 20))

        for col in range(2):
            btn_row.columnconfigure(col, weight=1)

        actions = [
            ("↓  Deposit",  self.show_deposit,  "gold"),
            ("↑  Withdraw", self.show_withdraw, "ghost"),
        ]

        for i, (lbl, cmd, sty) in enumerate(actions):
            bg = self.GOLD if sty == "gold" else self.PANEL
            fg = self.BG  if sty == "gold" else self.GOLD
            hbg = self.GOLD_LT if sty == "gold" else self.BORDER
            b = tk.Button(btn_row, text=lbl, command=cmd,
                          font=self.FONT_BTN,
                          bg=bg, fg=fg,
                          activebackground=hbg,
                          activeforeground=fg,
                          relief="flat", bd=0, cursor="hand2")
            b.grid(row=0, column=i, padx=(0, 8) if i == 0 else (8, 0),
                   sticky="ew", ipady=12)

        # ── Transaction log ───────────────────────────────────────────
        log_label = tk.Frame(body, bg=self.BG)
        log_label.pack(fill="x")
        tk.Label(log_label, text="RECENT ACTIVITY",
                 font=self.FONT_LBL, fg=self.TEXT_MID, bg=self.BG).pack(side="left")

        log_card = tk.Frame(body, bg=self.PANEL,
                             highlightbackground=self.BORDER, highlightthickness=1)
        log_card.pack(fill="both", expand=True, pady=(8, 0))

        self.log_frame = tk.Frame(log_card, bg=self.PANEL)
        self.log_frame.pack(fill="both", expand=True, padx=16, pady=12)

        self._refresh_log()

    def _refresh_log(self):
        for w in self.log_frame.winfo_children():
            w.destroy()

        txns = self.current_user.transactions
        if not txns:
            tk.Label(self.log_frame, text="No transactions yet",
                     font=self.FONT_VAL, fg=self.TEXT_DIM, bg=self.PANEL).pack(pady=20)
            return

        for txn in reversed(txns[-8:]):
            row = tk.Frame(self.log_frame, bg=self.PANEL)
            row.pack(fill="x", pady=3)

            icon = "↓" if txn[0] == "D" else "↑"
            clr  = self.GREEN if txn[0] == "D" else self.RED_ERR

            tk.Label(row, text=icon, font=("Helvetica", 13, "bold"),
                     fg=clr, bg=self.PANEL, width=2).pack(side="left")
            tk.Label(row, text=txn[1],
                     font=self.FONT_VAL, fg=self.TEXT_HI, bg=self.PANEL).pack(side="left", padx=8)
            tk.Label(row, text=txn[2],
                     font=("Helvetica", 11, "bold"),
                     fg=clr, bg=self.PANEL).pack(side="right")
            self._divider(self.log_frame)

    # ---------- Transaction Modal ----------

    def _transaction_modal(self, title, action_fn):
        modal = tk.Toplevel(self.root)
        modal.title(title)
        modal.geometry("360x240")
        modal.resizable(False, False)
        modal.configure(bg=self.BG)
        modal.grab_set()

        # center modal
        modal.update_idletasks()
        rx = self.root.winfo_rootx() + (820 - 360) // 2
        ry = self.root.winfo_rooty() + (640 - 240) // 2
        modal.geometry(f"360x240+{rx}+{ry}")

        tk.Label(modal, text=title,
                 font=("Georgia", 16, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(24, 4))
        tk.Label(modal, text="Enter amount in USD",
                 font=self.FONT_VAL, fg=self.TEXT_MID, bg=self.BG).pack()

        cont = tk.Frame(modal, bg="#1c2128",
                         highlightbackground=self.BORDER, highlightthickness=1)
        cont.pack(padx=40, pady=16, fill="x")

        prefix = tk.Label(cont, text="$", font=("Helvetica", 14, "bold"),
                          fg=self.GOLD, bg="#1c2128")
        prefix.pack(side="left", padx=(10, 0), pady=8)

        amt_e = tk.Entry(cont, bg="#1c2128", fg=self.TEXT_HI,
                         insertbackground=self.GOLD, relief="flat",
                         font=("Helvetica", 14), bd=0)
        amt_e.pack(side="left", fill="x", expand=True, padx=6, pady=8)
        amt_e.focus_set()

        def on_focus_in(_):  cont.configure(highlightbackground=self.GOLD)
        def on_focus_out(_): cont.configure(highlightbackground=self.BORDER)
        amt_e.bind("<FocusIn>",  on_focus_in)
        amt_e.bind("<FocusOut>", on_focus_out)

        btn_row = tk.Frame(modal, bg=self.BG)
        btn_row.pack(padx=40, fill="x")

        def confirm():
            try:
                amt = float(amt_e.get())
                if amt <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid", "Enter a valid positive amount.", parent=modal)
                return
            result = action_fn(amt)
            if result:
                self.balance_var.set(f"${self.current_user.balance:,.2f}")
                self._refresh_log()
                modal.destroy()

        tk.Button(btn_row, text="Confirm", command=confirm,
                  font=self.FONT_BTN, bg=self.GOLD, fg=self.BG,
                  activebackground=self.GOLD_LT, activeforeground=self.BG,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=9, pady=(0, 4))
        tk.Button(btn_row, text="Cancel", command=modal.destroy,
                  font=self.FONT_BTN, bg=self.PANEL, fg=self.TEXT_MID,
                  activebackground=self.BORDER, activeforeground=self.TEXT_HI,
                  relief="flat", bd=0, cursor="hand2").pack(fill="x", ipady=8)

        modal.bind("<Return>", lambda _: confirm())

    def show_deposit(self):
        def deposit(amt):
            self.current_user.balance += amt
            self.current_user.transactions.append(("D", "Deposit", f"+${amt:,.2f}"))
            return True
        self._transaction_modal("Deposit", deposit)

    def show_withdraw(self):
        def withdraw(amt):
            if amt > self.current_user.balance:
                messagebox.showerror("Insufficient Funds",
                                     f"Balance: ${self.current_user.balance:,.2f}",
                                     parent=self.root)
                return False
            self.current_user.balance -= amt
            self.current_user.transactions.append(("W", "Withdrawal", f"-${amt:,.2f}"))
            return True
        self._transaction_modal("Withdraw", withdraw)


# ────────────────────────── Entry Point ─────────────────────────────

def main():
    root = tk.Tk()
    BankApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()