# John Logiudice
# INF 308 - Fall 2022
# Assignment 11 - Case Study - Data Structures
# 13.4

# Make string library available
from string import *
import random

FILE_NAME = 'MobyDick.txt'
WORD_LIST = 'CROSSWD.TXT'


# Instantiate a word and clean word of extra characters
class Word:

    def __init__(self, word=None):
        self.word = word

    # Use the string library to remove punctuation from ends of word
    def strip_punctuation(self, word=None):
        # Use built-in punctuation list plus extra characters I noticed in the
        # eBook file
        punct = punctuation + "‘’”“£"
        if word is None:
            return self.word.strip(punct)
        else:
            return word.strip(punct)

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

        if word[0].isdigit():
            return None
        else:
            return word

    # process all the cleaning methods and return word
    def clean_word(self, word=None):
        if word is None:
            word = self.word

        word = self.strip_whitespace(word)
        word = self.strip_punctuation(word)
        # Discard empty strings after strip()
        if len(word) == 0:
            return None

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

    # Extract single words from a line
    def get_words(self):
        # Convert entire line to lower case
        line = self.line.lower()

        # Consider hyphens as a separator and use str.split() to create list of words
        self.words = line.replace('—', ' ').replace('-', ' ').split()


# Load a word list. Identify words in another list that are not in word list
class WordList:

    def __init__(self, filename):
        self.filename = filename
        self.word_list = []

    # Load words from word list file into list
    def load_words(self, filename=None):
        if filename is None:
            filename = self.filename

        with open(filename) as file:
            # clear the word list before loading words
            self.word_list.clear()
            # Iterate over each word in the file
            for word in file:
                # Append each word to the word list
                self.word_list.append(word.rstrip())

    # Compare another word list to the word list, return words not found
    def not_in_list(self, source_list, word_list=None):
        if word_list is None:
            word_list = self.word_list

        # Make copies of each list so original lists are not changed
        # Sort both lists for search efficiency
        source_copy = source_list.copy()
        word_copy = word_list.copy()

        # Iterate of word list
        for i in range(len(word_copy)):
            try:
                # Attempt to remove word from the source list
                source_copy.remove(word_copy[i])
            except ValueError:
                pass

        # Return source list that had known words removed
        return source_copy


# Instantiate a book, open the file and do analysis
class Ebook:

    def __init__(self, filename):
        self.filename = filename
        self.word_count = None
        self.unique_count = None

        # Initialize empty word dictionary
        self.word_dict = {}

    # Open a book text file and analyse the contents
    def read_lines(self):
        # Initialize counter
        count = 0
        # Initialize in header variable
        in_header_footer = True
        # open the file for reading
        with open(self.filename, encoding="utf-8") as file:
            # Iterate over each line
            for line in file:
                new_line = Line(line)
                # If in header or footer, do not process lines
                if not in_header_footer:
                    # Extract words from the line
                    words = new_line.words
                    # Iterate over each word
                    for word in words:
                        new_word = Word(word)
                        # Use clean method to get each word
                        new_word = new_word.clean_word()
                        # ignore words that were returned as None
                        if new_word is not None and len(new_word) > 0:
                            # Add word to dictionary and update the count
                            self.word_dict[new_word] = self.word_dict.get(new_word, 0) + 1

                            # Increment total count
                            count += 1

                # Check for header and footer start and end
                if line.startswith("*** START"):
                    in_header_footer = False
                elif line.startswith("*** END"):
                    in_header_footer = True

        # Only update the count variables if counts were done
        if count > 0:
            self.word_count = count
            self.unique_count = len(self.word_dict)

    # Get the top_num most used words in the word list
    def get_common_words(self, top_num, word_dict=None):
        if word_dict is None:
            word_dict = self.word_dict

        try:
            top_num = int(top_num)
        except ValueError as e:
            print(f"Exception: {e} \ntop_num must be an integer")
            return None

        # Convert the dictionary to a list of tuples (word, word_count)
        new_list = list(word_dict.items())
        # Sort the list by the second item (word_count) in the tuple
        new_list.sort(reverse=True, key=lambda t: t[1])
        # Return first top_num item from the list
        return new_list[:top_num]

    # Get list of unique words from the dictionary
    def get_all_words(self):
        # Return just the key names which represents each unique word
        return list(self.word_dict.keys())

    # Chose a random word from the eBook in proportion to its frequency
    def choose_from_hist(self):
        # Verify first that there is a word count
        if self.word_count is None:
            return None

        # Get a random number from 0 to word_count
        random_number = random.randrange(self.word_count)

        # Initialize a counter
        count = 0

        # Iterate over each word in the dictionary
        for word in self.word_dict:
            # Loop the number of times each word appears
            for i in range(self.word_dict[word]):
                # When the counter reaches the random number
                if count == random_number:
                    # Return the word
                    return word
                count += 1

        return None



# Print out a list of words with index numbers
def print_list(words):
    for i in range(len(words)):
        print(f"{i+1}. {words[i]}")


def main():
    # Initialize an eBook object
    ebook = Ebook(FILE_NAME)
    # Load the eBook into memory
    ebook.read_lines()

    # Display analysis
    print()
    print(f"The total number of words in the book: {ebook.word_count}")
    print(f"The number of different words in the book: {ebook.unique_count}")
    print()

    # Set the number of most common words to get
    get_top_num = 20
    print(f"The top {get_top_num} most used words in the book are:")
    # Use list comprehension to pull just the words from the common words list
    print_list([t[0] for t in ebook.get_common_words(get_top_num)])
    print()

    random_word = ebook.choose_from_hist()
    print("This word was chosen randomly from the book:")
    print(random_word)
    print(f"It was used {ebook.word_dict[random_word]} times.")
    print()

    # Initialize a word list object
    word_list = WordList(WORD_LIST)
    # Load the know word list file into memory
    word_list.load_words()
    # Display all words that are in the eBook, but not in the word list
    print("List of eBook words not found in the known word list:")
    print("(this may take a few seconds)")
    print(word_list.not_in_list(ebook.get_all_words()))




# Run the main function
if __name__ == '__main__':
    main()
