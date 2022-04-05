import urllib.request, urllib.parse, urllib.error
import ssl
import json

from hidden import get_key

class Email:
    '''Represent'''

    def __init__(self, sender, receiver, subject, body):
        '''Initialize an instance from sender's email, receiver email, 
        subject of mail message and its body.'''
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
    
    def send(self):
        '''Handles sending email to the user.'''
      
        return None


class NewsFeed:
    '''Represents multiple news titles and links as a single string.'''

    base_url = 'https://newsapi.org/v2/everything?'
    api_key = get_key()['key']

    def __init__(self, interest, language, from_date, to_date):
        '''Intialize an instance from interest, language in format as 'en' or 'ru' and 
        two dates in yyyy-mm-dd format in which interval news feed will be searched.'''
        self.interest = interest
        self.language = language
        self.from_date = from_date
        self.to_date = to_date
    
    def get_body(self):
        '''Returns latests news feeds as string.'''

        # Construct url and get json data from it 
        url = self._url_construct()
        data_json = self._get_json(url)

        # Go through each news article and save them in list 
        # as (title, url) tuple
        articles = data_json['articles']

        email_body = list()
        for article in articles:
            email_body.append((article['title'], article['url']))

        return email_body
    
    def _url_construct(self):
        '''Constructs url out of instance's data.'''

        url = f'{self.base_url}' \
            f'qInTitle={self.interest}&' \
            f'from={self.from_date}&' \
            f'to={self.to_date}&' \
            f'language={self.language}&' \
            f'apiKey={self.api_key}'
        
        return url

    def _get_json(self, url):
        '''Connects to the url, gets the data from it and transforms it into 
        json format.'''

        # Ignore SSL errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        html_data = urllib.request.urlopen(url, context=ctx)
        data = html_data.read().decode()
        data_json = json.loads(data)

        return data_json

        
class DBInfo:
    '''The class to handle extracting users' data.'''

    def __init__(self, path):
        '''Constructor with database's filepath string parameter.'''

        self.path = path

    def get_data(self):
        '''Returns users' names, emails and interests.'''

        names = None
        emails = None
        interests = None

        return (names, emails, interests)
