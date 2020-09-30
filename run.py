"""Gathers data and sends pushes"""

import json
import argparse
from datetime import datetime

from pushbullet import PushBullet
from live import gather_data, search_matches


with open('config.json') as j:
    config = json.load(j)

api_key = config['api_key']
my_teams = config['my_teams']
days_notice = config['days_notice']
device_idens = config['devices']
ignore_list = config['ignore']


def show_devices():
    """
    Print out the users' devices showing the index position
    User can then add whichever devices he wants to in the config
    """
    pushbullet = PushBullet(api_key)
    for i, device in enumerate(pushbullet.devices):
        print '[{}]  -->  {} ({})'.format(i, device.nickname, device.device_iden)


def less_than_days_notice(match):
    """
    Returns true if match starts in less than days_notice
    """
    time = match["date"]
    difference = time - datetime.now()
    return 0 < difference.days <= days_notice


def send_push(title, body):
    pushbullet = PushBullet(api_key)
    body_subject = body.partition('\n')[0].strip()
    if not device_idens:
        pushbullet.push_note(title=title, body=body)
        print "Pushed {0} to all devices".format(body_subject)
    else:
        for device in (device for device in pushbullet.devices if device.device_iden in device_idens):
            pushbullet.push_note(title=title, body=body, device=device)
            print "Pushed [{0}] to [{1}]".format(body_subject, device)


def push_match(match):
    matchfixture = match["fixture"]
    competition = match["competition"]
    time = match["date"]
    channel = match["channels"]

    time_format = '%H:%M  -  %A %d %b %Y'

    time = time.strftime(time_format)

    title = 'Live match on TV'
    body = matchfixture+'\n'+competition+'\n'+time+'\n'+channel
    body = body.encode('utf-8').strip()
    send_push(title, body)


if __name__ == '__main__':

    # Command arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--devices', action='store_true',
                        help=('Print a list of your devices.',
                              'See README for more info'))
    args = parser.parse_args()

    if args.devices:
        show_devices()
    else:
        matches = gather_data()

        my_matches = search_matches(matches, my_teams, ignore_list)

        for match in my_matches:
            if less_than_days_notice(match):
                push_match(match)
