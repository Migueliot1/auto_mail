from db_hidden import get_db_name
import funct
import datetime

def dates_for_email():
    '''Returns tuple of two dates in ready-to-use state (today, yesterday)'''

    # Format for datetime
    date_format = '%Y-%m-%d'

    today = datetime.datetime.now().strftime(date_format)
    yesterday = today - datetime.timedelta(days=1).strftime(date_format)

    return (today, yesterday)


def make_letter_body(raw_data, interest):
    '''Constructs proper letter body ready to sent in email.'''

    # Adding a header to the letter and then adding first 5 news articles
    letter_body = f'Hey, see what\'s about {interest} today!\n\n'
    for i in range(5):
        letter_body += raw_data[i][0] + '\n' + raw_data[i][1] + '\n\n'
    
    letter_body += '--\nGood day to you!'

    return letter_body


# Grabbing the data from the SQLite file
db = funct.DataHandler(get_db_name())
data = db.get_data()

# Send emails to users
for user in data:
    # Get the news
    dates = dates_for_email()
    news_feed = funct.NewsFeed(interest=user[3].replace(' ', '-'),
                                language='en',
                                from_date=dates[0],
                                to_date=dates[1])
    
    raw_letter_body = news_feed.get_body() # Getting a big list of tuples (title of article, link to it)

    # Construct letter body
    letter_body = make_letter_body(raw_letter_body, user[3])
    
    # Preparing other values for Email class
    subject = f'Your {user[3]} news for today!'
    name = f'{user[0]} {user[1]}' 
    email_address = user[2]

    # Send the email
    email = funct.Email(name, email_address, subject, letter_body)
    email.send()
