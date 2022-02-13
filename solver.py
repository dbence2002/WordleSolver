from copy import copy, deepcopy
import random, math

class WordleState:

    def __init__(self, wordlist):
        
        self.wordlist = wordlist
        self.inside = []
        self.excluded = []
        self.wrong_chars = []
        self.right_chars = []

    def is_matching(self, word: str):

        for char, ind in self.wrong_chars:
            if word[ind] == char:
                return False

        for char, ind in self.right_chars:
            if word[ind] != char:
                return False

        for char, maxcnt in self.excluded:
            if word.count(char) > maxcnt:
                return False

        for char in self.inside:
            if char in word:
                index = word.index(char)
                word = word[:index] + word[index + 1:]
            else:
                return False

        return True

    def print_matching(self):
        print('\n [!] Matching')
        print('\n'.join(map(lambda item: f'  => match {item[0]} => {item[1]}', enumerate(self.wordlist))))

    def adjust(self, word, resp):

        inside_copy = copy(self.inside)
        resp_copy = copy(resp)

        for ind, (char, res) in enumerate(zip(word, resp_copy)):
            if res == 2:
                self.right_chars.append((char, ind))
            else:
                self.wrong_chars.append((char, ind))
            if res == 0:
                self.excluded.append((char, len(list(filter(lambda item: item[0] == char and item[1] != 0, zip(word, resp_copy))))))
                continue
            if char in inside_copy:
                index = inside_copy.index(char)
                inside_copy = inside_copy[:index] + inside_copy[index + 1:]
            else:
                self.inside.append(char)

        self.wordlist = list(filter(lambda word: self.is_matching(word), self.wordlist))

def generate_responses():

    responses = []

    for mask in range(0, 3 ** 5):
        resp = []
        while mask > 0:
            resp.append(mask % 3)
            mask //= 3
        responses.append(resp)

    return responses

responses = generate_responses()

def calc_entropy(state: WordleState, word: str) -> float:

    global responses
    result = 0.0

    for resp in responses:

        state_copy = deepcopy(state)
        state_copy.adjust(word, resp)
        freq = len(state_copy.wordlist) / len(state.wordlist)

        if len(state_copy.wordlist) > 0:
            result += freq * math.log(freq)

    print(f'  {word} -> {result}')
    return -result

def find_optimum(state):

    wordlist = list(map(lambda arg: arg.strip(), open('final_words').readlines()))

    if state.wordlist == wordlist:
        return "crane"

    if state.wordlist == []:
        return "?????"

    if len(state.wordlist) == 1:
        return state.wordlist[0]

    random_list = [wordlist[random.randint(0, len(wordlist) - 1)] for _ in range(8)]
    random_list = [state.wordlist[random.randint(0, len(state.wordlist) - 1)] for _ in range(8)] + random_list

    return max([(calc_entropy(state, word), word) for word in random_list])[1]

def adjust_color(color, guess, response):

    if color == None:
        color = dict((chr(ord('A') + char), 'gray') for char in range(0, 26))

    for i in range(5):
        if response[i] == 1 and color[guess[i].upper()] == 'gray':
            color[guess[i].upper()] = 'yellow'
        elif response[i] == 2:
            color[guess[i].upper()] = 'green'

    return color