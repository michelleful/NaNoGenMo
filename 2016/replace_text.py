"""
Italicizes words that potentially have innuendo meanings and
also childishly replaces a few words with grawlixes for giggles.
"""
import random, re
from collections import Counter
from process_pnp import doc

# innuendo words that will just be italicised
innuendo = dict()
with open('suggestive1.txt', 'r') as f:
    innuendo = {line.strip():1 for line in f.readlines()}

# exclude words that are stopwords
with open('stopwords.txt', 'r') as f:
    stopwords = {line.strip():1 for line in f.readlines()}

frequencies = Counter()
with open('pnp_freq.csv') as f:
    for line in f:
        lemma, pos, freq = line.split('\t')
        if lemma in innuendo:
            frequencies[lemma] = int(freq)

# exclude innuendo words that are very common in P&P
innuendo = {w:1 for w in innuendo if w not in stopwords and
                                   w not in [w for w, f in frequencies.most_common()[:20]]}


# additionally turn some specific words into grawlixes
grawlixes = {
    ('dance', 'VERB'): None,
    ('visit', 'VERB'): None,
    ('marry', 'VERB'): None,
    ('wife', 'NOUN'): ('a', 'DET'),
    ('husband', 'NOUN'): ('a', 'DET'),
    ('ancle', 'NOUN'): ('his', 'DET')
}

def grawlix(length):
    chars = list('@#$%&*')
    random.shuffle(chars)
    if chars[0] == '*':  # avoid problems with italics in markdown
        chars = chars[1:] + ['*']
    chars = ''.join(chars)
    chars = chars * (int(length / len(chars)) + 1)
    return chars[:length]


suffixes = {
    'VB': '',
    'VBD': 'ed',
    'VBG': 'ing',
    'VBZ': 's',
    'VBP': '',
    'VBN': 'ed',
    'NN': '',
    'NNS': 's',
    'JJ': '',
    'JJR': 'er',
    'JJS': 'est',
    'RB': '',
    'RBR': 'er',
    'RBS': 'est'
}


string = ''
for token in doc:
    if token.pos_ in ['VERB', 'NOUN', 'ADJ', 'ADV'] and token.lemma_ in innuendo:
        string += re.sub(r'\b(.*)\b', r'*\1*', token.text_with_ws)
    elif (token.lemma_, token.pos_) in grawlixes:
        subordinate_word_pos = grawlixes[(token.lemma_, token.pos_)]
        if subordinate_word_pos is None or subordinate_word_pos in [(x.orth_, x.pos_) for x in token.children]:
            suffix = suffixes[token.tag_]
            num_asterisks = 4
            string += token.text_with_ws.replace(token.orth_, grawlix(num_asterisks) + suffix)
        else:
            string += token.text_with_ws            
    else:
        string += token.text_with_ws


with open('output1.md', 'w') as g:
    g.write('# Pride and Prejudice and Innuendo\n')
    g.write('### by Jane Austen and Python Script\n\n')
    g.write(string)
