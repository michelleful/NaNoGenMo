"""
Use SpaCy to part-of-speech tag P&P
"""

import spacy

# load SpaCy
nlp = spacy.load('en')

# POS-tag everything
with open('../2014/pnp/pnp_clean.txt') as f:
    pnp = f.read()

doc = nlp(pnp)
