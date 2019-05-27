
from itertools import combinations
import operator


def build_dict():
    '''
        - Load Dictionary words
    return:
        words - a list of loaded words
    '''
    file = 'words.txt'

    f = open(file, "r")

    words = [word.strip().lower() for word in f.readlines()]

    words = {''.join(sorted(word)): word for word in words}
    return words


if __name__ == '__main__':
    rounds = 0
    prompt = "Type letters: "

    # Load dictionary words
    words = build_dict()

    # print(list(words.keys())[:10])
    # print(list(words.values())[:10])

    # Points
    three_p = {k: 3 for k in ['j', 'k', 'q', 'x', 'z']}
    two_p = {k: 2 for k in ['c', 'f', 'h', 'l', 'm', 'p', 'v', 'w', 'y']}
    one_p = {k: 1 for k in ['a', 'b', 'd', 'e', 'g', 'i', 'n', 'o', 'r', 's', 't', 'u']}
    points = {**three_p, **two_p, **one_p}

    while rounds < 10:
        # given letters from the board
        letters = input(prompt)
        letters = letters.split()
        # avg O(nlogn), worst O(n^2)
        letters.sort()
        print(letters)

        # Find 2^n - 1 - n - (n choose 2) possibilities
        # Will not consider combination of one and two letters since minimum length of letters in dictionary words are at least 3.
        # 65399 possibilities for 16 characters
        comb = [''.join(p) for i in range(3, len(letters) + 1) for p in combinations(letters, i)]
        # print(len(comb))
        # print(comb)

        possibles = []
        for i, w in reversed(list(enumerate(comb))):
            try:
                possibles.append(words[w])
            except:
                continue

        if possibles:
            possibles = set(possibles)
            max_len = len(max(possibles, key=len))
            best_possibles = [p for p in possibles if len(p) == max_len or any(c in three_p.keys() for c in p) or any(c in two_p.keys() for c in p)]

            # print(best_possibles)

            scores = {}
            # Get best choice for this round
            for best in best_possibles:
                scores[best] = (sum([points[i] for i in best]) + 1)**2
            # print(scores)
            print("Best word is: ", max(scores.items(), key=operator.itemgetter(1)))

        else:
            print('NO WORDS!!')
        rounds += 1
    print('DONE!')
