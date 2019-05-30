from itertools import combinations
import operator
from dotenv import load_dotenv
import os
from os.path import join, dirname
from selenium import webdriver

# ROUNDS = 10
GOAL_SCORE = 1800
URL = "https://icanhazwordz.appspot.com/"

# Loading values
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CHROME = os.environ.get("CHROME")
NICK_NAME = os.environ.get('NAME')
GITHUB_URL = os.environ.get('GITHUB')

# POINTS
THREE_P = {k: 3 for k in ['j', 'k', 'x', 'z']}
TWO_P = {k: 2 for k in ['c', 'f', 'h', 'q', 'l', 'm', 'p', 'v', 'w', 'y']}
ONE_P = {k: 1 for k in ['a', 'b', 'd', 'e', 'g', 'i', 'n', 'o', 'r', 's', 't', 'u']}
POINTS = {**THREE_P, **TWO_P, **ONE_P}


def build_dict():
    '''
        - Load Dictionary words
    return:
        words - a dict of valid words, mapping the 'sorted' form of a word to its original form
    '''
    file = 'words.txt'

    f = open(file, "r")

    # words are in all lower capitals
    words = [word.strip().lower() for word in f.readlines()]

    # .join(sorted(word)) reproduces a string with its characters in sorted order and stored as key of the dict
    words = {''.join(sorted(word)): word for word in words}
    return words


def main():
    # build dictionary
    words = build_dict()

    # Open the web browser and access to the web page
    global driver
    driver = webdriver.Chrome(CHROME)
    driver.get(URL)

    # Keep track of number of game played
    game_count = 1
    global GOAL_SCORE
    while True:
        ROUNDS = 10
        # Keep track of scores
        total_scores = 0
        while ROUNDS:
            # Load strings
            letters = driver.find_elements_by_css_selector('div.letter')
            letters = [letter.text.lower() for letter in letters]
            letters.sort()
            # print(letters)

            word, score = get_word(letters, words)

            if word:
                # click submit
                driver.find_element_by_id('MoveField').send_keys(word)
                driver.find_element_by_xpath("//input[@value='Submit']").click()
                total_scores += score
            else:
                # click PASS
                driver.find_element_by_xpath("//input[@value='PASS']").click()

            ROUNDS -= 1
            # break
        print(f'THIS IS {game_count}th GAME and score is {total_scores}')
        game_count += 1
        if total_scores < GOAL_SCORE:
            # Start new game
            driver.find_element_by_xpath("//a[@href='/']").click()
        else:
            # goal achieved
            driver.find_element_by_xpath("//input[@name='NickName']").send_keys(NICK_NAME)
            driver.find_element_by_xpath("//input[@name='URL']").send_keys(GITHUB_URL)
            (driver.find_elements_by_xpath('//*[@name="Agent"].onclick()')).click()

            break

    print('DONE!')


def get_word(letters, words):
    # Find 2^n - 1 - n - (n choose 2) possibilities
    # Will not consider combination of one and two letters since minimum length of letters in dictionary words are at least 3.
    comb = [''.join(p) for i in range(3, len(letters) + 1) for p in combinations(letters, i)]

    word = None
    score = None
    possibles = []
    for w in comb:
        if w in words.keys():
            possibles.append(words[w])

    if possibles:
        scores = {}
        # Get the best choice for this round
        for best in possibles:
            scores[best] = (sum([POINTS[i] for i in best]) + 1)**2
        # print(scores)

        word, score = max(scores.items(), key=operator.itemgetter(1))
        # print("Best word is: ", word, score)

    else:
        print('NO WORDS!!')

    return word, score


if __name__ == '__main__':
    main()
