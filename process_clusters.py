import random
import re
from collections import defaultdict

from config import *

word_to_cluster = dict()
cluster_to_word = defaultdict(set)
word_frequencies = defaultdict(int)

with open(PATH_TO_CLUSTER_FILE, 'r') as f:
    for line in f:
        cluster, word, frequency = line.split('\t')

        # figure out whether to ignore word based on settings in config.py
        if IGNORE_URLS and word.startswith('<URL-'):
            continue
        if IGNORE_HASHTAGS and word.startswith('#'):
            continue
        if IGNORE_TWITTER_HANDLES and word.startswith('@'):
            continue
        if (IGNORE_MIXED_ALPHANUMERIC and re.search('[0-9]', word) and
                                          re.search('[A-z]', word)):
            continue
        if IGNORE_NON_ALPHANUMERIC and not word.isalnum():
            continue

        word_to_cluster[word] = cluster
        cluster_to_word[cluster].add(word)
        word_frequencies[word] = int(frequency)
        
def get_another_word_in_cluster(word):
    if word in word_to_cluster:
        return random.choice(list(cluster_to_word[word_to_cluster[word]]))
    else:
        return word
