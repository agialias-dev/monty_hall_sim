import argparse
from round import play_round

def main():
#Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Increases output verbosity, level 1 displays the host and contestants chat and level 2 displays repr information on the objects involved (e.g. -v 1, --verbose 2)",
                        type=int, choices=[1, 2])
    parser.add_argument("-i", "--iterations", type=int, default=1, help="Number of iterations to run (e.g. -i 10, --iterations 100).")
    args = parser.parse_args()

# Run simulations based on arguments provided.
    switch_wins = 0
    keep_wins = 0
    i = 1
    while i <= args.iterations:
        sw = play_round(True, args.verbose)
        i += 1
        if sw == True:
            switch_wins += 1
    print("----------------------------------------------------------------------------------")
    i = 1
    while i <= args.iterations:
        kw = play_round(False, args.verbose)
        i += 1
        if kw == True:
            keep_wins += 1

#Display the results.
    print(f"Switching the box resulted in {switch_wins} wins in {args.iterations} iterations.")
    print(f"Keeping the box resulted in {keep_wins} wins in {args.iterations} iterations.")
    return

if __name__ == "__main__":
    main()