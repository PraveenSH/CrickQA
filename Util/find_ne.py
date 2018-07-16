import nltk
from nltk.tree import Tree

def get_ne_chunks(text):
#    text = text.lower()
    locations = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
        if type(chunk) == Tree:
            print(chunk)
            if chunk.label() == 'GPE':
                ne = " ".join([token for token, pos in chunk.leaves()])
                print('hello', ne)
                locations.append(ne)
    return locations

get_ne_chunks("Number of runs for new zealand")
