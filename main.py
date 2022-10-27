# John Logiudice
# INF 308 - Fall 2022
# Assignment 11 - Case Study - Data Structures
# 13.1

# Make string library available
from string import *


# Instantiate a word and clean word of extra characters
class Word:

    def __init__(self, word=None):
        self.word = word

    # Use the string library to remove punctuation from ends of word
    def strip_punctuation(self, word=None):
        if word is None:
            return self.word.strip(punctuation)
        else:
            return word.strip(punctuation)

    # Use the string library to remove whitespace from ends of word
    def strip_whitespace(self, word=None):
        if word is None:
            return self.word.strip(whitespace)
        else:
            return word.strip(whitespace)

    # Check if a string is a word or number
    def discard_numbers(self, word=None):
        if word is None:
            word = self.word

        # Attempt to convert the string to a float
        try:
            number = float(word)
        # If there is an error, assume it's a word and return word
        except ValueError:
            return word
        # If there is no error, assume it's a number and return None
        else:
            return None

    # process all the cleaning methods and return word
    def clean_word(self, word=None):
        if word is None:
            word = self.word

        word = self.strip_whitespace(word)
        word = self.strip_punctuation(word)
        word = self.discard_numbers(word)

        return word


# Instantiate a line and extract individual words
class Line:

    def __init__(self, line=None):
        
        if line is None:
            self.line = ''
        else:
            self.line = line

        # Initialize empty word list
        self.words = []
        # Get word list every time a Line is instantiated
        self.get_words()

    def get_words(self):
        # Convert entire line to lower case
        line = self.line.lower()

        # Consider hyphens as a separator and use str.split() to create list of words
        self.words = line.replace('—', ' ').split()


class Ebook:

    def __init__(self, filename):
        self.filename = filename

        # Initialize empty word dictionary
        self.word_dict = {}

    def read_lines(self):
        # open the file for reading
        with open(self.filename, encoding="utf-8") as file:
            # Iterate over each line
            for line in file:
                new_line = Line(line)
                # Extract words from the line
                words = new_line.words
                # Iterate over each word
                for word in words:
                    new_word = Word(word)
                    # Use clean method to get each word
                    new_word = new_word.clean_word()
                    # ignore words that were returned as None
                    if new_word is not None:
                        print(new_word)


def main():
    ebook = Ebook("sample.txt")
    ebook.read_lines()


if __name__ == '__main__':
    main()
