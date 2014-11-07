# -------------
#  FILE PATHS
# -------------

# this is the path to the 50mpaths2 file from the CMU TweetNLP project, 
# available at http://www.ark.cs.cmu.edu/TweetNLP/clusters/50mpaths2
PATH_TO_CLUSTER_FILE = '50mpaths2'  # stored in my local directory

# -----------
#  SETTINGS
# -----------

# settings relevant for process_clusters.py

# ignore URLs, hashtags, Twitter handles, 
# and words with mixed alphanumeric such as '3omf',
# and words with non-alphanumeric content? 
# (beware: this also excludes hyphenated words)

IGNORE_URLS = True
IGNORE_HASHTAGS = True
IGNORE_TWITTER_HANDLES = True
IGNORE_MIXED_ALPHANUMERIC = True
IGNORE_NON_ALPHANUMERIC = True
# SELECT_PROPORTIONAL_TO_FREQUENCY (not implemented)

# settings relevant for process_text.py

# how to replace words
REPLACE_DIALOGUE = True
START_QUOTE = "``"
END_QUOTE   = "''"
REPLACE_PROSE = False

# probability of replacing a word (less for greater readability)
REPLACE_WITH_PROBABILITY = 0.5

# I'm using hyperrefs represent names or anything else I want to protect 
# from replacement - insert these yourself (use NLTK for named entity detection)

# NB!!! Hyperrefs <a href=...> and </a>
# must be together on on line
IGNORE_HYPERREFS = True  

# NB also that if you have lower case tags, you may need to 
# fix some of the replacements in process_pnp.py

# create a tooltip for each replaced word?
CREATE_TOOLTIP = True
