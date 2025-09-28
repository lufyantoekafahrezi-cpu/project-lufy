import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper - Python")

        # Default settings
        self.rows = 9
        self.cols = 9
        self.mines_count = 10

        self.first_click = True
        self.started_time = None
        self.timer_id = None

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        top = tk.Frame(self.root)
        top.pack(padx=8, pady=6, anchor="w")

        tk.Label(top, text="Rows:").pack(side=tk.LEFT)
        self.entry_rows = tk.Entry(top, width=4)
        self.entry_rows.insert(0, str(self.rows))
        self.entry_rows.pack(side=tk.LEFT, padx=(0,6))

        tk.Label(top, text="Cols:").pack(side=tk.LEFT)
        self.entry_cols = tk.Entry(top, width=4)
        self.entry_cols.insert(0, str(self.cols))
        self.entry_cols.pack(side=tk.LEFT, padx=(0,6))

        tk.Label(top, text="Mines:").pack(side=tk.LEFT)
        self.entry_mines = tk.Entry(top, width=5)
        self.entry_mines.insert(0, str(self.mines_count))
        self.entry_mines.pack(side=tk.LEFT, padx=(0,6))

        btn_start = tk.Button(top, text="Start / Restart", command=self.on_restart_click)
        btn_start.pack(side=tk.LEFT, padx=(4,0))

        self.timer_label = tk.Label(top, text="Time: 0s", width=10)
        self.timer_label.pack(side=tk.LEFT, padx=(10,0))

        self.flags_label = tk.Label(top, text="Flags: 0")
        self.flags_label.pack(side=tk.LEFT, padx=(10,0))

        # Frame for board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=8, pady=8)

    def on_restart_click(self):
        try:
            r = int(self.entry_rows.get())
            c = int(self.entry_cols.get())
            m = int(self.entry_mines.get())
            if r <= 0 or c <= 0 or m <= 0 or m >= r*c:
                raise ValueError
            self.rows, self.cols, self.mines_count = r, c, m
        except ValueError:
            messagebox.showerror("Invalid", "Masukkan angka valid untuk rows, cols, mines (mines < rows*cols).")
            return
        self.reset_game()

    def reset_game(self):
        # stop timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.started_time = None
        self.timer_label.config(text="Time: 0s")

        self.first_click = True
        self.flags = 0
        self.flags_label.config(text=f"Flags: {self.flags}")
        self.game_over = False

        # clear previous widgets
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # model
        self.mines = [[False]*self.cols for _ in range(self.rows)]
        self.values = [[0]*self.cols for _ in range(self.rows)]
        self.revealed = [[False]*self.cols for _ in range(self.rows)]
        self.flagged = [[False]*self.cols for _ in range(self.rows)]
        self.buttons = [[None]*self.cols for _ in range(self.rows)]

        # create buttons
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.board_frame, width=3, height=1, text="",
                                font=("Helvetica", 14),
                                command=lambda rr=r, cc=c: self.on_left_click(rr, cc))
                btn.grid(row=r, column=c)
                # right click (Windows/Linux)
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                # some Mac OS right click may be Button-2
                btn.bind("<Button-2>", lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                self.buttons[r][c] = btn

    def start_timer(self):
        if not self.started_time:
            self.started_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.started_time and not self.game_over:
            elapsed = int(time.time() - self.started_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.timer_id = self.root.after(1000, self.update_timer)

    def place_mines(self, safe_r, safe_c):
        # place mines randomly but avoid the first clicked cell and its neighbors
        cells = [(r,c) for r in range(self.rows) for c in range(self.cols)]
        forbidden = set()
        for rr in range(max(0,safe_r-1), min(self.rows, safe_r+2)):
            for cc in range(max(0,safe_c-1), min(self.cols, safe_c+2)):
                forbidden.add((rr,cc))
        candidates = [cell for cell in cells if cell not in forbidden]
        chosen = random.sample(candidates, self.mines_count)
        for (r,c) in chosen:
            self.mines[r][c] = True

        # compute numbers
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mines[r][c]:
                    self.values[r][c] = -1
                else:
                    count = 0
                    for rr in range(max(0,r-1), min(self.rows, r+2)):
                        for cc in range(max(0,c-1), min(self.cols, c+2)):
                            if self.mines[rr][cc]:
                                count += 1
                    self.values[r][c] = count

    def on_left_click(self, r, c):
        if self.game_over or self.flagged[r][c]:
            return

        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            self.start_timer()

        if self.mines[r][c]:
            # hit mine -> game over
            self.reveal_mine(r, c, exploded=True)
            self.end_game(False)
            return

        self.reveal_cell(r, c)
        if self.check_win():
            self.end_game(True)

    def reveal_cell(self, r, c):
        if self.revealed[r][c] or self.flagged[r][c]:
            return
        self.revealed[r][c] = True
        val = self.values[r][c]
        btn = self.buttons[r][c]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        if val == 0:
            btn.config(text="")
            # flood fill neighbors
            for rr in range(max(0,r-1), min(self.rows, r+2)):
                for cc in range(max(0,c-1), min(self.cols, c+2)):
                    if not self.revealed[rr][cc]:
                        self.reveal_cell(rr, cc)
        else:
            btn.config(text=str(val), disabledforeground=self.get_color_for_number(val))

    def reveal_mine(self, r, c, exploded=False):
        # reveal all mines when game over
        for rr in range(self.rows):
            for cc in range(self.cols):
                if self.mines[rr][cc]:
                    b = self.buttons[rr][cc]
                    b.config(text="*", disabledforeground="black", relief=tk.SUNKEN, state=tk.DISABLED)
        if exploded:
            # mark the clicked mine differently
            b = self.buttons[r][c]
            b.config(bg="red")

    def on_right_click(self, r, c):
        if self.game_over or self.revealed[r][c]:
            return
        if not self.flagged[r][c]:
            # place flag
            self.flagged[r][c] = True
            self.buttons[r][c].config(text="⚑", disabledforeground="blue")
            self.flags += 1
        else:
            # remove flag
            self.flagged[r][c] = False
            self.buttons[r][c].config(text="")
            self.flags -= 1
        self.flags_label.config(text=f"Flags: {self.flags}")

    def check_win(self):
        # win if all non-mine cells are revealed
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.mines[r][c] and not self.revealed[r][c]:
                    return False
        return True

    def end_game(self, won):
        self.game_over = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        # reveal all mines
        self.reveal_mine(-1, -1, exploded=False)
        if won:
            elapsed = int(time.time() - self.started_time) if self.started_time else 0
            messagebox.showinfo("Selamat!", f"Kamu menang!\nWaktu: {elapsed}s")
        else:
            messagebox.showinfo("Game Over", "Kamu kena bom!")

    @staticmethod
    def get_color_for_number(n):
        # typical Minesweeper color mapping for numbers
        colors = {
            1: "#0000FF",  # blue
            2: "#008200",  # green
            3: "#FF0000",  # red
            4: "#000084",
            5: "#840000",
            6: "#008284",
            7: "#000000",
            8: "#808080",
        }
        return colors.get(n, "black")

if __name__ == "__main__":
    root = tk.Tk()
    app = Minesweeper(root)
    root.mainloop()

