import spacy_processing as sp
from Wikipedia_scraping import Scrape_Wiki_Page
from Twitter_scraping import Scrape_Twitter
import nltk
from nltk.lm import KneserNeyInterpolated
from nltk.util import pad_sequence, everygrams, ngrams, flatten
from nltk.lm.preprocessing import padded_everygram_pipeline, pad_both_ends
from functools import partial
from nltk.tokenize.treebank import TreebankWordDetokenizer
detokenize = TreebankWordDetokenizer().detokenize

        
        
## Get wikipedia raw text
f = open("wikipedia_text.txt", "r", encoding='utf-8')
wiki_raw_text = f.read() 
f.close()
wiki_raw_text = wiki_raw_text[0:10000]

## Get twitter raw text
f = open("twitter_train_text.txt", "r", encoding='utf-8')
twitter_raw_text = f.read() 
f.close()

## ----------------------------------------PROBLEM 5 - Q1
'''## Tokenize and lemmatize data (also compute frequency)
sent_list_token, _ = sp.spacy_tokenize(wiki_raw_text)
voc, voc_dup, voc_txt, voc_dup_txt = sp.spacy_lemmatize(sent_list_token)

## Generate word cloud 
sp.plot_wordcloud(voc_dup_txt)'''


## ----------------------------------------PROBLEM 5 - Q2
'''## Build vocabularies
## Wikipedia
print('WIKIPEDIA')
token_list_wiki, _ = sp.spacy_tokenize(wiki_raw_text, False)
voc_wiki, *_  = sp.spacy_lemmatize(token_list_wiki)
token_list_wiki = [t.text for s in token_list_wiki for t in s] # Organize list token wise instead of sentence wise
print('-- Number of Tokens: ',len(token_list_wiki))
print('-- Number of Word Types: ',len(voc_wiki))
# Twitter test
print('\nTWITTER')
token_list_twitter, _ = sp.spacy_tokenize(twitter_raw_text, False)
voc_twitter, *_ = sp.spacy_lemmatize(token_list_twitter)
token_list_twitter = [t.text for s in token_list_twitter for t in s] # Organize list token wise instead of sentence wise
print('-- Number of Tokens: ',len(token_list_twitter))
print('-- Number of Word Types: ',len(voc_twitter))

## Compute how many word types in tweets are OOV, normalized by the number of word types in your tweets (when using vocabulary constructed from Wikipedia above)
# word types: is the element in the vocabulary (words after tokenizing, lemmatizing, cleaning etc)
oov_types_counter = 0
for el in voc_twitter:
    if el not in voc_wiki:
        oov_types_counter += 1
print('-- Number of OOV types: ',oov_types_counter)

## Compute how many tokens in your tweets are out of vocabulary, normalized by the number of tokens in your tweets
# token: is the single instance in the text (word without lemmatizing)
oov_tokens_counter = 0
for el in token_list_twitter:
    if el not in voc_wiki:
        oov_tokens_counter += 1
print('-- Number of OOV tokens: ',oov_tokens_counter)

## Compute the OOV-rate of your tweet test set when using your 9,000 train tweets, to construct your vocabulary/lexicon

'''

## ----------------------------------------PROBLEM 5 - Q3
## Get first 9000 sentences from tokenized data
_, token_list = sp.spacy_tokenize(wiki_raw_text, True)
print(len(token_list))
token_list = token_list[0:9000]

## train a trigram KneserNeyInterpolated language model (based on these 9,000 sentences)
ngram = 3
train_data, padded_sents = padded_everygram_pipeline(ngram, token_list) # this function also add the eof at every block of token words (sentence)
'''for ngramlize_sent in train_data:
    print(list(ngramlize_sent))
print('#############')
print(list(padded_sents))'''

model = KneserNeyInterpolated(ngram)
model.fit(train_data, vocabulary_text=padded_sents) 

def generate_sent(model, num_words):
    """
    :param model: An ngram language model from `nltk.lm.model`.
    :param num_words: Max no. of words to generate.
    """
    content = []
    for token in model.generate(num_words):
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenize(content)
print('\n-------Generate sentence')    
print(generate_sent(model, 20))
## Average perplexity of the model on your Twitter test sentences (the one that contains 1,000 tweets)






'''
ngram=1
data = (everygrams(list(padding_fn(sent)), max_len=ngram) for sent in tokenized_text)
vocab = flatten(map(padding_fn, tokenized_text))
model = KneserNeyInterpolated(ngram)
model.fit(train_data, vocab)
if it doesn't work for unigram use MLE
padding_fn = partial(pad_both_ends, n=ngram)


ngram = 13
ad_both_ends = partial(pad_sequence, pad_left=True, left_pad_symbol="<s>", pad_right=True, right_pad_symbol="</s>",)
padding_fn = partial(pad_both_ends, n=ngram)
data = (everygrams(list(padding_fn(sent)), max_len = ngram) for sent in token_list)
vocab = flatten(map(padding_fn, token_list))
print(list(everygrams(list(padding_fn(token_list[0])), max_len = ngram)))
model = KneserNeyInterpolated(ngram)
model.fit(data, vocab)

'''




