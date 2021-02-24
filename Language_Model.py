import nltk
from nltk.lm import KneserNeyInterpolated
from nltk.util import pad_sequence, everygrams, ngrams, flatten
from nltk.lm.preprocessing import padded_everygram_pipeline, pad_both_ends
from nltk.tokenize.treebank import TreebankWordDetokenizer
detokenize = TreebankWordDetokenizer().detokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()


def train_ngram(model, train_data, ngram):
    """
    :param model: usually KneserNey or MLE
    :param train_data: train data padded 
    :param ngram: ngram to consider
    :return model: the model trained
    """
    train_data, padded_sents = padded_everygram_pipeline(ngram, train_data) # this function also add the eof at every block of token words (sentence)
    '''## Decomment to visualize data , but will not run the model as it's a lazy iterator
        for ngramlize_sent in train_data:
        print(list(ngramlize_sent))
    print('#############')
    print(list(padded_sents))'''
    model.fit(train_data, vocabulary_text=padded_sents)
    return model

def sentiment_tweet(sent_list):
    """
    :param sent_list: list of sentences to evaluate
    :return sent_score: global sentiment score
    """
    total_score = 0
    for sent in sent_list:
        ss = sentiment.polarity_scores(str(sent))
        total_score -= ss["neg"]
        total_score += ss["pos"]
    sent_score = round(total_score,3)
    #print(sent_list)
    #print(sent_score)
    return sent_score

def generate_sent(model, num_words):
    """
    :param model: An ngram language model from `nltk.lm.model`.
    :param num_words: Max no. of words to generate.
    :return detokenize(content): clean text of the sentence generated
    """
    content = []
    for token in model.generate(num_words):
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenize(content)

    
    
    
    
    