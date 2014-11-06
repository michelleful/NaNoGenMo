from __future__ import print_function

from process_clusters import get_another_word_in_cluster

with open('pnp_chapter1.html', 'r') as f:
    for line in f:
        for word in line.split():
            print(get_another_word_in_cluster(word), end=" ")
