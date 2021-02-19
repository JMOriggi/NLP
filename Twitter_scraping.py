from twython import Twython, TwythonError

class Scrape_Tweet():
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
        user_timeline = self.twitter.search(q=word, count=2)
        for tweets in user_timeline['statuses']:
            print(tweets['text'] +"\n")
     
    def search_user(self, user):
        ## Returns all tweets by username
        try:
           user_timeline = self.twitter.get_user_timeline(screen_name=user, count=2)
        except TwythonError as e:
            print(e)
        for tweets in user_timeline:
            print(tweets['text'])

if __name__ == "__main__":
    scrape_twitter = Scrape_Tweet()
    wiki_link_list = scrape_twitter.search_user('@BarackObama')
    wiki_link_list = scrape_twitter.search_word('covid')