import re

from app.config import config

dictionary_file = config.get_data('dictionary_file')


def get_words():
    with open(dictionary_file, 'r') as file:
        words = file.read().split('\n')

    return words


def split_title(text):
    splitters = ['&', ',', '_', '/', '|', '-', '.', '+']

    for splitter in splitters:
        text = text.replace(splitter, ' ')

    return text.split(' ')


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


def remove_duplicate(text):
    return ' '.join(unique_list(text.strip().lower().split()))


def generate_words_from_title(text, query):
    regex = re.compile('[^a-zA-Z0-9]')
    words = []

    for word in split_title(text):
        word = regex.sub('', word)
        sentence = word

        if query not in sentence.strip().lower():
            sentence = f'{query} {sentence.strip()}'

        sentence = remove_duplicate(sentence)

        if sentence in words or sentence == query:
            continue

        for character in get_words():
            if f'{sentence.strip().lower()} {character}'.strip().lower() in words:
                continue

            words.append(f'{sentence.strip().lower()} {character}')

        words.append(sentence)

    return words
