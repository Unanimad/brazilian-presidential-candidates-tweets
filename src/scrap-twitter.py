import csv

from utils import conn_api, add_profile, get_statuses_between_dates

start_at = '16082018'
end_at = '29102018'

targets = [
    'jairbolsonaro', 'Haddad_Fernando', 'alvarodias_', 'CaboDaciolo', 'cirogomes',
    'Eymaeloficial', 'geraldoalckmin', 'GuilhermeBoulos', 'meirelles', 'joaoamoedonovo',
    'joaogoulart54', 'MarinaSilva', 'verapstu', 'LulaOficial'
]

consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

api = conn_api(consumer_key, consumer_secret,
                    access_token_key, access_token_secret)

for target in targets:
    csv_file = open(f'../data/{target.lower()}.csv', 'w+',
                    newline='', encoding='utf-8')

    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"')

    csv_writer.writerow(['id', 'name', 'screen_name', 'location', 'url', 'description', 'protected', 'verified',
                         'followers_count', 'friends_count', 'favourites_count', 'statuses_count', 'created_at',
                         'profile_image_url'])

    add_profile(api, target, csv_writer)

    csv_file.close()

    csv_file = open(
        f'../data/tweets/{target.lower()}_election_tweets.csv', 'w+',
        newline='', encoding='utf-8'
    )

    writer = csv.writer(csv_file, delimiter=';', quotechar='"')
    writer.writerow(['id', 'created_at', 'text',
                     'retweet_count', 'favorite_count'])

    get_statuses_between_dates(api, target, start_at, end_at, writer)

    csv_file.close()
