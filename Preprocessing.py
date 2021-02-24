## Spacy: very good for complex sentence split, tokenization, lemmatization.
## Convert the text to a spacy document, and I can access a lot of built-in functions
## The spacy boundaries stops after the lemmatization because it trasform to string the token object (can access like a string using token.text)
## You need to tokenize the words only to use a ngram or to normalize words

import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 100000


def tokenize_sent(raw_data):
    """
    :param raw_data: raw text data
    :return tok_sent: text tokenized by sentence, list of sentences
    """ 
    doc = nlp(raw_data) 
    tok_sent = list(doc.sents)
    return tok_sent

def tokenize_word(raw_data): 
    """
    :param raw_data: raw text data
    :return tok_sent: text tokenized by word, list of words
    """ 
    doc = nlp(raw_data) 
    tok_word = list(doc.words)
    return tok_word

def tokenize_sent_word(raw_data): 
    """
    :param raw_data: raw text data
    :return tok_sent: text tokenized by sentence and word, list of sentences and words
    """ 
    doc = nlp(raw_data) 
    tok_sent = list(doc.sents)
    tok_sent_word = [list(tok for tok in s) for s in tok_sent]
    return tok_sent_word

def check_token(token, with_stop_word):
    """
    :param token: one token element of spacy module
    :param with_stop_word: flag to consider or not stop word in the text analysed
    :return boolean: True skip the word, False consider it
    """ 
    #or not re.match('^(?=.*[a-zA-z]).+', t.text)
    if (token.is_stop and not with_stop_word) or token.is_punct or token.text.strip() == '\n' or token.text.strip() == '' or 'https://' in token.text or 'http://' in token.text:
        #print(t.text)
        return True
    return False
def clean_tokens(tok_list, with_stop_word=True):
    """
    :param tok_list: list of token elements of spacy module
    :return tok_clean_list: same list filtered word wise
    """ 
    ## No stop word, no punctuation (only used for sentence splitting), no new line char, no only numbers token
    tok_clean_list = [tok for tok in tok_list if not check_token(tok, with_stop_word)] # token wise clean
    return tok_clean_list
def clean_sent(tok_sent_list, with_stop_word=True):
    """
    :param tok_sent_list: list of sentences containing another list token elements of spacy module
    :return tok_sent_list: same list filtered sentence wise
    """ 
    tok_sent_list = [s for s in tok_sent_list if not (len(s) == 1 and check_token(s[0], with_stop_word) or len(s) == 0)] # sentence wise clean
    return tok_sent_list
def clean(tok_sent_list, with_stop_word=True):
    """
    :param tok_list: list of sentences containing another list token elements of spacy module
    :return tok_clean_list: same list filtered word and sentence wise
    """ 
    ## No stop word, no punctuation (only used for sentence splitting), no new line char, no only numbers token
    tok_clean_list = [tok for sent in tok_sent_list for tok in sent if not check_token(tok, with_stop_word)] # token wise clean
    tok_sent_list = [s for s in tok_sent_list if not (len(s) == 1 and check_token(s[0], with_stop_word) or len(s) == 0)] # sentence wise clean
    return tok_clean_list


def token_to_text(tok_list):
    """
    :param tok_list: list of token elements of spacy module
    :return text_list: list of words
    """ 
    text_list = [tok.text.lower().strip() for tok in tok_list] # convert token to text
    return text_list


def lemmatize(tok_list):
    """
    :param tok_list: list of token elements of spacy module
    :return lemma_list: list of lemmas (basically a string of normalized tokens)
    """ 
    ## tok_sent_word: tokenized by sentence and by words
    ## Lemmatize: the lemma is a string (not like token that is an object)
    lemma_list = [tok.lemma_.lower().strip() for tok in tok_list]
    return lemma_list
    
def build_voc(preprocessed_text_list, only_word_tokenized=False):
    """
    :param preprocessed_text_list: list of sentences containing list of string words or when only_word_tokenized = True simple list of words preprocessed
    :return voc, voc_dup: list of words with and without duplicates
    """ 
    ## Vocabulary: the voc is not organized per sentence and comes in 2 versions with and without duplicates
    ## A vocabulary is a simple list of the raw text tokenized and lemmatized.
    if only_word_tokenized:
        voc_dup = preprocessed_text_list
    else:
        voc_dup = [tok for s in preprocessed_text_list for tok in s]
    voc = list(dict.fromkeys(voc_dup)) # remove duplicates
    return voc, voc_dup
    
def word_frequency(voc_dup):
    """
    :param voc: list of words with duplicates
    :plot frequency: word frequency
    """ 
    ## Frequency
    print('\nVocabulary words frequency')
    frequencies = Counter(w for w in voc_dup)
    for word, frequency in frequencies.most_common(20):
        print(word,'---', frequency)
    

def plot_wordcloud(voc):
    """
    :param voc: raw text data
    :plot wordcloud: wordcloud
    """ 
    voc = ' '.join(voc) #trasform voc list in txt
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Pastel2', collocations=False).generate(voc)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud) 
    plt.axis("off");


    
  
if __name__ == "__main__":
    
    text = """pandemic have shed 2.2m 2.2m 2.2m light 🙄 on. various 2000 2000 2000 200FM 200FM social and economic issues, including student debt, digital learning, food insecurity, and homelessness, as well as access to childcare, health care, housing, internet, and disability services., The impact has been more severe for disadvantaged children and their families., 
    , The pandemic has had many impacts on global COVID-19 COVID-19 health beyond those caused by the COVID-19 disease itself., It has led to a reduction in hospital visits for other reasons., There have been 38 per cent fewer hospital visits for heart attack symptoms in the United States and 40 per cent fewer in Spain., 
    , In several countries there has 👎🏽 been a marked £ £ £ reduction of 🙄 spread of sexually transmitted infections, including HIV"""
    
    tok_sent_word = tokenize_sent_word(text) 
    tok_sent_word = [clean_tokens(s, with_stop_word=False) for s in tok_sent_word]
    lem_sent_word = [lemmatize(s) for s in tok_sent_word]
    voc, voc_dup = build_voc(lem_sent_word, only_word_tokenized=False)
    word_frequency(voc_dup)
    plot_wordcloud(voc_dup)
    
    
    
    

