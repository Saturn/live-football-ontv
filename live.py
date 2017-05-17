""" Parses http://www.live-footballontv.com for info about live matches """

import re
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


url = 'http://www.live-footballontv.com'
headers = {'User-Agent': 'Football Push Notifications'}


def convert_date(date):
    """Returns datetime object from date string
    eg Friday 6th October 2025"""
    date = date.split(' ')
    date[1] = date[1][:-2]
    if len(date[1]) == 1:
        date[1] = '0'+date[1]
    date = ' '.join(date)

    date_format = '%A %d %B %Y'
    date_object = datetime.strptime(date, date_format)
    return date_object


def search_matches(match_list, search_list, ignore_list=None):
    """Return list of football matches that match search"""
    if ignore_list is None:
        ignore_list = []

    search = re.compile('|'.join(search_list))

    my_matches = [m for m in match_list if search.search(m['fixture'])]

    if ignore_list:
        ignore = re.compile('|'.join(ignore_list))
        my_matches = [m for m in my_matches if not ignore.search(m["fixture"])]

    return my_matches


def gather_data():
    """Returns the list of matches"""
    soup = BeautifulSoup(requests.get(url, headers=headers).text)

    data = soup.find_all(True, {'class': ['matchdate',
                                          'matchfixture',
                                          'competition',
                                          'kickofftime',
                                          'channels']})
    dates = []
    matches = []
    i = 0
    while i < len(data):
        if 'matchdate' in data[i].attrs.values()[0]:
            dates.append(convert_date(data[i].text))
            i += 1
        else:
            d = {}
            d['fixture'] = data[i].text
            d['competition'] = data[i + 1].text
            d['kotime'] = data[i + 2].text
            d['channels'] = data[i + 3].text
            kotime = d['kotime']
            if kotime != 'TBC':
                hours, minutes = kotime.split(':')
                date = dates[-1] + timedelta(hours=int(hours), minutes=int(minutes))
                d['date'] = date
            matches.append(d)
            i += 4

    return matches
