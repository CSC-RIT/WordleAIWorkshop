from collections import Counter, defaultdict
from math import log2, inf
from tqdm import tqdm
import random

def load_allowed_words():
    """
    Load a list of words from the allowed_words text file

    return - the list of allowed words (words that are valid guesses)
    """

    words = []

    with open('allowed_words.txt') as f:
        for word in f:
            words.append(word.strip())
    
    return words


def load_possible_words():
    """
    Load a list of words from the possible_words text file

    return - the list of possible words (words that the answer could actually be)
    """

    words = []

    with open('possible_words.txt') as f:
        for word in f:
            words.append(word.strip())
    
    return words


def get_pattern(guess_word, secret_word):
    """
    Given guess_word and a secret_word, returns the pattern if guess_word were to be checked against secret_word
    Patterns consist of B (black), Y (yellow), or G (green)

    guess_word - string representing the guess
    secret_word - string representing the answer

    return - a pattern representing the result of the guess against the secret
    """
    pattern = [''] * 5

    guess_counts = defaultdict(int)
    secret_counts = Counter(secret_word)

    for i, (guess_letter, secret_letter) in enumerate(zip(guess_word, secret_word)):
        if guess_letter == secret_letter:
            pattern[i] = 'G'
            guess_counts[guess_letter] += 1
            continue

    for i, (guess_letter, secret_letter) in enumerate(zip(guess_word, secret_word)):
        if pattern[i] == 'G':
            continue

        if guess_counts[guess_letter] < secret_counts.get(guess_letter, 0):
            pattern[i] = 'Y'
            guess_counts[guess_letter] += 1
        else:
            pattern[i] = 'B'
    
    return ''.join(pattern)


def get_pattern_counts(guess_word, secret_words):
    """
    Counts the number of words that form each pattern, returns the answer as a dict/map

    guess_word - string representing the guess
    secret_words - list of strings of valid secret words left

    return - a dict of pattern -> count, where pattern is a guess result and count is
    the number of words that result in the pattern when guess_word is guessed
    """

    patterns = defaultdict(int)

    for secret_word in secret_words:
        pattern = get_pattern(guess_word, secret_word)
        patterns[pattern] += 1
    
    return patterns


def calculate_entropy(guess_word, secret_words):
    """
    Calculates the entropy of guess_word with remaining secret_words

    guess_word - string representing the guess
    secret_words - list of strings of valid secret words left

    return - the total entropy of the guess_word
    """

    n = len(secret_words)
    
    patterns = get_pattern_counts(guess_word, secret_words)

    entropy = 0

    for count in patterns.values():
        probability = count / n
        entropy += probability * log2(1 / probability)
    
    return entropy


def get_best_guess(words):
    """
    Calculates the word with the highest entropy out of the list words

    words - list of strings of valid words left

    return - the word representing the best guess
    """

    best_entropy = -inf
    best_word = None

    for guess_word in tqdm(words):
        entropy = calculate_entropy(guess_word, words)

        if entropy > best_entropy:
            best_entropy = entropy
            best_word = guess_word
    
    return best_word


def get_words_with_pattern(guess_word, words, pattern):
    """
    Finds all secret words that result in pattern when guess_word is guessed

    guess_word - a string of the word being guessed
    words - a list of valid remaining words
    pattern - the pattern guess_word results in when guessed against the secret word

    return - a list of words that result in pattern when guess_word is guessed
    """

    possible = []

    for secret_word in words:
        if get_pattern(guess_word, secret_word) == pattern:
            possible.append(secret_word)
    
    return possible


def main():
    words = load_possible_words()

    # loop until we get the answer
    while True:

        # 1. get the best guess
        best_guess = get_best_guess(words)

        print(f'best guess: {best_guess}')

        # 2. play the guess on Wordle; then give the program the pattern
        pattern = input('pattern received:\n> ')

        # 3. get the list of remaining valid words
        words = get_words_with_pattern(best_guess, words, pattern)


if __name__ == '__main__':
    main()