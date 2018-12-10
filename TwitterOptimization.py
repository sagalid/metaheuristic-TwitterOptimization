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
number_of_evaluation_N = 100
bernoulli_p = 0.5

users_of_twitter = [None]  # List of M twitter users.
followers = dict()  # Each user has F followers.
tweets_by_user = dict()  # Each user has a tweet and every tweet has: user [key], tweeter, fitness, factibility and Number of RT.
hottest_tweet_by_user = dict()  # Tweets with more RT. Could exist more than one, given equal number of RT.
seed = None


def run_mh(inputFile):
    initialize_mh(inputFile)
    for rund in range(number_of_evaluation_N):
        for person in users_of_twitter:
            user_followers = obtain_followers(person)
            tweets = obtain_twitters(user_followers)  # Get tweets and retweets
            best_tweet = obtain_best(tweets)
            worst_tweet = obtain_worst(tweets)
            perform_re_tweet(best_tweet)
            follow_author(person, best_tweet)
            unfollow_author(person, worst_tweet)
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
    else:
        print("\n")
        exit()
    if (verbose):
        print(colored("Rows:\t\t", 'yellow'), colored(pf.filas, 'blue'))
        print(colored("Columns:\t", 'yellow'), colored(pf.columnas, 'blue'), '\n')
        print(colored(pf.matriz_a, 'yellow'))
    if (verbose):
        print(colored('\nSeed Generation...', 'yellow'), end='')
    seed = random.randint(0, (population_number_M - 1))
    random.seed(seed)
    if (verbose):
        print(colored('OK\n', 'blue'))
    if (verbose):
        print(colored('Initial twitter user...', 'yellow'), end='')
    users_of_twitter = initial_twitter_user()
    if (verbose):
        print(colored('OK', 'blue'))
        # print(users_of_twitter)
    if (verbose):
        print(colored('\nInitial Following...', 'yellow'), end='')
    initial_following(users_of_twitter)
    if (verbose):
        print(colored('OK', 'blue'))
        # print(followers)
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


def follow_author(person, best_tweet):
    """

    :param best_tweet:
    :return:
    """
    global followers
    followers_by_user = followers[person]
    for user in best_tweet:
        follow_user = user

    tmp_fitness = None
    tmp_user = None
    for follow in followers_by_user:
        c_fitness = tweets_by_user[follow][1]
        if tmp_fitness is None:
            tmp_fitness = c_fitness
        elif tmp_fitness < c_fitness:
            tmp_fitness = c_fitness
            tmp_user = follow

    if follow_user not in followers_by_user:
        followers_by_user.append(follow_user)
        followers_by_user.remove(tmp_user)


def unfollow_author(person, worst_tweet):
    """
    worst_tweet = user [key], tweeter, fitness, factibility and Number of RT
    :param worst_tweet:
    :param user_followers:
    :return:
    """
    global followers
    followers_by_user = followers[person]
    for user in worst_tweet:
        unfollow_user = user

    for i in range(number_of_followers_F):
        random_user = random.randint(0, (population_number_M - 1))
        if (random_user != unfollow_user) and (random_user not in followers_by_user):
            break
    list_for_replace = []
    for user in followers_by_user:
        if user == unfollow_user:
            list_for_replace.append(random_user)
        else:
            list_for_replace.append(user)
    followers[person] = list_for_replace


def perform_re_tweet(best_tweet):
    """
    Retweet the best tweet in the followers 
    user [key], tweeter, fitness, factibility and Number of RT
    :param best_tweet:
    :return:
    """
    global tweets_by_user
    user_number = 0
    for user in best_tweet:
        user_number = user

    rt_number = tweets_by_user[user_number][3]
    rt_number += 1  # Retweet by increment in 1.
    tweets_by_user[user_number][3] = rt_number


def obtain_worst(tweets):
    """
    obtain worst tweet by fitness from followers.
    user [key], tweeter, fitness, factibility and Number of RT
    :param tweets:
    :return dictionary whit worst tweet, user[key], tweet, fitness and #RT:
    """
    max_fitness = None
    fitness_list = []
    for tweet in tweets:
        c_fitness = tweets[tweet][1]
        c_factibility = tweets[tweet][2]
        if c_factibility:
            fitness_list.append(c_fitness)
    max_fitness = max(fitness_list)
    worst_tweet = dict()
    for tweet in tweets:
        c_tweet = tweets[tweet][0]
        c_fitness = tweets[tweet][1]
        c_factibility = tweets[tweet][2]
        c_number_of_rt = tweets[tweet][3]
        if c_fitness == max_fitness:
            worst_tweet[tweet] = [c_tweet, c_fitness, c_factibility, c_number_of_rt]
    return worst_tweet


def obtain_best(tweets):
    """
    obtain the best tweet by fitness from followers.
    user [key], tweeter, fitness, factibility and Number of RT
    :param tweets:
    :return dictionary whit best tweet, user[key], tweet, fitness and #RT:
    """
    global hottest_tweet_by_user
    min_fitness = None
    fitness_list = []
    for tweet in tweets:
        current_fitness = tweets[tweet][1]
        factibility = tweets[tweet][2]
        if factibility:
            fitness_list.append(current_fitness)
    min_fitness = min(fitness_list)
    best_tweet = dict()
    for tweet in tweets:
        c_tweet = tweets[tweet][0]
        c_fitness = tweets[tweet][1]
        c_factibility = tweets[tweet][2]
        c_number_of_rt = tweets[tweet][3]
        if c_fitness == min_fitness:
            best_tweet[tweet] = [c_tweet, c_fitness, c_factibility, c_number_of_rt]
            for x in hottest_tweet_by_user:
                if hottest_tweet_by_user[x][1] > c_fitness:
                    hottest_tweet_by_user = None
                    hottest_tweet_by_user = dict()
                    hottest_tweet_by_user = best_tweet
    return best_tweet


def obtain_twitters(followers):
    """
    user [key], tweeter, fitness, factibility and Number of RT
    :param followers:
    :return:
    """
    tweets = dict()
    for person in followers:
        tweets[person] = [tweets_by_user[person][0],  # Tweeter
                          tweets_by_user[person][1],  # Fitness
                          tweets_by_user[person][2],  # Factibility
                          tweets_by_user[person][3]]  # RT Num
    return tweets


def obtain_followers(person):
    """
    This function return the followers of person P.
    :param person:
    :return list of followers:
    """
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
    """
    global followers
    for user in twitter_users:
        followers_list = []
        for i in range(number_of_followers_F):
            random_user = random.randint(0, (population_number_M - 1))
            if followers_list.__len__() == 0:
                followers_list.append(random_user)
            else:
                while random_user in followers_list:
                    random_user = random.randint(1, (population_number_M - 1))
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

    # print(tweets_by_user)


def random_re_twitt():
    global tweets_by_user
    for user in tweets_by_user.keys():
        followers_of_user = obtain_followers(user)
        random_follower = random.choice(followers_of_user)
        while (1):
            tweet_details = tweets_by_user[random_follower]
            if tweet_details[2]:
                break
            else:
                random_follower = random.choice(followers_of_user)
        tweet_details[3] += 1
        # print(tweets_by_user[user][3])


def find_hottest_by_fitness():
    """
    This function search and return de best tweet (Binary Vector) for fitness and RT's.
    :return Tweet binary vector:
    """
    pass


def find_hottest_twitt():
    """
    This function iterate over every twitter in tweets_by_user,
    in look for the one with best fitness.
    :return:
    dictionary whit this estructure
    [user], tweet,  fitness, feasible, # RT.
    """
    global hottest_tweet_by_user
    best_fitness = None
    for user in tweets_by_user:
        c_fitness = tweets_by_user[user][1]
        c_factibility = tweets_by_user[user][2]
        if best_fitness is None and c_factibility:
            best_fitness = c_fitness
        elif c_fitness < best_fitness and c_factibility:
            best_fitness = c_fitness
    temp_hottest = dict()
    for user in tweets_by_user:
        c_tweet = tweets_by_user[user][0]
        c_fitness = tweets_by_user[user][1]
        c_factibility = tweets_by_user[user][2]
        c_number_of_rt = tweets_by_user[user][3]
        if c_fitness == best_fitness:
            temp_hottest[user] = [c_tweet, c_fitness, c_factibility, c_number_of_rt]
    hottest_tweet_by_user = None
    hottest_tweet_by_user = dict()
    hottest_tweet_by_user = temp_hottest

def empty_tweet():
    return [None] * pf.columnas


def main(argv):
    global verbose
    inputfile = ''
    try:
        if len(argv) == 0:
            help()
            exit()
        opts, args = getopt.getopt(argv, "h:i:v", ["ifile="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if not opt:
            help()
            break
        if opt == '-h':
            help()
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in ('-v'):
            verbose = True

    run_mh(inputfile)


def help():
    print("")
    print("For run Twitter Optimization," + colored(" you must", "red") + " set de benchmark file with:")
    print("")
    print("\t" + colored('TwitterOptimization.py -i <scp41.txt>', 'green'))
    print("\n\n")


main(sys.argv[1:])
