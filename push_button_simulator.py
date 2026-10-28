from pathlib import Path
import tkinter as tk


STATE_DETAILS = (
    ("BTN_UP0", "L=0", "Hold: I=0"),
    ("BTN_DN1", "L=1", "Hold: I=1"),
    ("BTN_UP1", "L=1", "Hold: I=0"),
    ("BTN_DN0", "L=0", "Hold: I=1"),
)

TRANSITIONS = {
    0: {False: 0, True: 1},
    1: {False: 2, True: 1},
    2: {False: 2, True: 3},
    3: {False: 0, True: 3},
}


def next_state(state, switch_pressed):
    """Return the next state for the current switch input."""
    if state not in TRANSITIONS:
        raise ValueError(f"Unknown FSM state: {state}")
    return TRANSITIONS[state][bool(switch_pressed)]


class PushButtonSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("University of Gibraltar - Push-Button FSM")
        self.root.configure(bg="#f1f5f9")
        self.root.minsize(850, 540)
        self.root.geometry("940x590")
        self.state = 0
        self.switch_pressed = False

        main = tk.Frame(root, bg="#f1f5f9", padx=24, pady=20)
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg="#f1f5f9")
        header.pack(fill="x", pady=(0, 14))

        logo_path = Path(__file__).with_name("logo.png")
        logo = tk.PhotoImage(file=str(logo_path))
        shrink_by = max(1, (max(logo.width(), logo.height()) + 89) // 90)
        self.logo_image = logo.subsample(shrink_by, shrink_by)
        tk.Label(header, image=self.logo_image, bg="#f1f5f9").pack(side="left", padx=(0, 14))

        brand = tk.Frame(header, bg="#f1f5f9")
        brand.pack(side="left", fill="x", expand=True)
        tk.Label(
            brand,
            text="UNIVERSITY OF GIBRALTAR",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5f9",
            fg="#a30d19",
        ).pack(anchor="w")
        tk.Label(
            brand,
            text="Push-Button FSM",
            font=("Segoe UI", 20, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
        ).pack(anchor="w")
        tk.Label(
            brand,
            text="Press and release the switch to toggle the lamp.",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg="#475569",
        ).pack(anchor="w", pady=(2, 0))

        content = tk.Frame(main, bg="#f1f5f9")
        content.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            content,
            width=640,
            height=440,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.draw_diagram()

        panel = tk.Frame(content, bg="#f1f5f9", padx=22, pady=12)
        panel.pack(side="left", fill="y")
        tk.Label(
            panel,
            text="HARDWARE",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5f9",
            fg="#475569",
        ).pack(anchor="w", pady=(8, 10))

        self.lamp = tk.Canvas(
            panel,
            width=150,
            height=100,
            bg="#f1f5f9",
            highlightthickness=0,
        )
        self.lamp.pack(anchor="center")
        self.lamp.create_oval(48, 8, 102, 62, fill="#94a3b8", outline="#64748b", width=3)
        self.lamp.create_text(75, 82, text="LAMP  L=0", font=("Segoe UI", 10, "bold"), fill="#334155")

        self.switch = tk.Button(
            panel,
            text="PUSH",
            font=("Segoe UI", 12, "bold"),
            bg="#e2e8f0",
            fg="#0f172a",
            activebackground="#bfdbfe",
            activeforeground="#0f172a",
            relief="raised",
            padx=24,
            pady=12,
            cursor="hand2",
        )
        self.switch.pack(fill="x", pady=(16, 5))
        self.switch.bind("<ButtonPress-1>", self.press_switch)
        self.switch.bind("<ButtonRelease-1>", self.release_switch)
        self.root.bind("<KeyPress-space>", self.press_switch)
        self.root.bind("<KeyRelease-space>", self.release_switch)

        tk.Label(
            panel,
            text="Click and hold PUSH, then release. You can also hold the Space key.",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#64748b",
            justify="left",
            wraplength=185,
        ).pack(anchor="w", pady=(4, 16))

        tk.Label(
            panel,
            text="CURRENT STATE",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5f9",
            fg="#475569",
        ).pack(anchor="w")
        self.state_label = tk.Label(
            panel,
            font=("Consolas", 12, "bold"),
            bg="#f1f5f9",
            fg="#1d4ed8",
            justify="left",
        )
        self.state_label.pack(anchor="w", pady=(4, 12))

        tk.Button(
            panel,
            text="Reset",
            command=self.reset,
            font=("Segoe UI", 10),
            bg="#e2e8f0",
            fg="#0f172a",
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2",
        ).pack(anchor="w")

        self.update_display()

    def draw_diagram(self):
        canvas = self.canvas
        positions = ((150, 112), (470, 112), (470, 330), (150, 330))
        radius = 62

        for index, (x, y) in enumerate(positions):
            canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill="#e2e8f0",
                outline="#64748b",
                width=2,
                tags=(f"state-bubble-{index}",),
            )
            name, output, hold = STATE_DETAILS[index]
            canvas.create_text(
                x,
                y,
                text=f"S{index}\n{name}\n{output}\n{hold}",
                font=("Segoe UI", 9, "bold"),
                fill="#0f172a",
                justify="center",
                tags=(f"state-label-{index}",),
            )

        arrows = (
            (214, 112, 406, 112, "I=1", 310, 95),
            (470, 176, 470, 266, "I=0", 505, 220),
            (406, 330, 214, 330, "I=1", 310, 348),
            (150, 266, 150, 176, "I=0", 115, 220),
        )
        for x1, y1, x2, y2, label, label_x, label_y in arrows:
            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#475569",
                width=2,
                arrow=tk.LAST,
                arrowshape=(10, 12, 5),
            )
            canvas.create_text(
                label_x,
                label_y,
                text=label,
                font=("Segoe UI", 9, "bold"),
                fill="#334155",
            )

        canvas.create_text(
            310,
            405,
            text="Follow the arrows on a switch change; each state's hold condition is shown inside its bubble.",
            font=("Segoe UI", 9),
            fill="#64748b",
        )

    def set_switch(self, pressed):
        if self.switch_pressed == pressed:
            return
        self.switch_pressed = pressed
        self.state = next_state(self.state, pressed)
        self.update_display()

    def press_switch(self, _event=None):
        self.set_switch(True)

    def release_switch(self, _event=None):
        self.set_switch(False)

    def reset(self):
        self.state = 0
        self.switch_pressed = False
        self.update_display()

    def update_display(self):
        for index in range(len(STATE_DETAILS)):
            active = index == self.state
            self.canvas.itemconfigure(
                f"state-bubble-{index}",
                fill="#bfdbfe" if active else "#e2e8f0",
                outline="#2563eb" if active else "#64748b",
                width=4 if active else 2,
            )

        lamp_on = STATE_DETAILS[self.state][1] == "L=1"
        self.lamp.itemconfigure(
            1,
            fill="#facc15" if lamp_on else "#94a3b8",
            outline="#ca8a04" if lamp_on else "#64748b",
        )
        self.lamp.itemconfigure(2, text=f"LAMP  L={int(lamp_on)}")
        self.switch.configure(
            text="PUSHED" if self.switch_pressed else "PUSH",
            relief="sunken" if self.switch_pressed else "raised",
            bg="#bfdbfe" if self.switch_pressed else "#e2e8f0",
        )
        name, output, _hold = STATE_DETAILS[self.state]
        self.state_label.configure(
            text=f"{name}\nI={int(self.switch_pressed)}   {output}"
        )


if __name__ == "__main__":
    window = tk.Tk()
    PushButtonSimulator(window)
    window.mainloop()
