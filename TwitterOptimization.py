from termcolor import colored
import sys
import getopt
import ParsingFile as pf

def runMH(inputFile):
    pf.parsear(inputFile)
    pass


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg

    runMH(inputfile)

def help():
    print("")
    print("For run Twitter Optimization," + colored(" you must","red") + " set de benchmark file with:")
    print("")
    print("\t" + colored('TwitterOptimization.py -i <scp41.txt>', 'green'))


main(sys.argv[1:])
