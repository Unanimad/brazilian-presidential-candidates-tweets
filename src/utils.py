import time
import datetime
import twitter


def conn_api(consumer_key, consumer_secret, access_token_key, access_token_secret):
    """ Connect to Twitter API

    Returns:
        object: Connection
    """
    api = twitter.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret,
        sleep_on_rate_limit=True,
        tweet_mode='extended'
    )

    return api


def twitter_date(value):
    """Convert Twitter date to Datetime object

    Args:
        value (str): Twitter date

    Returns:
        datetime: Converted datetime object
    """
    split_date = value.split()
    del split_date[0], split_date[-2]
    value = ' '.join(split_date)

    return datetime.datetime.strptime(value, '%b %d %H:%M:%S %Y')


def get_statuses_between_dates(api, screen_name, start_at, end_at, writer):
    """ Get User Tweets between two dates

    Args:
        screen_name (str): The screen name, handle, or alias that
                            this user identifies themselves with.
        start_at (datetime): When the mining started
        end_at (datetime): When the mining ended
        save (bool): If True save status into database
        writer (object): Writer object

    Returns:
        Saved tweets
    """

    start_at = datetime.datetime.strptime(start_at, '%d%m%Y')
    end_at = datetime.datetime.strptime(end_at, '%d%m%Y')

    print(f"Fetching tweets from @{screen_name}!")

    tmp_statuses = api.GetUserTimeline(screen_name=screen_name)

    if len(tmp_statuses) > 0:
        for status in tmp_statuses:
            created_at = twitter_date(status.created_at)

            if created_at < end_at and created_at > start_at:
                add_status(status, screen_name, writer)

        last_status = 0

        while twitter_date(tmp_statuses[-1].created_at) > start_at:
            tmp_statuses = api.GetUserTimeline(
                screen_name=screen_name, max_id=tmp_statuses[-1].id)

            if last_status == tmp_statuses[-1].id:
                break

            last_status = tmp_statuses[-1].id

            for status in tmp_statuses:
                created_at = twitter_date(status.created_at)

                if created_at < end_at and created_at > start_at:
                    add_status(status, screen_name, writer)

    else:
        print('No tweets posted!')


def add_status(status, screen_name, writer):
    output = [status.id, twitter_date(
        status.created_at), status.full_text.replace("\n", "")]
    writer.writerow(output)


def add_profile(api, screen_name, writer):
    """ Get a Twitter User by screen name
    Args:
        screen_name (str): The screen name, handle, or alias that this
                            user identifies themselves with.
    Returns:
        User object
    """
    # api = conn_api()

    try:
        user = api.GetUser(screen_name=screen_name)
    except twitter.error.TwitterError as error:
        print(error.args)
    else:
        output = [
            user.id, user.name, user.screen_name, user.location, user.url, user.description, user.protected, user.verified,
            user.followers_count, user.friends_count, user.favourites_count, user.statuses_count, twitter_date(
                user.created_at),
            user.profile_image_url,
        ]

        writer.writerow(output)
