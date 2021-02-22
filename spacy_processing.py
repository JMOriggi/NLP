## Spacy: very good for complex sentence split, tokenization, lemmatization.
## Convert the text to a spacy document, and I can access a lot of built-in functions
## The spacy boundaries stops after the lemmatization because it trasform to string the token object (can access like a string using token.text)

import re
from collections import Counter
import spacy
nlp = spacy.load('en_core_web_sm')

def check_token(t):
    ## Skip all the things I don't want
    if t.is_stop or t.is_punct or '\n' in t.text or t.text.strip() == '' or re.match('^[0-9]*$', t.text):
        return True
    return False

def spacy_processing(raw_text):
    
    ## Transform string text in spacy text
    doc = nlp(raw_text)
    ## Sentence splitting
    sent_list = list(doc.sents)
    #print(sent_list)
    ## Tokenize sentences
    sent_list_token = [list(t for t in s) for s in sent_list]
    #print(sent_list_token)
    ## Clean tokens: no stop word, no punctuation (only used for sentence splitting), no new line char, no numbers
    sent_list_token = [list(t for t in s if not check_token(t)) for s in sent_list_token if not (len(s) == 1 and check_token(s[0]))]
    ## Lemmatize: the lemma is a string (not like token that is an object)
    sent_list_token_lemma = [list(t.lemma_.lower().strip() for t in s) for s in sent_list_token]
    
    ## Frequency
    print('\nVocabulary frequency')
    frequencies = Counter(l for s in sent_list_token_lemma for l in s)
    for word, frequency in frequencies.most_common(20):
        print(word,'---', frequency)
    
    ## Vocabulary: with and without duplicates
    voc_dup = [t for s in sent_list_token_lemma for t in s]
    voc = list(dict.fromkeys(voc_dup)) # remove duplicates
    voc_txt = ' '.join(voc)
    voc_dup_txt = ' '.join(voc_dup)
    #print(voc)
    
    return voc, voc_dup, voc_txt, voc_dup_txt
    
  
if __name__ == "__main__":
    
    text = """pandemic have shed light 🙄 on various social and economic issues, including student debt, digital learning, food insecurity, and homelessness, as well as access to childcare, health care, housing, internet, and disability services., The impact has been more severe for disadvantaged children and their families., 
    , The pandemic has had many impacts on global health beyond those caused by the COVID-19 disease itself., It has led to a reduction in hospital visits for other reasons., There have been 38 per cent fewer hospital visits for heart attack symptoms in the United States and 40 per cent fewer in Spain., 
    , In several countries there has 👎🏽 been a marked reduction of 🙄 spread of sexually transmitted infections, including HIV"""
    
    spacy_processing(text) 
    
    
    
    
    
    
    

