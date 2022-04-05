class Email:

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

    def __init__(self, interest, language, from_date, to_date):
        '''Intialize an instance from interest, language in format as 'en' or 'ru' and 
        two dates in yyyy-mm-dd format in which interval news feed will be searched.'''
        self.interest = interest
        self.language = language
        self.from_date = from_date
        self.to_date = to_date
    
    def get(self):
        '''Returns latests news feeds.'''

        return None

        
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
