from termcolor import colored
import sys
import getopt
import ParsingFile as pf
verbose = False
population_number_M = 30
number_of_followers_F = 10
number_of_evaluation_N = 10000
twitter_users = [None]


def run_mh(inputFile):
    global twitter_users
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
    twitter_users = initial_twitter_user()
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

    for ronda in range(number_of_evaluation_N):
        for person in twitter_users:
            followers = obtain_followers(person)
            twitts = obtain_twitters(followers)
            re_twitts = obtain_re_twitts(followers)


def obtain_re_twitts(followers):
    pass


def obtain_twitters(followers):
    pass


def obtain_followers(person):
    pass


def initial_twitter_user():
    """
    This function return a list, with number of user created
    the users, are represented by a incremental int.
    :return:
    list[1,2,3,...,population_number_M]
    """
    return [i for i in range(population_number_M)]


def initial_following():
    pass


def random_twitt():
    pass


def random_re_twitt():
    pass


def find_hottest_twitt():
    pass


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
