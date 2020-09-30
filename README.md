## Live-Football-on-TV

Simple script that sends Pushbullet notification if your team is live on UK TV !

> www.live-footballontv.com is dedicated to providing the most up-to-date, extensive and accurate listings of live football on TV in the UK. Live-FootballOnTV.Com includes schedules of live football on television from broadcasters including: Sky Sports, BT Sport, BBC, ITV, British Eurosport, S4C, Premier Sports and more.

**What is the point?** To keep on top of when your team is on live UK television.

_Example notifications:_

![notification example screenshot](https://raw.githubusercontent.com/Saturn/live-football-ontv/master/screenshot.jpg)

1. Script pulls in all of the matches available on the www.live-footballontv.com page.
2. Parses each match into a single list and adds datetime object
3. Searches for matches based on your criteria such as _Arsenal_ or _Bradford_
4. Initiates a push notification for each match that fits your criteria

Times displayed on the source site are UK time.

#### Config

Config settings can be edited inside `config.json`

**`api_key`** - Pushbullet API key.

**`my_teams`** - List of strings matching the team or teams you are interested in.

**`days_notice`** - How many days in advance does a match have to be before a push will be sent.

**`ignore`** - Ignore certain types of matches. Maybe you want _Arsenal_ but not _Arsenal Ladies_.

**`devices`** - List of devices you want to push to. In the form of `["device_iden"]`. Each `device_iden` represents the device you want to send to. To see your account's devices and their device iden `python run.py --devices`.
Leave this empty if you want Pushbullet to send to all of your devices. (Which is the default behaviour)

**Example config**

```json
{
  "api_key": "PUSHBULLET__API__KEY",

  "my_teams": ["Arsenal", "Chelsea"],

  "days_notice": 2,

  "devices": [],

  "ignore": ["Ladies", "Women", "U21", "U18"]
}
```

You will get notified when the script runs if Arsenal or Chelsea are playing within live on UK television in the next 48 hours.

In this config example the user wants to receive push messages on two devices. To figure out the device iden of the devices you want:

`python run.py --devices`

```
[0]  -->  LGE Nexus 5 (iden_key_here)

[1]  -->  Firefox (iden_key_here)

[2]  -->  Chrome (iden_key_here)

[3]  -->  Galaxy Tab 4 (iden_key_here)
```

You can change the 'nickname' of your devices at https://www.pushbullet.com/#settings/devices.

#### Installing

Clone the repository. `git clone https://github.com/Saturn/live-football-ontv.git`

#### Cron

```
0 13 * * * cd /path/to/live-football-ontv && python run.py > /dev/null 2>&1
```

#### Pushbullet

A Pushbullet API_KEY is required in order to send pushes to your devices.

Get your API_KEY here https://www.pushbullet.com/#settings/account

API Documentation available here https://docs.pushbullet.com
