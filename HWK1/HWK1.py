from itertools import combinations
import operator

import requests
from bs4 import BeautifulSoup

URL = "https://icanhazwordz.appspot.com/"

ROUNDS = 10

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


def get_string():
    '''
        - Request to a website and get 16 letters from a game board
    return:
        letters - a string of 16 characters given
    '''
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    ids = soup.select('tr > td')
    divs = [i.find('div') for i in ids]
    letters = [letter.text.lower() for letter in divs if letter]

    seeds = soup.find('input', {'name': 'Seed'}).get('value')
    print(seeds)
    return letters


if __name__ == '__main__':

    # Load dictionary words
    words = build_dict()

    while ROUNDS:
        # Load strings
        letters = get_string()
        letters.sort()
        print(letters)

        # Find 2^n - 1 - n - (n choose 2) possibilities
        # Will not consider combination of one and two letters since minimum length of letters in dictionary words are at least 3.
        comb = [''.join(p) for i in range(3, len(letters) + 1) for p in combinations(letters, i)]

        possibles = []
        for w in comb:
            if w in words.keys():
                possibles.append(words[w])

        if possibles:
            max_len = len(max(possibles, key=len))
            scores = {}
            # Get the best choice for this round
            for best in possibles:
                scores[best] = (sum([POINTS[i] for i in best]) + 1)**2
            # print(scores)
            print("Best word is: ", max(scores.items(), key=operator.itemgetter(1)))

        else:
            print('NO WORDS!!')
        ROUNDS -= 1
    print('DONE!')
