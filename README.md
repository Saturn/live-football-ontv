## Live-Football-on-TV


Simple script that sends PushBullet notification if your team is live on UK TV !

It is meant to be run periodically via cron. Once a day should be good.


> http://www.live-footballontv.com is dedicated to providing the most up-to-date, extensive and accurate listings of live football on TV in the UK. Live-FootballOnTV.Com includes schedules of live football on television from broadcasters including: Sky Sports, BT Sport, BBC, ITV, British Eurosport, S4C, Premier Sports and more.

1. Script pulls in all of the matches available on the http://www.live-footballontv.com page.
2. Parses each match into a single list while applying a sane date format
3. Searches for matches based on your criteria such as *Arsenal* or *Bradford*
4. Initiates a push notification for each match it finds

Times displayed on the source site are UK time. This script runs a `datetime.now()` command so your current timezone may be different.

####Config

Config settings can be edited inside `config.json`

**`api_key`** - Pushbullet API key.

**`my_teams`** - List of strings matching the team or teams you are interested in

**`days_notice`** - How many days in advance does a match have to be before a push will be sent.

**`devices`** - List of devices you want to push to. In the form of `[0,1,2]`. Each index represents the device you want to send to. To see your account's devices and their index `python run.py --devices`. 
Leave this empty if you wish want PushBullet to send to all of your devices. (Which is default behaviour)

#####Example config
```json
{

	"api_key": "PUSHBULLET__API__KEY",

	"my_teams": ["Arsenal", "Chelsea"],

	"days_notice": 2,

	"devices": [0, 3]
}
```
You will get notified when the script runs if Arsenal or Chelsea are playing within live on UK tv in the next 48 hours. (Or at least that is what I intend!!)

In this config example the user wants to receive push messages on two devices. To figure out the index number of the devices you want:

`python run.py --devices`

```
[0]  -->  LGE Nexus 5

[1]  -->  Firefox

[2]  -->  Chrome

[3]  -->  Galaxy Tab 4
```

You can change the 'nickname' of your devices at https://www.pushbullet.com/#settings/devices.


####Installing

Clone the repository. `git clone https://github.com/Saturn/live-football-ontv.git`

A virtualenv is highly recommended. https://virtualenv.pypa.io

Create a virtualenv inside of the projects directory for simplicity.

Once inside virtualenv run `pip install -r requirements.txt` to install dependencies.

**Cron example**

`0 13 * * * cd /path/to/live-football-ontv; venv/bin/python run.py >/dev/null 2>&1`

####PushBullet
A PushBullet API_KEY is required in order to send pushes to your devices.

Get your API_KEY here: '''https://www.pushbullet.com/#settings/account'''

API Documentation available here https://docs.pushbullet.com

