import re
import urllib
from time import sleep
import praw
import wikipedia
import botinfo

class LocationMeta(object):
    def __init__(self, title, desc, lon, lat, link):
        self.title = title
        self.desc = desc
        self.lon = lon
        self.lat = lat
        self.link = link

    def __str__(self):
        return f'Location name: {self.name}'

user = botinfo.username
mention = f'u/{user}'
# Cities
CITY_REGEX = '.+$'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'
SPACE_REGEX = '\s+'

WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
MAPS_URL = 'https://www.google.com/maps/search/{}'
BOOKING_URL = 'https://www.booking.com/searchresults.sl.html?ss={}'
PT_URL = 'https://www.pinterest.com/search/pins/?q={}'

FOOTER = '\n\n---\n\n^(I am a bot and this was an automated message.' \
         'below.)\n\n^(Author: [u/'+user+'](https://www.reddit.com/user/'+user+')'

def get_map_link(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return MAPS_URL.format(parsed)

def get_booking_url(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return BOOKING_URL.format(parsed)

def get_pt_url(txt):
    parsed = urllib.parse.quote_plus(txt)
    return PT_URL.format(parsed)


def send_link(city, where):
    is_successful = False

    if city is None:
        comment = get_response_message(None, 'Không tìm thấy tên địa điểm trong comment', None)
    else:
        wiki_obj = get_location_meta(city)

        if wiki_obj is None:
            comment = get_response_message(None, 'Không tìm thấy địa điểm '.format(city), None, 'None')
        else:
            comment = get_response_message(wiki_obj.title, wiki_obj.desc, wiki_obj.link)

        print(f'{city} xử lý thành công!')
        is_successful = True

    try:
        where.reply(comment)
    except Exception as e:
        print(e)
    return is_successful


def get_location_meta(city):
    search = wikipedia.search(city)
    st = 0

    if search is None:
        return False

    # Get first location
    for result in search:
        try:
            page = wikipedia.page(title=result, auto_suggest=False)
        except wikipedia.DisambiguationError:
            return None
        except wikipedia.PageError:
            return None

        if is_location(page):
            summary = wikipedia.summary(page.title, sentences=3, auto_suggest=False)
            return LocationMeta(page.title, summary, page.coordinates[0], page.coordinates[1], page.url)

        if st > 3:
            return None
        st = st + 1

    return None


def is_location(page):
    for attr in page.categories:
        if attr == 'Coordinates on Wikidata':
            return True
    return False


def get_response_message(city, msg, link):
    if city is None:
        message = f'''
{msg}
{FOOTER}
'''
    else:
        message = f'''
Thông tin về địa điểm: {city}:\n\n {msg} \n\n
- links: [wiki]({link}) 
    ~[map]({get_map_link(city)}) 
    ~ [hotels]({get_booking_url(city)}) 
    ~ [pinterest]({get_pt_url(city)}) 
{FOOTER}'''

    return message

def main(r):
    try:
        inbox = list(r.inbox.unread())
    except praw.exceptions.APIException:
        print('Rate limited.')
        return False
    inbox.reverse()
    for item in inbox:
        if mention.lower() in item.body.lower():
            text = item.body
            result = re.search(BODY_REGEX, text, flags=re.IGNORECASE)
            if result is not None:
                body = result.group(1)
                if send_link(body, item):
                    item.mark_read()
            else:
                item.reply(f'Did not detect any message. Please try again\n\n{FOOTER}')
            sleep(10)