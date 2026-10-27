import tkinter as tk
from tkinter import ttk


FLOOR_COUNT = 5


def next_floor(active_buttons, current_floor):
    """Return the lowest-numbered pressed floor button, or hold the current floor."""
    buttons = tuple(active_buttons)
    if any(not isinstance(floor, int) or floor < 1 or floor > FLOOR_COUNT for floor in buttons):
        raise ValueError("Floor buttons must be numbered 1 through 5.")
    return min(buttons) if buttons else current_floor


def one_hot_floor(floor):
    if not isinstance(floor, int) or floor < 1 or floor > FLOOR_COUNT:
        raise ValueError("Floor must be numbered 1 through 5.")
    return f"{1 << (floor - 1):05b}"


class ElevatorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Five-Floor Elevator - FSM Demo")
        self.root.configure(bg="#f1f5f9")
        self.root.minsize(780, 560)
        self.root.geometry("850x610")

        self.floor_y = {floor: 445 - (floor - 1) * 88 for floor in range(1, FLOOR_COUNT + 1)}
        self.car_y = float(self.floor_y[1])
        self.current_floor = 1
        self.target_floor = 1
        self.speed = 3.0
        self.animating = False
        self.pressed = set()

        main = tk.Frame(root, bg="#f1f5f9", padx=24, pady=20)
        main.pack(fill="both", expand=True)

        tk.Label(
            main,
            text="Five-Floor Elevator",
            font=("Segoe UI", 20, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
        ).pack(anchor="w")
        tk.Label(
            main,
            text="Press any number of floor buttons. The lowest-numbered pressed floor is served first.",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg="#475569",
        ).pack(anchor="w", pady=(2, 14))

        content = tk.Frame(main, bg="#f1f5f9")
        content.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            content,
            width=500,
            height=500,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.draw_building()

        panel = tk.Frame(content, bg="#f1f5f9", padx=22, pady=12)
        panel.pack(side="left", fill="y")
        tk.Label(
            panel,
            text="DESTINATION",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5f9",
            fg="#475569",
        ).pack(anchor="w", pady=(8, 10))

        self.buttons = {}
        for floor in range(FLOOR_COUNT, 0, -1):
            button = tk.Button(
                panel,
                text=f"B{floor}  -  Floor {floor}",
                command=lambda selected=floor: self.select_floor(selected),
                font=("Segoe UI", 11, "bold"),
                bg="#e2e8f0",
                fg="#0f172a",
                activebackground="#bfdbfe",
                activeforeground="#0f172a",
                relief="flat",
                padx=14,
                pady=9,
                width=22,
                cursor="hand2",
            )
            button.pack(fill="x", pady=4)
            self.buttons[floor] = button

        ttk.Separator(panel, orient="horizontal").pack(fill="x", pady=18)
        tk.Label(
            panel,
            text="FSM output state",
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

        self.motion_label = tk.Label(
            panel,
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg="#475569",
            justify="left",
            wraplength=190,
        )
        self.motion_label.pack(anchor="w")
        tk.Label(
            panel,
            text="One-hot output: one bit is 1 for the selected floor.",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#64748b",
            justify="left",
            wraplength=190,
        ).pack(anchor="w", pady=(18, 0))
        self.update_status()

    def draw_building(self):
        canvas = self.canvas
        canvas.create_rectangle(125, 55, 390, 485, fill="#f8fafc", outline="#334155", width=3)
        canvas.create_rectangle(230, 65, 345, 480, fill="#e2e8f0", outline="#64748b", width=2)
        for floor, y in self.floor_y.items():
            canvas.create_line(126, y + 34, 390, y + 34, fill="#94a3b8", width=2)
            canvas.create_text(
                72,
                y,
                text=f"FLOOR {floor}",
                font=("Segoe UI", 10, "bold"),
                fill="#334155",
            )
            canvas.create_oval(365, y - 6, 377, y + 6, fill="#94a3b8", outline="")
            canvas.create_text(
                404,
                y,
                text=str(floor),
                font=("Segoe UI", 9),
                fill="#64748b",
                anchor="w",
            )
        self.car = canvas.create_rectangle(
            246,
            self.car_y - 25,
            329,
            self.car_y + 25,
            fill="#2563eb",
            outline="#1e3a8a",
            width=2,
        )
        canvas.create_rectangle(
            254,
            self.car_y - 16,
            321,
            self.car_y + 16,
            fill="#dbeafe",
            outline="",
            tags=("car-window",),
        )
        canvas.create_text(
            287,
            self.car_y,
            text="ELEVATOR",
            font=("Segoe UI", 8, "bold"),
            fill="#1e3a8a",
            tags=("car-label",),
        )
        self.car_window = canvas.find_withtag("car-window")[0]
        self.car_label = canvas.find_withtag("car-label")[0]

    def select_floor(self, floor):
        if floor != self.current_floor or self.animating:
            self.pressed.add(floor)
        self.update_status()
        if not self.animating:
            self.step()

    def step(self):
        """One FSM step: the lowest-numbered pressed button picks the next floor."""
        if self.animating:
            return
        if not self.pressed:
            self.motion_label.configure(text="Idle - press one or more floor buttons.")
            return
        self.current_floor = next_floor(self.pressed, self.current_floor)
        self.target_floor = self.current_floor
        self.update_status()
        if abs(self.car_y - self.floor_y[self.target_floor]) < 0.1:
            self.arrive()
        else:
            self.animating = True
            self.animate()

    def arrive(self):
        self.pressed.discard(self.target_floor)
        self.update_status()
        waiting = ", ".join(f"B{f}" for f in sorted(self.pressed))
        suffix = f" Still waiting: {waiting}." if waiting else ""
        self.motion_label.configure(text=f"Arrived at Floor {self.target_floor}.{suffix}")
        self.root.after(600, self.step)

    def animate(self):
        target_y = self.floor_y[self.target_floor]
        difference = target_y - self.car_y
        if abs(difference) <= self.speed:
            self.car_y = float(target_y)
            self.animating = False
            self.arrive()
        else:
            self.car_y += self.speed if difference > 0 else -self.speed
            self.motion_label.configure(text=f"Moving to Floor {self.target_floor}...")

        self.canvas.coords(self.car, 246, self.car_y - 25, 329, self.car_y + 25)
        self.canvas.coords(self.car_window, 254, self.car_y - 16, 321, self.car_y + 16)
        self.canvas.coords(self.car_label, 287, self.car_y)
        if self.animating:
            self.root.after(16, self.animate)

    def update_status(self):
        self.state_label.configure(
            text=f"Floor {self.current_floor}\nF={one_hot_floor(self.current_floor)}"
        )
        for floor, button in self.buttons.items():
            if floor in self.pressed:
                button.configure(
                    text=f"B{floor}  -  Floor {floor}  (pressed)",
                    bg="#fde68a",
                    activebackground="#fcd34d",
                )
            else:
                button.configure(
                    text=f"B{floor}  -  Floor {floor}",
                    bg="#e2e8f0",
                    activebackground="#bfdbfe",
                )


if __name__ == "__main__":
    window = tk.Tk()
    ElevatorSimulator(window)
    window.mainloop()
