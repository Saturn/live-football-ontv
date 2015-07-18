""" Parses http://www.live-footballontv.com for info about live matches """

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

url = 'http://www.live-footballontv.com'
headers = {'User-Agent': 'Football Push Notifications'}

def convert_date(date):
    """Returns datetime object
    This will allow the script to calculate timedeltas and reformat the date easily"""
    regex_date = re.compile(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)+ \d{1,31}(th|rd|nd|st) +\w* \d\d\d\d')
    if not regex_date.match(date):
        raise Exception('Date was not the correct format')

    date = date.split(' ')
    date[1] = date[1][:-2]
    if len(date[1]) == 1:
        date[1] = '0'+date[1]
    date = ' '.join(date)

    date_format = '%A %d %B %Y'

    date_object = datetime.strptime(date, date_format)
    return date_object


def register_match(match, date):
    """Parses the match item into a simple dict"""
    kotime = match[2].text
    if kotime == 'TBC':
        kotime = '12:00'

    kotime = kotime.split(':')
    # Date of match plus the kick off time
    kotime = date + timedelta(hours=int(kotime[0]), minutes=int(kotime[1]))


    match_dict = {
        "matchfixture": match[0].text,
        "competition": match[1].text,
        "kickofftime": kotime,
        "channels": match[3].text
        }

    return match_dict




def search_matches(match_list, search_list):
    """Return list of football matches that match search"""

    search = re.compile('|'.join(search_list))
    my_matches = []
    for matches in match_list:
        if search.search(matches["matchfixture"]):
            my_matches.append(matches)

    return my_matches



def gather_data():
    """Returns the list of matches"""
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

    # Get rid of <hr> cruft
    for node in soup.findAll('hr'):
        node.replaceWithChildren()

    # Get the date nodes
    result = soup.find_all('div', class_='span12 matchdate')

    dates = []

    for item in result:
        dates.append(item.parent)

    # Holds the list of dictionaries
    matches = []

    for item in dates:
        date = convert_date(item.text)
        cursor = item.findNextSibling()

        while True:
            try:
                if cursor.next.attrs == {u'class': [u'span12', u'matchdate']}:
                    break
                else:
                    matches.append(register_match(cursor.contents, date))
                    cursor = cursor.findNextSibling()
            except Exception:
                break

    return matches
