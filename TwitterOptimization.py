from termcolor import colored
import sys
import getopt
import ParsingFile as pf
verbose = False
population_number_M = 30
number_of_followers_F = 10
number_of_evaluation_N = 10000


def run_mh(inputFile):
    if(verbose):
        print(colored('\n\nBegin of Twitter Optmization\n', 'blue'))
    if(verbose):
        print(colored('Parsing file...', 'yellow'), end='')
    if(pf.parsear(inputFile) and verbose):
            print(colored('OK\n', 'blue'))
    if(verbose):
        print(colored("Rows:\t\t", 'yellow'), colored(pf.filas, 'blue'))
        print(colored("Columns:\t", 'yellow'), colored(pf.columnas, 'blue'), '\n')
        print(colored(pf.matriz_a, 'yellow'))
    if(verbose):
        print(colored('\nInitial twitter user...', 'yellow'), end='')
    list_twitter_users = initial_twitter_user()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nInitial Following...', 'yellow'), end='')
    initial_following()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nRandom Twitt...', 'yellow'), end='')
    random_twitt()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nRandom Re-Twitt...', 'yellow'), end='')
    random_re_twitt()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nFind hottest Twitt...', 'yellow'), end='')
    find_hottest_twitt()
    if (verbose):
        print(colored('OK', 'blue'))



def initial_twitter_user():
    return [None]*population_number_M

def initial_following():
    pass

def random_twitt():
    pass

def random_re_twitt():
    pass

def find_hottest_twitt():
    pass

# Un tweet representa un vector solución.
def empty_tweet():
    return [None] * pf.columnas


def main(argv):
    global verbose
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "h:i:v", ["ifile="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in('-v'):
            verbose = True

    run_mh(inputfile)


def help():
    print("")
    print("For run Twitter Optimization," + colored(" you must", "red") + " set de benchmark file with:")
    print("")
    print("\t" + colored('TwitterOptimization.py -i <scp41.txt>', 'green'))


main(sys.argv[1:])
