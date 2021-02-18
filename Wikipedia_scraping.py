# Libraries
# requests: get an html page
# bs4: go through the page to get information (a parser)
#   select: can use queries
#   findall: must chain different conditions
# nltk: 3.5 version

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs
import re

class Scrape_Wiki_Page():
    def __init__(self, url): 
        self.base = 'https://en.wikipedia.org'
        self.url = url
        self.html = self.get_html(self.base, self.url)
        self.soup = bs(self.html, 'lxml') #  html.parser
        
    @staticmethod    
    def get_html(base, url): 
        complete_url = base + url
        try:
            r = requests.get(complete_url)
            r.raise_for_status() # detect code status and raise exception for some cases
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}') 
        else:
            print('Success!')
            r.encoding = 'utf-8' # Optional: requests infers this internally
            header = r.headers['content-type'] # Header gives usefull infos
            print(header+'\n')
            html = r.text # raw string response
            #json = r.json() # if response not in jason format returns error 
            return html
    
    def get_links(self):
        a_list = self.soup.select("div.mw-parser-output a") # with > a is the direct children
        href_list = [el['href'] for el in a_list if el.has_attr('href')] #list comprehension method; take only href attribute value
        wiki_link_list = [el for el in href_list if el.startswith('/wiki/') and '#' not in el and ':' not in el]
        print('Count of links found within the page: '+str(len(wiki_link_list)))
        return wiki_link_list
    
    
    def get_text(self):
        #title = self.soup.select("#firstHeading")[0].text
        p_list = self.soup.select("div.mw-parser-output p")
        print('Count of text element found within the page: '+str(len(p_list)))
        text = ''.join([ p.text for p in p_list])
        return text


if __name__ == "__main__":
    
    url = '/wiki/COVID-19_pandemic'
    scrape_page = Scrape_Wiki_Page(url)
    wiki_link_list = scrape_page.get_links()
    p_list = scrape_page.get_text()
    frame = p_list[-100:-1]
    frame = re.sub('\[(.*)\]', '', frame) # delete the braket for numering citations
    #print(frame)    


'''
^        # Match the start of the line
.*?      # Non-greedy match anything
\(       # Upto the first opening bracket (escaped)
[^\d]*   # Match anything not a digit (zero or more)
(\d+)    # Match a digit string (one or more)
[^\d]*   # Match anything not a digit (zero or more)
\)       # Match closing bracket
.*       # Match the rest of the line
$        # Match the end of the line

/\(([^)]+)\)/;
( : begin capturing group
[^)]+: match one or more non ) characters
) : end capturing group
    
re.sub('\[(.*)\]', '', frame) # \ è l'escape per dire che "[" è un carattere; () indica un grouppo di match ; .* qualsiasi cosa
    
'''

'''    
1. Sentence split, tokenize, lemmatize, lower case, then remove stop words from the text using the library
spacy. Then, construct a vocabulary of words in the text.
(a) What are the top 20 words in the vocabulary according to frequency? Are they from a specific
topic? Do they give you insights into what the text is all about?
(b) Using library such as wordcloud, generate the word cloud of the text to visualize the distribution of
words—include the word cloud image in your write up. Does the word cloud give you some insights into
what the text is all about?

2. Sentence split, tokenize, lemmatize, lower case, then remove stop words from your 1,000 test tweets
from Problem 4 using spacy.
(a) Compute how many word types in your tweets are out-of-vocabulary, normalized by the number of
word types in your tweets, when using vocabulary constructed from Wikipedia above.
(b) Compute how many tokens in your tweets are out of vocabulary, normalized by the number of
tokens in your tweets. This is the OOV-rate of your tweet test set.
(c) Compute the OOV-rate of your tweet test set when using your 9,000 train tweets from Problem 4
to construct your vocabulary/lexicon. Note that you have to do the same pre-processing on your tweet
train set (i.e., sentence split, tokenize, lemmatize, lower case, then remove stop words using spacy) before
constructing the vocabulary.
(d) What does the OOV-rate tell you about the domain of these two texts (Wikipedia vs. Twitter of
similar topic that is COVID-19)?

3. Sentence split, tokenize, and lower case the Wikipedia data you have collected, then get the first 9,000
sentences from the data—most of the sentences therefore will come from the first URL that you scrape:
https://en.wikipedia.org/wiki/COVID-19 pandemic. Then, train a trigram KneserNeyInterpolated language
model based on these 9,000 sentences (remember to pad with begin- and end-of-sentence symbols).
(a) Report the average perplexity of the model on your Twitter test sentences, the one that contains
1,000 tweets from Problem 4 (remember to pre-process the test set the same way you pre-process the
training data of your LM).
(b) Compare this perplexity to the one you obtain in Problem 4.1 for the trigram LM trained on tweets.
What does the perplexity difference tell you about the domain of these two texts (Wikipedia vs. Twitter of
similar topic that is COVID-19)?
'''  
    
    
    
    
    
    
    
    
    
    
    
    
    

