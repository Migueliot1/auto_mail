import urllib.request, urllib.parse, urllib.error
import ssl
import json
import yagmail
import sqlite3

from hidden import get_key, get_email

class Email:
    '''Represents email address which sends emails to other addresses.'''

    email_data = get_email()

    def __init__(self, receiver_name ,receiver_email, subject, body):
        '''Initialize an instance from receiver's name, receiver's email, 
        subject of mail message and its body.'''
        self.receiver_name = receiver_name
        self.receiver_email = receiver_email
        self.subject = subject
        self.body = body
    
    def send(self):
        '''Handles sending email to the user.'''
        email = yagmail.SMTP(user=self.email_data[0], password=self.email_data[1])
        email.send(to=self.receiver_email,
                    subject=self.subject,
                    contents=self.body)


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

        
class DataHandler:
    '''The class to handle extracting users' data from SQLite file.'''

    def __init__(self, path):
        '''Constructor with SQLite database's filepath string parameter.'''

        self.path = path

    def get_data(self):
        '''Returns list of tuples (name, surname, email, interest).'''

        # Open SQLite file
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        # Select needed data
        cursor.execute('''
        SELECT Emails.name, Emails.surname, Emails.email, Interests.interest
        FROM Emails JOIN Interests
        ON Emails.interest_id = Interests.id
        ''')

        # Place needed data into list and return it
        users = list()
        for row in cursor:
            users.append(row)

        return users
