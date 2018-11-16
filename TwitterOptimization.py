from termcolor import colored
import sys
import getopt
import ParsingFile as pf
import random
from scipy.stats import bernoulli
import numpy as np
verbose = False
population_number_M = 30
number_of_followers_F = 10
number_of_evaluation_N = 10000
bernoulli_p = 0.5
users_of_twitter = [None]
hottest_tweet = [None]
followers = dict()
tweets_by_user = dict()
seed = None

def run_mh(inputFile):
    global hottest_tweet
    initialize_mh(inputFile)
    for ronda in range(number_of_evaluation_N):
        for person in users_of_twitter:
            followers = obtain_followers(person)
            tweets = obtain_twitters(followers)
            re_tweets = obtain_re_twitts(followers)
            best_tweet = obtain_best(tweets, re_tweets)
            worst_tweet = obtain_worst(tweets, re_tweets)
            perform_re_tweet(best_tweet)
            # TODO uncoment
            #if (fitness(best_tweet) < fitness(hottest_tweet)):
            #    hottest_tweet = best_tweet
            follow_author(best_tweet)
            unfollow_author(worst_tweet)
            # TODO se debe programar esta parte.
            ##if is own tweet hasnt been retweeted for several rounds then
            ####Tweet a new tweet B and replace hottest tweet with B if B is more valuable...

def initialize_mh(inputFile):
    global users_of_twitter
    global seed
    if (verbose):
        print(colored('\n\nBegin of Twitter Optmization\n', 'blue'))
    if (verbose):
        print(colored('Parsing file...', 'yellow'), end='')
    if (pf.parsear(inputFile) and verbose):
        print(colored('OK\n', 'blue'))
    if (verbose):
        print(colored("Rows:\t\t", 'yellow'), colored(pf.filas, 'blue'))
        print(colored("Columns:\t", 'yellow'), colored(pf.columnas, 'blue'), '\n')
        print(colored(pf.matriz_a, 'yellow'))
    if (verbose):
        print(colored('\nSeed Generation...', 'yellow'), end='')
    seed = random.randint(0, (population_number_M-1))
    random.seed(seed)
    if (verbose):
        print(colored('OK\n', 'blue'))
    if (verbose):
        print(colored('Initial twitter user...', 'yellow'), end='')
    users_of_twitter = initial_twitter_user()
    if (verbose):
        print(colored('OK', 'blue'))
        #print(users_of_twitter)
    if (verbose):
        print(colored('\nInitial Following...', 'yellow'), end='')
    initial_following(users_of_twitter)
    if (verbose):
        print(colored('OK', 'blue'))
        #print(followers)
    if (verbose):
        print(colored('\nRandom Tweett...', 'yellow'), end='')
    random_twitt()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nRandom Re-Tweett...', 'yellow'), end='')
    random_re_twitt()
    if (verbose):
        print(colored('OK', 'blue'))
    if (verbose):
        print(colored('\nFind hottest Tweett...', 'yellow'), end='')
    find_hottest_twitt()
    if (verbose):
        print(colored('OK', 'blue'))


def fitness(tweet):
    if tweet is not None:
        cost_vector = pf.getVectorCosto()
        activated_vector = [a * b for a, b in zip(tweet, cost_vector)]
        return sum(activated_vector)
    else:
        return 0


def feasible(tweet):
    a_transposed = np.transpose(pf.getMatrizA())
    set_of_restriction = np.dot(tweet, a_transposed)
    comply = True

    for restriction in set_of_restriction:
        if restriction == 0:
            comply = False

    if comply:
        return True
    else:
        return False


def follow_author(best_tweet):
    pass


def unfollow_author(worst_tweet):
    pass


def perform_re_tweet(best_tweet):
    pass


def obtain_worst(tweets, re_tweets):
    pass


def obtain_best(tweets, re_tweets):
    pass


def obtain_re_twitts(followers):
    pass


def obtain_twitters(followers):
    pass


def obtain_followers(person):
    return followers[person]


def initial_twitter_user():
    """
    This function return a list, with number of user created
    the users, are represented by a incremental int.
    :return:
    list[0,1,2,3,..., population_number-1]
    """
    return [i for i in range(population_number_M)]


def initial_following(twitter_users):
    """
    This function implement a random follower for a twitter user.
    in stochastic process F user are selected and added to followers of twitter_user
    :param twitter_users:
    :return: None
    """
    global followers
    for user in twitter_users:
        followers_list = []
        for i in range(number_of_followers_F):
            random_user = random.randint(0, (population_number_M-1))
            if followers_list.__len__() == 0:
                followers_list.append(random_user)
            else:
                while random_user in followers_list:
                    random_user = random.randint(1, (population_number_M-1))
                followers_list.append(random_user)
        followers[user] = followers_list


def random_twitt():
    """
    This function randomly generated tweet for every user in twitter.
    Populating a global dictionary where every user get:
        -Tweet
        -fitness of this tweet
        -If the tweet is feasible
        -Numbers of Re-Tweet, obviously in this case te value is 0.
    :return: None
    """
    global tweets_by_user
    users = [i for i in range(population_number_M)]
    for user in users:
        random_tweet = list(bernoulli.rvs(bernoulli_p, size=pf.getCantidadColumnas()))
        fitness_of_tweet = fitness(random_tweet)
        is_feasible = feasible(random_tweet)
        # in tweets by user, append 4 principal elements: tweet, fitness, feasibility and number of re-tweet.
        tweets_by_user[user] = [random_tweet, fitness_of_tweet, is_feasible, 0]


def random_re_twitt():
    print("\nWORK ON =============")
    global tweets_by_user
    for user in tweets_by_user.keys():
        followers_of_user = obtain_followers(user)
        random_follower = random.choice(followers_of_user)
        while(1):
            tweet_details = tweets_by_user[random_follower]
            if tweet_details[2]:
                break
        print(tweet_details)

    print("END==================")


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
