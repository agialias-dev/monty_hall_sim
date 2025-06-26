import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib, time
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from round import play_round

class MontyHallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monty Hall Simulator")

        # Iterations input
        tk.Label(root, text="Number of iterations:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.iterations_entry = tk.Entry(root)
        self.iterations_entry.insert(0, "1")
        self.iterations_entry.grid(row=0, column=1, padx=10, pady=5)

        # Verbosity level
        tk.Label(root, text="Verbosity:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.verbosity_var = tk.IntVar(value=0)
        verbosity_frame = tk.Frame(root)
        verbosity_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        for val, label in enumerate(["0 - Silent", "1 - Host Chat", "2 - Debug"]):
            tk.Radiobutton(verbosity_frame, text=label, variable=self.verbosity_var, value=val).pack(anchor="w")

        # Optional plot
        tk.Label(root, text="Display graph of results?").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.plot_option = tk.BooleanVar()
        plot_frame = tk.Frame(root)
        plot_frame.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        tk.Checkbutton(plot_frame, variable=self.plot_option).pack(anchor='e')

        # Output area
        self.output_area = scrolledtext.ScrolledText(root, height=5, width=120, state="disabled", wrap="word")
        self.output_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Run button
        run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Map Plot
        self.figure = None
        self.canvas = None
        self.ax = None
        self.switch_line = None
        self.keep_line = None
        self.plot_frame = tk.Frame(root)
        self.plot_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def run_simulation(self):
        try:
            iterations = int(self.iterations_entry.get())
            verbosity = self.verbosity_var.get()
            plotting = self.plot_option.get()
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.canvas = None
                self.figure = None
                self.ax = None
                self.switch_line = None
                self.keep_line = None
                self.plot_frame.grid_forget()
                self.root.grid_rowconfigure(5, minsize=0)
            if not plotting and self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.canvas = None
                self.plot_frame.grid_remove()
            target_time = 2.5
            sleep = target_time/iterations
            redraw_rate = max(1, iterations // 100)

            self.output_area.config(state="normal")
            self.output_area.delete(1.0, tk.END)

            # Redirect verbose output if verbosity > 0
            if verbosity > 0:
                import sys
                class StdoutRedirector:
                    def __init__(self, widget):
                        self.widget = widget
                    def write(self, message):
                        self.widget.insert(tk.END, message)
                        self.widget.see(tk.END)
                    def flush(self):  # Needed for Python 3 compatibility
                        pass
                sys.stdout = StdoutRedirector(self.output_area)

            # Resize the Output area appropriately
            if verbosity > 0:
                self.output_area.config(height=30)
            else:
                self.output_area.config(height=5)

            # Run simulations
            switch_cumulative = []
            keep_cumulative = []
            if plotting:
                self.plot_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
                self.root.grid_rowconfigure(5, weight=0)
                self.figure = Figure(figsize=(10, 4), dpi=100)
                self.ax = self.figure.add_subplot(111)
                self.ax.set_title("Monty Hall Simulation: Switch vs. Keep")
                self.ax.set_xlabel("Number of Rounds")
                self.ax.set_ylabel("Cumulative Win Rate")
                self.ax.set_xlim(0, int(self.iterations_entry.get()))
                self.ax.set_ylim(0, 1)
                self.ax.grid(True)
                self.switch_line, = self.ax.plot([], [], label="Switch", color="green")
                self.keep_line, = self.ax.plot([], [], label="Keep", color="red")
                self.ax.axhline(2/3, color="green", linestyle="--", label="Expected Switch (66.7%)")
                self.ax.axhline(1/3, color="red", linestyle="--", label="Expected Keep (33.3%)")
                self.ax.legend()
                self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack()

            switch_wins = 0
            for i in range(iterations):
                sw = play_round(True, verbosity)
                switch_wins += int(sw)
                switch_cumulative.append(switch_wins / (i + 1))
                if plotting and (i % redraw_rate == 0 or i == iterations - 1):
                    self.switch_line.set_data(range(1, i + 2), switch_cumulative)
                    self.ax.set_xlim(0, iterations)
                    self.canvas.draw()
                    self.canvas.flush_events()
                    self.root.update_idletasks()
                if plotting:
                    time.sleep(sleep)
            if verbosity > 0:
                print("\n" + "-" * 60 + "\n")
            keep_wins = 0
            for i in range(iterations):
                kw = play_round(False, verbosity)
                keep_wins += int(kw)
                keep_cumulative.append(keep_wins / (i + 1))
                if plotting and (i % redraw_rate == 0 or i == iterations - 1):
                    self.keep_line.set_data(range(1, i + 2), keep_cumulative)
                    self.ax.set_xlim(0, iterations)
                    self.canvas.draw()
                    self.canvas.flush_events()
                    self.root.update_idletasks()
                if plotting:
                    time.sleep(sleep)

            # Reset stdout if redirected
            if verbosity > 0:
                import sys
                sys.stdout = sys.__stdout__

            # Display final result
            result = (
                f"\n--- Results ---\n"
                f"Switching won {switch_wins}/{iterations} times ({(switch_wins/iterations)*100:.2f}%)\n"
                f"Staying won {keep_wins}/{iterations} times ({(keep_wins/iterations)*100:.2f}%)"
            )
            self.output_area.insert(tk.END, result)
            self.output_area.config(state="disabled")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of iterations.")

# Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MontyHallApp(root)
    root.mainloop()