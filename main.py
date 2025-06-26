import argparse, time
import matplotlib.pyplot as plt
from round import play_round

def main():
#Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Increases output verbosity, level 1 displays the host and contestants chat and level 2 displays repr information on the objects involved (e.g. -v 1, --verbose 2)",
                        type=int, choices=[1, 2])
    parser.add_argument("-i", "--iterations", type=int, default=1, help="Number of iterations to run (e.g. -i 10, --iterations 100).")
    parser.add_argument("-p", "--plot", action="store_true", help="Display a plot of the results of the simulation.")
    args = parser.parse_args()

# Run simulations based on arguments provided.
    switch_results = []
    switch_cumulative = []
    switch_wins = 0
    keep_results = []
    keep_cumulative = []
    keep_wins = 0

    for i in range(args.iterations):
        result = play_round(True, args.verbose)
        switch_results.append(result)
        switch_wins += int(result)
        switch_cumulative.append(switch_wins / (i + 1))
    print("----------------------------------------------------------------------------------")
    for j in range(args.iterations):
        result = play_round(False, args.verbose)
        keep_results.append(result)
        keep_wins += int(result)
        keep_cumulative.append(keep_wins / (j + 1))

#Display the results.
    print(f"Switching the box resulted in {switch_wins} wins in {args.iterations} iterations.")
    print(f"Keeping the box resulted in {keep_wins} wins in {args.iterations} iterations.")
    if args.plot:
        plt.figure(figsize=(20, 12))
        plt.plot(range(1, args.iterations + 1), switch_cumulative, label="Switch Strategy", color="green")
        plt.plot(range(1, args.iterations + 1), keep_cumulative, label="Keep Strategy", color="red")
        plt.axhline(2/3, color="green", linestyle="--", label="Expected Switch Win Rate (≈66.7%)")
        plt.axhline(1/3, color="red", linestyle="--", label="Expected Keep Win Rate (≈33.3%)")

        plt.xlabel("Number of Rounds")
        plt.ylabel("Cumulative Win Rate")
        plt.title("Monty Hall Simulation: Switch vs. Keep")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    return

if __name__ == "__main__":
    main()