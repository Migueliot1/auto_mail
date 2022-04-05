import funct

# Grabbing the data from the SQLite file
db = funct.DataHandler('emails_receivers.db')
data = db.get_data()

# Send emails to users
for user in data:
    # Get the news
    news_feed = funct.NewsFeed(interest=user[3].replace(' ', '-'),
                                language='en',
                                from_date='2022-04-05',
                                to_date='2022-04-06')
    
    raw_letter_body = news_feed.get_body() # Getting a big list of tuples (title of article, link to it)

    # Adding a header to the letter and then adding first 5 news articles
    letter_body = f'Hey, see what\'s about {user[3]} today!\n\n'
    for i in range(5):
        letter_body += raw_letter_body[i][0] + '\n' + raw_letter_body[i][1] + '\n\n'
    
    # Preparing values for Email class
    letter_body += '--\nGood day to you!'
    subject = f'Your {user[3]} news for today!'
    name = f'{user[0]} {user[1]}' 
    email_address = user[2]

    # Send the email
    email = funct.Email(name, email_address, subject, letter_body)
    email.send()
