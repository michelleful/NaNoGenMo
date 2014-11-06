from __future__ import print_function
import re
import random
from nltk.tokenize.punkt import PunktWordTokenizer
from config import *

from process_clusters import get_another_word_in_cluster

tkn = PunktWordTokenizer()

with open('pnp_chapter1.html', 'r') as f:

    # hacky way of keeping track of whether we're in a quote or anchor tag
    # I assume it just toggles, no nesting
    in_open_quote = False
    in_open_anchor_tag = False

    for line in f:
        line = line.replace('&#32;', ' ')\
                   .replace('>', '> ').replace('<', ' <')\
                   .replace(START_QUOTE, '" ').replace(END_QUOTE, ' "')\
                   .replace('.', ' .')

        new_words = list()

        for word in tkn.tokenize(line):
            if word.startswith('<A') or word.endswith('A>'):
                in_open_anchor_tag = not in_open_anchor_tag
            if word == '"':
                in_open_quote = not in_open_quote

            # should we be translating this word?
            to_translate = True
            if in_open_quote and not REPLACE_DIALOGUE:
                to_translate = False
            if not in_open_quote and not REPLACE_PROSE:
                to_translate = False
            if in_open_anchor_tag and IGNORE_HYPERREFS:
                to_translate = False
            if not word.isalnum():  # don't translate punctuation
                to_translate = False

            # choose whether we'll translate this word - flip a biased coin
            to_translate = to_translate & (random.random() <
                                           REPLACE_WITH_PROBABILITY)

            if to_translate:
                if CREATE_TOOLTIP:
                    new_words.append('<span title="' +
                                     word + '">' +
                                     get_another_word_in_cluster(word) +
                                     '</span>')
                else:
                    new_words.append(get_another_word_in_cluster(word))
            else:
                new_words.append(word)

        # join words with spaces into a new line
        new_sentence = ' '.join(new_words)

        # remove links
        new_sentence = re.sub('<A .*?\>', '', new_sentence)
        new_sentence = re.sub('</A>', '', new_sentence)

        # clear extra spaces
        new_sentence = re.sub(' +', ' ', new_sentence)

        # fixing some punctuation issues due to the introduction of extra spaces
        new_sentence = new_sentence.replace(' .', '.')\
                                   .replace(' ,', ',').replace(' ;', ';')\
                                   .replace(' !', '!').replace(' ?', '?')\
                                   .replace('<em> ', '<em>')\
                                   .replace(' </em', '</em')\
                                   .replace(' </A>', '</A>')\

        # TODO: fix spaces around quotes. Would help if we had separate marking
        # of pre- and post-quotes. Current fix below is inadequate.
        new_sentence = re.sub(' " ', '"', new_sentence)

        # clear extra spaces again
        new_sentence = re.sub(' +', ' ', new_sentence)

        print(new_sentence)

