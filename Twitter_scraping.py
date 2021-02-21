from twython import Twython, TwythonError
import random
import re
import nltk
from nltk.lm import KneserNeyInterpolated
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.util import pad_sequence, everygrams, ngrams
from nltk.corpus import stopwords
from nltk.lm.preprocessing import padded_everygram_pipeline, pad_both_ends
from nltk.tokenize.treebank import TreebankWordDetokenizer
detokenize = TreebankWordDetokenizer().detokenize
stop_words = set(stopwords.words('english'))
sentiment = SentimentIntensityAnalyzer()

class Scrape_Twitter():
    def __init__(self): 
        self.__accessToken = "1357334800638631936-ymkPwxrMGv9PxqXsEPcnGeLlPcc33h"
        self.__accessTokenSecret = "0qMFeEVcH8Qyuxdziny48AGM1RFnZv8RwChtfS9BQbZEt"
        self.__consumerKey = "kEyhZWZ04eg5ieI2Y7Edsxqsq"
        self.__consumerSecret = "5LSx0YCbYbr9VflGvht1rmYcTRThMJzmUXLUaNoTAQOXRAmGDo"
        self.__bearerToken = "AAAAAAAAAAAAAAAAAAAAAOiiMwEAAAAAQrCeINClNDG9zl4kMWqmpN%2BmRbw%3D7vUnEUXSJxoNeZR8gO94LJ6TCIP8nNKIvA69pLzqRP9coDqBXf"
        
        print("Obtaining OAuth 2 token\n\n")
        twitter = Twython(self.__consumerKey, self.__consumerSecret, oauth_version=2)
        ACCESS_TOKEN = twitter.obtain_access_token()
        self.twitter = Twython(self.__consumerKey, access_token=ACCESS_TOKEN)
        print("Access token granted\n")
   
    def search_word(self, word):
        ## Search with specific keyword
        result = self.twitter.search(q=word, count=200, lang='en', tweet_mode="extended")
        return result['statuses'] #return complete block
     
    def search_user(self, user):
        ## Returns all tweets by username
        try:
           user_timeline = self.twitter.get_user_timeline(screen_name=user, count=1)
        except TwythonError as e:
            print(e)
        for tweets in user_timeline:
            print(tweets['text'])
    
    @staticmethod
    def clean_tweet(tweet):
        # keep only the period "." to be able to sent tokenize
        tweet = tweet.encode('utf-8','ignore').decode("utf-8") # remove weird character
        tweet = re.sub('@[^\s]+', '', tweet) # delete username
        #tweet = re.sub(r'#([^\s]+)', r' \1', tweet) # replace hashtag with only the words
        tweet = re.sub(r'#([^\s]+)', ' ', tweet) # delete hashtag 
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet) # delete web address
        tweet = re.sub('[^A-Za-z0-9.!?\' ]+',' ', tweet) #Remove all characters which are not alphabets, numbers or whitespaces.
        tweet = re.sub("[\s]+"," ",tweet) # delete aditional white spaces
        tweet = tweet.lower()
        return tweet
    
    @staticmethod
    def clean_after(s):
        s = re.sub('\.{3}', '', s)
        s = s.replace('.', '')
        s = s.replace('?', '')
        s = s.replace('!', '')
        s = s.strip()
        return s
    
    @staticmethod
    def generate_sent(model, num_words, random_seed=42):
        """
        :param model: An ngram language model from `nltk.lm.model`.
        :param num_words: Max no. of words to generate.
        :param random_seed: Seed value for random.
        """
        content = []
        for token in model.generate(num_words, random_seed=random_seed):
            if token == '<s>':
                continue
            if token == '</s>':
                break
            content.append(token)
        return detokenize(content)
    
    @staticmethod
    def sentiment_tweet(tweet_sent_token):
        """
        :param tweet_sent_token: tweet tokenize by sentence
        """
        total_score = 0
        for sentence in tweet_sent_token:
            ss = sentiment.polarity_scores(sentence)
            total_score -= ss["neg"]
            total_score += ss["pos"]
        tweet_score = round(total_score,3)
        print(tweet_sent_token)
        print(tweet_score)
        return tweet_score
        

if __name__ == "__main__":
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
    print(scrape_twitter.generate_sent(model, 20, random_seed=7))
    
        
    '''# Join in one long string
    tweet_string = '\n'.join('<s>'+str(el)+'</s>' for el in tweet_list)
    #print(tweet_string)
    
    # File save
    save_file = open("sample.txt", "wt")
    n = save_file.write(tweet_string)
    save_file.close()'''
    
    
    
    
    
    
    
    