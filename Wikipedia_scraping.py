# Libraries
# requests: get an html page
# bs4: go through the page to get information (a parser)
#   select: can use queries
#   findall: must chain different conditions
# nltk: 3.5 version

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs

class Scrape_Wiki():
    def __init__(self, url): 
        self.base = 'https://en.wikipedia.org'
        self.url = url
        self.html = self.get_html(self.base, self.url)
        self.soup = bs(self.html, 'html.parser') # lxml
        
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
            text = r.text # raw string response
            #json = r.json() # if response not in jason format returns error   
            return text
    
    
    def get_links(self):
        a_list = self.soup.select("p > a")
        href_list = [el['href'] for el in a_list] #list comprehension
        return href_list
    
    
    def get_text(self):
        title = self.soup.select("#firstHeading")[0].text
        p_list = self.soup.select("p")
        '''
        intro = '\n'.join([ p.text for p in p_list[0:5]])
        print (intro)
        '''
        return p_list


if __name__ == "__main__":
    
    url = '/wiki/COVID-19_pandemic'
    scrape = Scrape_Wiki(url)
    href_list = scrape.get_links()
    print(href_list[0])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

