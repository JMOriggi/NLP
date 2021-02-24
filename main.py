import Preprocessing as pre
from Scrape_Wikipedia import Scrape_Wikipedia
from Scrape_Twitter import Scrape_Twitter
import Language_Model
import nltk
from nltk.lm import KneserNeyInterpolated, MLE
from nltk.util import pad_sequence, everygrams, ngrams, flatten
from nltk.lm.preprocessing import padded_everygram_pipeline, pad_both_ends
import json
import itertools
        
## Get wikipedia raw text
with open("wikipedia_raw.txt", "r", encoding='utf-8') as f:
    wiki_raw_text = f.read() 
wiki_raw_text = wiki_raw_text[0:500]

## Get twitter raw text
with open('tweets_raw.json') as f:
    tweets_raw = json.load(f)
tweet_list = tweets_raw['statuses']
tweet_list = Scrape_Twitter.extract_tweet(tweet_list)
tweet_list = tweet_list[0:200]


## ----------------------------------------PROBLEM 4
## ------------- Q1
## Preprocess the data: segmenting, tokenizing, lower casing, and padding with begin-of-sentence and end-of-sentence (this last step done after)
# Train preprocessing: end structure is a list of sentences (that is again a list of tokens)
tweet_list_train = tweet_list[0:100]
train_data = [pre.tokenize_sent_word(tweet) for tweet in tweet_list_train]
train_data = [pre.clean_tokens(s, with_stop_word=True) for tweet in train_data for s in tweet]
train_data = pre.clean_sent(train_data, with_stop_word=True)
train_data = [pre.token_to_text(sent) for sent in train_data]

#Test preprocssing: end structure is a list of sentences (that is again a list of tokens)
tweet_list_test = tweet_list[100:150]
test_data = [pre.tokenize_sent_word(tweet) for tweet in tweet_list_test]
test_data = [pre.clean_tokens(s, with_stop_word=True) for tweet in test_data for s in tweet]
test_data = pre.clean_sent(test_data, with_stop_word=True)
test_data = [pre.token_to_text(sent) for sent in test_data]


## Train models: unigram, bigram, trigram
## train a trigram KneserNeyInterpolated language model (based on the 9,000 tweets)
## The models needs a list of sent-lemmas as data (tweet division not needed anymore)
model_uni = Language_Model.train_ngram(KneserNeyInterpolated(1), train_data, ngram=1)
model_bi = Language_Model.train_ngram(KneserNeyInterpolated(2), train_data, ngram=2)
model_tri = Language_Model.train_ngram(KneserNeyInterpolated(3), train_data, ngram=3)


## Test models: plot perplexity
## Important to use Kneser model for the 0 probability smoothing (otherzise perplexity goes to inf)
print("Perplexity on test_data model_uni = ", model_uni.perplexity(test_data)/len(tweet_list_test))
print("Perplexity on test_data model_bi = ", model_bi.perplexity(test_data)/len(tweet_list_test))
print("Perplexity on test_data model_tri =", model_tri.perplexity(test_data)/len(tweet_list_test))


## ------------- Q2
## Generate with models: 10 tweets for each model (total 30)
## If too long can use MLE instead of Kneser
print('\n-------Generate sentence')    
max_len = 20
for i in range(1):
    print("Generated from model_uni = ", Language_Model.generate_sent(model_uni, max_len))
    print("Generated from model_bi = ", Language_Model.generate_sent(model_bi, max_len))
    print("Generated from model_tri = ", Language_Model.generate_sent(model_tri, max_len))


## ------------- Q3 - WORK IN PROGRESS
## VADER model: compute the sentiment of each tweet in all your 10,000 tweets
## No preprocessing since everything maybe is usefull to the sentiment ????
tweet_tok = [pre.tokenize_sent(tweet) for tweet in tweet_list]
for tweet in tweet_tok:
    tweet_score = Language_Model.sentiment_tweet(tweet)
    print("Sentiment score =", tweet_score)





## ----------------------------------------PROBLEM 5
## ------------- Q1
## Sentence split, tokenize, lemmatize, lower case, remove stop words and plot top 20 words
wiki_tok = pre.tokenize_sent_word(wiki_raw_text)
wiki_tok = [pre.clean_tokens(s, with_stop_word=False) for s in wiki_tok]
wiki_tok = pre.clean_sent(wiki_tok, with_stop_word=False)
wiki_tok = [pre.lemmatize(s) for s in wiki_tok]

## Generate word cloud and plot frequency top 20
wiki_voc, wiki_voc_dup = pre.build_voc(wiki_tok, only_word_tokenized=False)
pre.word_frequency(wiki_voc_dup)
pre.plot_wordcloud(wiki_voc_dup)

## ------------- Q2
## Sentence split, tokenize, lemmatize, lower case, then remove stop words from your 1,000 test tweets
tweet_list_test = tweet_list[100:150]
tweet_tok = [pre.tokenize_sent_word(tweet) for tweet in tweet_list_test]
tweet_tok = [pre.clean_tokens(sent, with_stop_word=False) for tweet in tweet_tok for sent in tweet]
tweet_tok = pre.clean_sent(tweet_tok, with_stop_word=False)
tweet_tok = [pre.lemmatize(sent) for sent in tweet_tok]
twitter_voc_test, twitter_voc_test_dup = pre.build_voc(tweet_tok, only_word_tokenized=False)

### !!!!!!!!!!!!!!!!!!!! correct this: you have to use word types, and so not preprocess ?
## How many OOV in test tweet, normalized by the number of word types in your tweets (when using vocabulary constructed from Wikipedia above)
## word types: is the element in the vocabulary (words after tokenizing, lemmatizing, cleaning etc)
## word types in test tweets out of vocabulary / # word types in scraped wikipedia
oov_types_counter = 0
for el in twitter_voc_test:
    if el not in wiki_voc:
        oov_types_counter += 1
print('-- Number of OOV types: ',oov_types_counter/len(wiki_voc))

##How many tokens in your tweets are out of vocabulary, normalized by the number of tokens in your tweets
# token: is the single instance in the text (word without lemmatizing)
oov_tokens_counter = 0
for el in twitter_voc_test_dup:
    if el not in wiki_voc:
        oov_tokens_counter += 1
print('-- Number of OOV tokens: ',oov_tokens_counter/len(wiki_voc_dup))

## Compute the OOV-rate (tokens not words types) of your tweet test set when using your 9,000 train tweets, to construct your vocabulary/lexicon
tweet_train_tok = [pre.tokenize_sent_word(tweet) for tweet in tweet_list[0:10]]
tweet_train_tok = [pre.clean_tokens(s, with_stop_word=False) for tweet in tweet_train_tok for s in tweet]
tweet_test_tok = pre.clean_sent(tweet_train_tok, with_stop_word=False)
tweet_train_tok = [pre.lemmatize(sent) for sent in tweet_train_tok]
twitter_voc_train, twitter_voc_train_dup = pre.build_voc(tweet_train_tok, only_word_tokenized=False)
oov_tokens_counter = 0
for el in twitter_voc_test_dup:
    if el not in twitter_voc_train:
        oov_tokens_counter += 1
print('-- Number of OOV tokens: ',oov_tokens_counter/len(twitter_voc_train))

## ------------- Q3
## Sentence split, tokenize, and lower case the Wikipedia data you have collected, then get the first 9,000
wiki_tok = pre.tokenize_sent_word(wiki_raw_text)
wiki_tok = [pre.clean_tokens(s, with_stop_word=True) for s in wiki_tok]
wiki_tok = pre.clean_sent(wiki_tok, with_stop_word=True)
wiki_tok = [' '.join(pre.token_to_text(s)) for s in wiki_tok] # group the token element, only sentence group maintained
wiki_sent_list = wiki_tok[0:500]

## train a trigram KneserNeyInterpolated language model (based on these 9,000 sentences wikipedia)
model_tri = Language_Model.train_ngram(KneserNeyInterpolated(3), wiki_sent_list, ngram=3)

## Average perplexity of the model on test Twitter sentences (the one that contains 1,000 tweets)
tweet_test_tok = [pre.tokenize_sent_word(tweet) for tweet in tweet_list[0:10]]
tweet_test_tok = [pre.clean_tokens(s, with_stop_word=True) for tweet in tweet_test_tok for s in tweet]
tweet_test_tok = pre.clean_sent(tweet_test_tok, with_stop_word=True)
test_data = [pre.token_to_text(sent) for sent in tweet_test_tok]

print("Perplexity(test) = ", model_tri.perplexity(test_data))











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

'''tweet_tok = [pre.tokenize_sent_word(tweet) for tweet in tweet_list]
tweet_tok = [list(pre.clean_tokens(sent, with_stop_word=True) for sent in tweet) for tweet in tweet_tok]
tweet_tok = [pre.clean_sent(tweet, with_stop_word=True) for tweet in tweet_tok]
tweet_tok = [list(pre.token_to_text(sent) for sent in tweet) for tweet in tweet_tok]

train_data = list(itertools.chain.from_iterable(tweet_tok[0:100])) # flatten tweet dimension train data
test_data = list(itertools.chain.from_iterable(tweet_tok[100:150])) # flatten tweet dimension train data
'''




