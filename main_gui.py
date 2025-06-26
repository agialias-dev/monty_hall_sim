import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox, scrolledtext
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
        self.output_area = scrolledtext.ScrolledText(root, height=30, width=120, state="disabled", wrap="word")
        self.output_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Run button
        run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=3, column=0, columnspan=2, pady=10)

    def run_simulation(self):
        try:
            iterations = int(self.iterations_entry.get())
            verbosity = self.verbosity_var.get()
            plotting = self.plot_option.get()

            switch_wins = 0
            keep_wins = 0

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

            # Run simulations
            switch_results = []
            keep_results = []
            switch_cumulative = []
            keep_cumulative = []

            switch_wins = 0
            for i in range(iterations):
                result = play_round(True, verbosity)
                switch_results.append(result)
                switch_wins += int(result)
                switch_cumulative.append(switch_wins / (i + 1))
            if verbosity > 0:
                print("\n" + "-" * 60)
            keep_wins = 0
            for i in range(iterations):
                result = play_round(False, verbosity)
                keep_results.append(result)
                keep_wins += int(result)
                keep_cumulative.append(keep_wins / (i + 1))

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

            if plotting:
                plt.figure(figsize=(10, 6))
                plt.plot(range(1, iterations + 1), switch_cumulative, label="Switch Strategy", color="green")
                plt.plot(range(1, iterations + 1), keep_cumulative, label="Keep Strategy", color="red")
                plt.axhline(2/3, color="green", linestyle="--", label="Expected Switch Win Rate (≈66.7%)")
                plt.axhline(1/3, color="red", linestyle="--", label="Expected Keep Win Rate (≈33.3%)")

                plt.xlabel("Number of Rounds")
                plt.ylabel("Cumulative Win Rate")
                plt.title("Monty Hall Simulation: Switch vs. Keep")
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of iterations.")

# Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MontyHallApp(root)
    root.mainloop()