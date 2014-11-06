import random
from collections import defaultdict

word_to_cluster = dict()
cluster_to_word = defaultdict(set)
word_frequencies = defaultdict(int)

with open('50mpaths2', 'r') as f:
    for line in f:
        cluster, word, frequency = line.split('\t')
        word_to_cluster[word] = cluster
        cluster_to_word[cluster].add(word)
        word_frequencies[word] = int(frequency)
        
def get_another_word_in_cluster(word):
    if word in word_to_cluster:
        return random.choice(list(cluster_to_word[word_to_cluster[word]]))
    else:
        return word
