"""Gathers data and sends pushes"""

import json
import argparse

from datetime import datetime
from pushbullet import PushBullet
from live import gather_data, search_matches


# Load config from config.json

with open('config.json') as j:
    config = json.load(j)

api_key = config['api_key']
my_teams = config['my_teams']
days_notice = config['days_notice']
devices = config['devices']
ignore_list = config['ignore']


def show_devices():
    """Print out the users' devices showing the index position
    User can then add whichever devices he wants to in the config"""
    pushbullet = PushBullet(api_key)
    list_devices = pushbullet.devices
    for i, device in enumerate(list_devices):
        print '['+str(i)+']  -->  ' + device.nickname

# Command arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--devices', action='store_true',
    help='Print a list of your devices. See README for more info')
args = parser.parse_args()

if args.devices:
    show_devices()
    quit()



def less_than_days_notice(match):
    """Returns true if match starts in less than days_notice"""
    time = match["kickofftime"]

    difference = time - datetime.now()
    if difference.days <= days_notice:
        return True
    else:
        return False



def push(match):

    def send_push(title, body):
        pushbullet = PushBullet(api_key)
        if not devices:
            pushbullet.push_note(title=title, body=body)
        else:
            # load devices
            d = pushbullet.devices

            for i in devices:
                d[i].push_note(title=title, body=body)

    matchfixture = match["matchfixture"]
    competition = match["competition"]
    time = match["kickofftime"]
    channel = match["channels"]

    time_format = '%H:%M  -  %A %d %b %Y'

    time = time.strftime(time_format)

    title = 'Live match on TV'
    body = matchfixture+'\n'+competition+'\n'+time+'\n'+channel

    send_push(title, body)


if __name__ == '__main__':
    matches = gather_data()

    my_matches = search_matches(matches, my_teams, ignore_list)

    for match in my_matches:
        if less_than_days_notice(match):
            push(match)
