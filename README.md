NaNoGenMo
=========

My entry (entries?) to National Novel Generation Month 


## Twide and Twejudice (2014)

[Read the novel](https://cdn.rawgit.com/michelleful/NaNoGenMo/master/twide_and_twejudice.html)

### What the hell is this?

Pride and Prejudice with (almost) each word of the dialogue replaced
with another word in the same 
[hierarchical Twitter cluster](http://www.ark.cs.cmu.edu/TweetNLP/cluster_viewer.html), 
that is, with another word that is used in a similar context on Twitter
as computed by the CMU TweetNLP project.

### How to run:

1. Change the settings in `config.py` if you need to
2. Run `python twitterize.py filename.html`

The Python script was hacked together so it probably won't work on your own
text right out of the box.

### Acknowledgments

With apologies to Jane Austen and thanks to 
[Pemberley Manor](http://www.pemberley.com/janeinfo/pridprej.html#toc) 
for the supply of their e-text, as well as CMU for 
[TweetNLP](http://www.ark.cs.cmu.edu/TweetNLP/).

And thanks also to Lynne Cherny (@arnicas) for telling me about NaNoGenMo
and inspiring the idea.
