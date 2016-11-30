"""
Find words in P&P that are also in Urban Dictionary
"""
import string, json, time
from glob import glob
import urbandict

# first get words in P&P
pnp_dict = dict()
with open('suggestive.txt') as f:
    for line in f:
        word = line.strip()
        pnp_dict[word] = 1

def is_term_in_pnp(term):
    # term may consist of multiple words
    words = term.split()
    if len(words) > 1:
        return False  # temp: only consider 1-word things
    for w in words:
        if w not in pnp_dict:
            return False
    return True


def seems_suggestive(defns):
    if 'sex' in defns[0]['def']:
        return True
    return False


# check what we've already done - may have to rerun script in case of timeout
done_words = dict()
with open('suggestive1.txt', 'r') as f:
    for word in f:
        done_words[word.strip()] = 1
with open('non_suggestive1.txt', 'r') as g:
    for word in g:
        done_words[word.strip()] = 1


path_to_urban_dictionary = '/home/michelle/Language_Resources/english/urban-dictionary-word-list/data/'
with open('suggestive1.txt', 'a') as g1:
    with open('non_suggestive1.txt', 'a') as g2:
        for letter in string.ascii_uppercase:
            with open(path_to_urban_dictionary + letter + '.data') as f:
                for term in f:
                    term = term.strip().lower()
                    if term in done_words:
                        continue
                    if is_term_in_pnp(term):
                        defns = urbandict.define(term)
                        if seems_suggestive(defns):
                            print(defns)
                            g1.write(term + '\n')
                            g1.flush()
                        else:
                            g2.write(term + '\n')
                            g2.flush()
                        time.sleep(1)
                    done_words[term] = 1
