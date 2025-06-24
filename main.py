import sys, getopt
from round import play_round

def main():
    args = sys.argv[1:]
    short_options = 'v'
    long_options = ['verbose', 'trials=']
    optlist, args = getopt.getopt(args, short_options, long_options)
    if any([opt[0]=='-v' or opt[0]=='--verbose' for opt in optlist]):
        verbose = True
    else:
        verbose = False

    play_round(True, verbose)
    print("----------------------------------------------------------------------------------")
    play_round(False, verbose)
    print()
    return

if __name__ == "__main__":
    main()