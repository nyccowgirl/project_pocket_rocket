
"""Generate Markov text from text files."""

from random import choice


def open_and_read_files(file_path_list):
    """Take file path as list; read through each file; and return text as string.
    Increment each file and turns the files' contents as one string of text.
    """

    long_text = ""

    for f in file_path_list:
        with open(f) as text_file:
            long_text += text_file.read()

    return long_text


def make_chains(text_string, n_grams):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:
        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:
        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:
        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()  # creates list from text_string
    words.append(None)  # add none at end of list to indicate stopping point

    #Looping through up and including last n-gram
    for i in range(len(words)-n_grams):
        extract_words = words[i:i+n_grams]
        state = tuple(extract_words)  # creates tuple of n-grams
        transition = words[i + n_grams]  # creates value of word following n-gram
        chains.setdefault(state, []).append(transition)

    return chains


def pull_cap(chains):
    """ Generates start key until first word is capitalized. """
    while True:
        start_key = choice(chains.keys())

        if start_key[0].title() == start_key[0]:
            return start_key


def end_punc(transition):
    """Determines if value ends in (. ! ?)"""

    punctuation = set(['.', '!', '?'])

    if transition[-1] in punctuation:
        return True
    else:
        return False


def make_title_descr(chains, word_limit):
    """Return title or description from chains."""

    words = []
    key = choice(chains.keys())
    words.extend(key)

    while True:
        combo = chains[key]
        transition = choice(combo)

        if (transition is None):
            break
        elif (end_punc(transition) is True):
            words.append(transition)
            break
        elif len(words) >= word_limit:
            break

        words.append(transition)
        extract_words = list(key[1:])
        extract_words.append(transition)
        key = tuple(extract_words)

    chain = " ".join(words)

    return chain


def make_text(chains, min_char, max_char):
    """Return text from chains."""

    words = []
    start_key = pull_cap(chains)
    words.extend(start_key)
    new_key = start_key

    while True:
        combo = chains[new_key]
        transition = choice(combo)

        if (transition is None):
            break

        words.append(transition)
        chain = ' '.join(words)

        if (len(chain) >= min_char) and (len(chain) <= max_char) and (end_punc(transition) is True):
            break

        extract_words = list(new_key[1:])
        extract_words.append(transition)
        new_key = tuple(extract_words)

    return chain


excerpts = ['data/markov/trump.txt', 'data/markov/nin_deltaofvenus.txt',
            'data/markov/rice_claimingofsleepingbeauty.txt', 'data/markov/jfk_inaugural.txt',
            'data/markov/mlk_ihaveadream.txt', 'data/markov/miller_tropicofcancer']
MARKOV_CHAIN = make_chains(open_and_read_files(excerpts), 2)
