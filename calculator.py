import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
from datetime import datetime

# ─── Theme ───────────────────────────────────────────────────────────────────
BG          = "#0f0f13"
SURFACE     = "#1a1a24"
SURFACE2    = "#22222e"
ACCENT      = "#7c6af7"
ACCENT2     = "#a78bfa"
TEXT        = "#f0eeff"
TEXT_DIM    = "#9090b0"
BTN_NUM     = "#1e1e2a"
BTN_OP      = "#2a2040"
BTN_EQ      = "#7c6af7"
BTN_CLEAR   = "#3a1f2e"
BTN_FUNC    = "#1a2535"
DANGER      = "#f06292"
SUCCESS     = "#66bb6a"
FONT_MAIN   = ("Courier New", 13)
FONT_DISP   = ("Courier New", 28, "bold")
FONT_SUB    = ("Courier New", 11)
FONT_BTN    = ("Courier New", 13, "bold")
FONT_TITLE  = ("Courier New", 11, "bold")

# ─── Calculator Logic ─────────────────────────────────────────────────────────
class Calculator:
    def __init__(self):
        self.reset()
        self.history = []

    def reset(self):
        self.expression = ""
        self.display    = "0"
        self.result     = None
        self.just_computed = False

    def append(self, val):
        if self.just_computed:
            if val in "+-×÷%":
                self.expression = str(self.result) + val
            else:
                self.expression = val
            self.just_computed = False
        else:
            if self.expression == "0" and val not in "+-×÷%.":
                self.expression = val
            else:
                self.expression += val
        self.display = self.expression

    def compute(self):
        expr = self.expression
        if not expr:
            return
        try:
            safe = (expr
                    .replace("×", "*")
                    .replace("÷", "/")
                    .replace("^", "**")
                    .replace("%", "/100"))
            result = eval(safe, {"__builtins__": {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            entry = f"{expr} = {result}"
            self.history.append({
                "expr": expr,
                "result": result,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            self.result = result
            self.display = str(result)
            self.expression = str(result)
            self.just_computed = True
            return entry
        except Exception:
            self.display = "Error"
            self.expression = ""
            return None

    def apply_func(self, func):
        try:
            val = float(self.expression or self.display or "0")
            if func == "sin":   res = math.sin(math.radians(val))
            elif func == "cos": res = math.cos(math.radians(val))
            elif func == "tan": res = math.tan(math.radians(val))
            elif func == "log": res = math.log10(val)
            elif func == "ln":  res = math.log(val)
            elif func == "√":   res = math.sqrt(val)
            elif func == "x²":  res = val ** 2
            elif func == "x³":  res = val ** 3
            elif func == "1/x": res = 1 / val
            elif func == "±":   res = -val
            elif func == "π":
                self.expression += str(math.pi)
                self.display = self.expression
                return
            elif func == "e":
                self.expression += str(math.e)
                self.display = self.expression
                return
            else:
                return
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            else:
                res = round(res, 10)
            entry = f"{func}({val}) = {res}"
            self.history.append({
                "expr": f"{func}({val})",
                "result": res,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            self.result = res
            self.display = str(res)
            self.expression = str(res)
            self.just_computed = True
        except Exception:
            self.display = "Error"
            self.expression = ""

    def backspace(self):
        if self.just_computed:
            self.reset()
        elif len(self.expression) > 1:
            self.expression = self.expression[:-1]
            self.display = self.expression
        else:
            self.expression = ""
            self.display = "0"

# ─── Unit Converter ───────────────────────────────────────────────────────────
UNIT_CATEGORIES = {
    "Length": {
        "Meter": 1, "Kilometer": 1000, "Mile": 1609.34,
        "Foot": 0.3048, "Inch": 0.0254, "Centimeter": 0.01,
    },
    "Weight": {
        "Kilogram": 1, "Gram": 0.001, "Pound": 0.453592,
        "Ounce": 0.0283495, "Ton": 1000,
    },
    "Temperature": {
        "Celsius": "C", "Fahrenheit": "F", "Kelvin": "K",
    },
    "Area": {
        "m²": 1, "km²": 1e6, "Acre": 4046.86, "Hectare": 10000, "ft²": 0.0929,
    },
    "Speed": {
        "m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444,
    },
}

def convert_unit(val, cat, frm, to):
    if cat == "Temperature":
        if frm == "Celsius":
            base = val
        elif frm == "Fahrenheit":
            base = (val - 32) * 5/9
        else:
            base = val - 273.15
        if to == "Celsius":     return base
        elif to == "Fahrenheit": return base * 9/5 + 32
        else:                   return base + 273.15
    else:
        units = UNIT_CATEGORIES[cat]
        return val * units[frm] / units[to]

# ─── Main App ─────────────────────────────────────────────────────────────────
class ModernCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Modern Calculator")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Apply ttk style BEFORE building UI to prevent white flash
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=BTN_NUM,
                        background=BTN_NUM,
                        foreground=TEXT,
                        selectbackground=ACCENT,
                        selectforeground=TEXT,
                        arrowcolor=ACCENT2)
        style.map("TCombobox",
                  fieldbackground=[("readonly", BTN_NUM)],
                  selectbackground=[("readonly", BTN_NUM)],
                  selectforeground=[("readonly", TEXT)],
                  background=[("readonly", BTN_NUM)])
        style.configure("Vertical.TScrollbar",
                        background=SURFACE2,
                        troughcolor=BG,
                        arrowcolor=ACCENT2)

        self.withdraw()   # hide until fully built — prevents white flash
        self.calc = Calculator()
        self.current_tab = tk.StringVar(value="calc")
        self._build_ui()
        self.bind("<Key>", self._on_key)
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
        self.deiconify()  # show fully styled window

    # ── UI Shell ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        bar = tk.Frame(self, bg=SURFACE, pady=8)
        bar.pack(fill="x")
        tk.Label(bar, text="✦ MODERN CALCULATOR", font=FONT_TITLE,
                 bg=SURFACE, fg=ACCENT2).pack(side="left", padx=16)

        # Tab buttons
        tab_frame = tk.Frame(bar, bg=SURFACE)
        tab_frame.pack(side="right", padx=10)
        for label, val in [("CALC", "calc"), ("HISTORY", "hist"), ("CONVERT", "conv")]:
            tk.Button(
                tab_frame, text=label, font=("Courier New", 9, "bold"),
                bg=SURFACE, fg=TEXT_DIM, relief="flat", padx=10, cursor="hand2",
                activebackground=SURFACE2, activeforeground=ACCENT2,
                command=lambda v=val: self._switch_tab(v)
            ).pack(side="left", padx=2)

        # Content area
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(fill="both", expand=True)

        self.frames = {}
        self.frames["calc"] = self._build_calc_tab()
        self.frames["hist"] = self._build_history_tab()
        self.frames["conv"] = self._build_converter_tab()
        self._switch_tab("calc")

    def _switch_tab(self, tab):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[tab].pack(fill="both", expand=True)
        self.current_tab.set(tab)
        if tab == "hist":
            self._refresh_history()

    # ── Calculator Tab ────────────────────────────────────────────────────────
    def _build_calc_tab(self):
        frame = tk.Frame(self.content, bg=BG)

        # Display
        disp_frame = tk.Frame(frame, bg=SURFACE, pady=18, padx=18)
        disp_frame.pack(fill="x", padx=12, pady=(12, 6))

        self.sub_label = tk.Label(disp_frame, text="", font=FONT_SUB,
                                  bg=SURFACE, fg=TEXT_DIM, anchor="e")
        self.sub_label.pack(fill="x")

        self.disp_label = tk.Label(disp_frame, text="0", font=FONT_DISP,
                                   bg=SURFACE, fg=TEXT, anchor="e")
        self.disp_label.pack(fill="x")

        # Scientific row
        sci_frame = tk.Frame(frame, bg=BG)
        sci_frame.pack(fill="x", padx=12, pady=(0, 4))
        sci_btns = ["sin", "cos", "tan", "log", "ln", "√",
                    "x²", "x³", "1/x", "π", "e", "±"]
        for i, b in enumerate(sci_btns):
            self._make_btn(sci_frame, b, BTN_FUNC, TEXT_DIM,
                           lambda v=b: self._func(v), 9).grid(
                row=i//6, column=i%6, padx=2, pady=2, sticky="nsew")
        for c in range(6):
            sci_frame.columnconfigure(c, weight=1)

        # Main buttons
        main_frame = tk.Frame(frame, bg=BG)
        main_frame.pack(fill="x", padx=12, pady=4)

        layout = [
            [("C", BTN_CLEAR, DANGER), ("⌫", BTN_CLEAR, DANGER),
             ("%", BTN_OP, ACCENT2),   ("÷", BTN_OP, ACCENT2)],
            [("7", BTN_NUM, TEXT),     ("8", BTN_NUM, TEXT),
             ("9", BTN_NUM, TEXT),     ("×", BTN_OP, ACCENT2)],
            [("4", BTN_NUM, TEXT),     ("5", BTN_NUM, TEXT),
             ("6", BTN_NUM, TEXT),     ("-", BTN_OP, ACCENT2)],
            [("1", BTN_NUM, TEXT),     ("2", BTN_NUM, TEXT),
             ("3", BTN_NUM, TEXT),     ("+", BTN_OP, ACCENT2)],
            [("0", BTN_NUM, TEXT),     (".", BTN_NUM, TEXT),
             ("(", BTN_OP, ACCENT2),  ("=", BTN_EQ, TEXT)],
        ]

        for r, row in enumerate(layout):
            for c, (label, bg, fg) in enumerate(row):
                cmd = self._btn_command(label)
                btn = self._make_btn(main_frame, label, bg, fg, cmd, 13)
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew",
                         ipady=10)
        for c in range(4):
            main_frame.columnconfigure(c, weight=1)

        return frame

    def _make_btn(self, parent, text, bg, fg, cmd, fontsize=13):
        btn = tk.Button(
            parent, text=text, bg=bg, fg=fg,
            font=("Courier New", fontsize, "bold"),
            relief="flat", cursor="hand2",
            activebackground=ACCENT, activeforeground=TEXT,
            command=cmd, bd=0
        )
        def on_enter(e, b=btn, c=bg): b.configure(bg=ACCENT if text=="=" else SURFACE2)
        def on_leave(e, b=btn, c=bg): b.configure(bg=c)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _btn_command(self, label):
        if label == "=":     return self._compute
        if label == "C":     return self._clear
        if label == "⌫":    return self._backspace
        if label == "(":
            return lambda: self._append("(")
        return lambda v=label: self._append(v)

    def _append(self, val):
        self.calc.append(val)
        self._update_display()

    def _func(self, fn):
        self.calc.apply_func(fn)
        self._update_display()

    def _compute(self):
        prev = self.calc.expression
        result = self.calc.compute()
        if result:
            self.sub_label.configure(text=prev)
        self._update_display()

    def _clear(self):
        self.calc.reset()
        self.sub_label.configure(text="")
        self._update_display()

    def _backspace(self):
        self.calc.backspace()
        self._update_display()

    def _update_display(self):
        txt = self.calc.display
        if len(txt) > 16:
            txt = txt[-16:]
        self.disp_label.configure(text=txt)

    def _on_key(self, event):
        key = event.char
        if key in "0123456789.+-*/()%":
            op = key.replace("*", "×").replace("/", "÷")
            self._append(op)
        elif event.keysym in ("Return", "KP_Enter"):
            self._compute()
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym == "Escape":
            self._clear()

    # ── History Tab ───────────────────────────────────────────────────────────
    def _build_history_tab(self):
        frame = tk.Frame(self.content, bg=BG)
        tk.Label(frame, text="CALCULATION HISTORY", font=FONT_TITLE,
                 bg=BG, fg=ACCENT2, pady=10).pack()

        self.hist_frame = tk.Frame(frame, bg=BG)
        self.hist_frame.pack(fill="both", expand=True, padx=12)

        btn_frame = tk.Frame(frame, bg=BG, pady=8)
        btn_frame.pack()
        tk.Button(btn_frame, text="CLEAR HISTORY", font=("Courier New", 10, "bold"),
                  bg=BTN_CLEAR, fg=DANGER, relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self._clear_history).pack()
        return frame

    def _refresh_history(self):
        for w in self.hist_frame.winfo_children():
            w.destroy()
        if not self.calc.history:
            tk.Label(self.hist_frame, text="No calculations yet.",
                     font=FONT_MAIN, bg=BG, fg=TEXT_DIM, pady=40).pack()
            return
        canvas = tk.Canvas(self.hist_frame, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.hist_frame, orient="vertical",
                                  command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)
        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in reversed(self.calc.history):
            card = tk.Frame(scroll_frame, bg=SURFACE, pady=8, padx=12)
            card.pack(fill="x", pady=3)
            tk.Label(card, text=item["time"], font=("Courier New", 9),
                     bg=SURFACE, fg=TEXT_DIM).pack(anchor="w")
            tk.Label(card, text=item["expr"], font=("Courier New", 12),
                     bg=SURFACE, fg=TEXT_DIM).pack(anchor="w")
            tk.Label(card, text=f"= {item['result']}", font=("Courier New", 16, "bold"),
                     bg=SURFACE, fg=ACCENT2).pack(anchor="w")

    def _clear_history(self):
        self.calc.history.clear()
        self._refresh_history()

    # ── Unit Converter Tab ────────────────────────────────────────────────────
    def _build_converter_tab(self):
        frame = tk.Frame(self.content, bg=BG)
        tk.Label(frame, text="UNIT CONVERTER", font=FONT_TITLE,
                 bg=BG, fg=ACCENT2, pady=10).pack()

        inner = tk.Frame(frame, bg=SURFACE, padx=20, pady=20)
        inner.pack(padx=16, pady=8, fill="x")

        # Category
        tk.Label(inner, text="Category", font=FONT_SUB, bg=SURFACE, fg=TEXT_DIM).grid(
            row=0, column=0, sticky="w", pady=4)
        self.conv_cat = tk.StringVar(value="Length")
        cat_menu = ttk.Combobox(inner, textvariable=self.conv_cat,
                                values=list(UNIT_CATEGORIES.keys()),
                                state="readonly", font=FONT_SUB, width=18)
        cat_menu.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(10, 0), pady=4)
        cat_menu.bind("<<ComboboxSelected>>", self._on_cat_change)

        # From / To
        self.conv_from = tk.StringVar(value="Meter")
        self.conv_to   = tk.StringVar(value="Kilometer")
        tk.Label(inner, text="From", font=FONT_SUB, bg=SURFACE, fg=TEXT_DIM).grid(
            row=1, column=0, sticky="w", pady=4)
        self.from_menu = ttk.Combobox(inner, textvariable=self.conv_from,
                                       state="readonly", font=FONT_SUB, width=18)
        self.from_menu.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(10,0), pady=4)

        tk.Label(inner, text="To", font=FONT_SUB, bg=SURFACE, fg=TEXT_DIM).grid(
            row=2, column=0, sticky="w", pady=4)
        self.to_menu = ttk.Combobox(inner, textvariable=self.conv_to,
                                     state="readonly", font=FONT_SUB, width=18)
        self.to_menu.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(10,0), pady=4)

        # Value input
        tk.Label(inner, text="Value", font=FONT_SUB, bg=SURFACE, fg=TEXT_DIM).grid(
            row=3, column=0, sticky="w", pady=4)
        self.conv_val = tk.Entry(inner, font=FONT_MAIN, bg=BTN_NUM, fg=TEXT,
                                  insertbackground=TEXT, relief="flat",
                                  bd=6, width=20)
        self.conv_val.grid(row=3, column=1, columnspan=2, sticky="ew", padx=(10,0), pady=4)
        self.conv_val.insert(0, "1")

        # Convert button
        tk.Button(inner, text="CONVERT →", font=("Courier New", 11, "bold"),
                  bg=BTN_EQ, fg=TEXT, relief="flat", padx=16, pady=8,
                  cursor="hand2", command=self._do_convert).grid(
            row=4, column=0, columnspan=3, pady=12, sticky="ew")

        # Result
        self.conv_result = tk.Label(inner, text="", font=("Courier New", 18, "bold"),
                                     bg=SURFACE, fg=ACCENT2)
        self.conv_result.grid(row=5, column=0, columnspan=3, pady=4)

        inner.columnconfigure(1, weight=1)
        self._on_cat_change()
        return frame

    def _on_cat_change(self, *_):
        cat   = self.conv_cat.get()
        units = list(UNIT_CATEGORIES[cat].keys())
        self.from_menu["values"] = units
        self.to_menu["values"]   = units
        self.conv_from.set(units[0])
        self.conv_to.set(units[1] if len(units) > 1 else units[0])

    def _do_convert(self):
        try:
            val = float(self.conv_val.get())
            cat = self.conv_cat.get()
            frm = self.conv_from.get()
            to  = self.conv_to.get()
            res = convert_unit(val, cat, frm, to)
            if isinstance(res, float):
                res = round(res, 8)
            self.conv_result.configure(
                text=f"{val} {frm} = {res} {to}", fg=ACCENT2)
        except Exception as ex:
            self.conv_result.configure(text=f"Error: {ex}", fg=DANGER)


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ModernCalculator()
    app.mainloop()