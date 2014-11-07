from __future__ import print_function
import sys
import re
import random
from nltk.tokenize.punkt import PunktWordTokenizer
from config import *

from process_clusters import get_another_word_in_cluster

tkn = PunktWordTokenizer()

if len(sys.argv) <= 1:
    sys.stderr.write('Please specify the file you want to Twitterize\n')
    sys.exit()


with open(sys.argv[1], 'r') as f:

    # hacky way of keeping track of whether we're in a quote or anchor tag
    # I assume it just toggles, no nesting
    in_open_quote = False
    in_open_anchor_tag = False
    
    previous_word_translated = False

    for line in f:
        line = line.replace('&#32;', ' ')\
                   .replace('>', '> ').replace('<', ' <')\
                   .replace(START_QUOTE, 'START_QUOTE ')\
                   .replace(END_QUOTE, ' END_QUOTE')\
                   .replace('.', ' .')

        new_words = list()

        for word in tkn.tokenize(line):
            if word.startswith('<A') or word.endswith('A>'):
                in_open_anchor_tag = not in_open_anchor_tag
            if word == 'START_QUOTE' or word == 'END_QUOTE':
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
            # try to make it so that we don't have long stretches of
            # untranslated words
            if previous_word_translated:
                # decrease probability of translating
                replace_prob = REPLACE_WITH_PROBABILITY * 0.5
            else:
                # increase probability of translating
                replace_prob = REPLACE_WITH_PROBABILITY * 1.5
            to_translate = to_translate & (random.random() < replace_prob)
            
            # now that we've computed whether to translate this word,
            # store the info for next time around
            previous_word_translated = to_translate

            # actually process the word
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

        # fixing some punctuation issues due to 
        # introduction of extra spaces
        new_sentence = new_sentence.replace(' .', '.')\
                                   .replace(' ,', ',').replace(' ;', ';')\
                                   .replace(' !', '!').replace(' ?', '?')\
                                   .replace('<em> ', '<em>')\
                                   .replace(' </em', '</em')\
                                   .replace('( ', '(').replace(' )', ')')\
                                   .replace('& amp', '&amp')

        # TODO: fix spaces around quotes. Would help if we had separate marking
        # of pre- and post-quotes.
        new_sentence = new_sentence.replace('START_QUOTE ', '"')\
                                   .replace(' END_QUOTE', '"')\
                                   .replace('<P> ', '<P>')\
                                   .replace(' </P>', '</P>')

        # clear extra spaces again
        new_sentence = re.sub(' +', ' ', new_sentence)

        print(new_sentence)
