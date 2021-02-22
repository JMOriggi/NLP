import spacy_processing as sp
from Wikipedia_scraping import Scrape_Wiki_Page
from Twitter_scraping import Scrape_Twitter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
def plot_cloud(wordcloud):
        plt.figure(figsize=(40, 30))
        plt.imshow(wordcloud) 
        plt.axis("off");
        
        
## ----------------------------------------WIKIPEDIA
## Read main page
url = '/wiki/COVID-19_pandemic'
scrape_page = Scrape_Wiki_Page(url)
wiki_link_list = scrape_page.get_links()
raw_text = scrape_page.get_text() 

## Get all links text
for url_sec in wiki_link_list:
    scrape_sec_page = Scrape_Wiki_Page(url_sec)
    raw_text = raw_text + '\n' + scrape_sec_page.get_text()
    del scrape_sec_page  

## Save file
f = open("wikipedia_text.txt", "wt")
n = f.write(raw_text)
f.close()
'''## Read file
f = open("wikipedia_text.txt", "r")
text = f.read()   
print(text) 
f.close()'''

'''
## Preprocess raw text
voc, voc_dup, voc_txt, voc_dup_txt = sp.spacy_processing(text[0:10000])

## Generate word cloud
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Pastel2', collocations=False).generate(voc_dup_txt)
plot_cloud(wordcloud)'''



## ----------------------------------------TWITTER
scrape_twitter = Scrape_Twitter()
res = scrape_twitter.search_word('covid')

# Extract only tweets
print('\n-------Unclean tweet')
tweet_list = [el['full_text'] if not el['full_text'].startswith('RT @') else el['retweeted_status']['full_text'] for el in res]
print(tweet_list[0])

# Clean tweets
print('\n-------Clean tweet')
for i in range(len(tweet_list)):
    tweet = tweet_list[i]
    clean_tweet = scrape_twitter.clean_tweet(tweet)
    tweet_list[i] = clean_tweet
print(tweet_list[0])


# File save
save_file = open("sample.txt", "wt")
n = save_file.write('\n'.join(str(el) for el in tweet_list))
save_file.close()

'''print('\n-------Tokenize Sentence in each tweet')
tweet_list_token = []
for i in range(len(tweet_list)):
    tweet = tweet_list[i]
    sent = nltk.sent_tokenize(tweet)
    sent = [scrape_twitter.clean_after(s) for s in sent] # now clean from last punctuation used for sentence segmentation
    tweet_list_token.append(sent)
print(tweet_list_token)

print('\n-------Tokenize word in each sentence and create bigram')
all_tgrams = []
for tweet in tweet_list_token:
    for sentence in tweet:
        w_t = word_tokenize(sentence)
        padded_bigrams = list(pad_both_ends(w_t, n=2))
        #grams = everygrams(padded_bigrams, max_len=3)
        grams = ngrams(padded_bigrams, 2)
        #grams = ngram(w_t, 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol="</s>")
        all_tgrams.extend(grams)
print(all_tgrams)'''

print('\n-------Tokenize word and sentences')
all_sent = []
all_sent_word = []
for tweet in tweet_list:
    sent = sent_tokenize(tweet)
    for s in sent:
        s = scrape_twitter.clean_after(s)
        all_sent.append(s)
        all_sent_word.append(word_tokenize(s))
print(all_sent[0])
print(all_sent_word[0])


print('\n-------Create vocabulary')
'''train, vocab = padded_everygram_pipeline(3, all_tgrams)
for ngramlize_sent in train:
    print(list(ngramlize_sent))
print(list(vocab))'''
# Preprocess the tokenized text for 3-grams language modelling
n = 3
train_data, padded_sents = padded_everygram_pipeline(n, all_sent_word) # this function also add the eof at every block of token words (sentence)
# By accessing train_data, we destroy the iterator and the data become unaccessible to the model
'''for ngramlize_sent in train_data:
    print(list(ngramlize_sent))
print('#############')
print(list(padded_sents))'''
 

print('\n-------Create Model')
#model = KneserNeyInterpolated()
from nltk.lm import MLE
model = MLE(3)
model.fit(train_data, vocabulary_text=padded_sents)
print(model.vocab)
'''model = KneserNeyInterpolated()
model.fit(train_data, vocabulary_text=padded_sents)
print(model.vocab)'''


print('\n-------Generate sentence')    
print(scrape_twitter.generate_sent(model, 50, random_seed=7))

    
# Join in one long string
#tweet_string = '\n'.join('<s>'+str(el)+'</s>' for el in tweet_list)
#print(tweet_string)
