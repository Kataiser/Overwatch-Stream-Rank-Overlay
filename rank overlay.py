import urllib.request
import time
from time import localtime, strftime
import re

print("Overwatch Stream Rank Overlay - made by Kataiser")

#url = 'https://owapi.net/api/v3/u/Kataiser-11855/stats?platform=pc'
urlpre = 'https://owapi.net/api/v3/u/'
urlpost = '/stats?platform='
battlenet = input('Battle.net ID (formatted as "Example-1234" if PC and "Example" if not): ')
if battlenet == '':
    battlenet = 'Kataiser-11855'
platform = ''
platforms = ['pc', 'xbl', 'psn']
while platform not in platforms:
    platform = input("Platform (pc, xbl, or psn): ").lower()
    if platform not in platforms:
        print("One of the three, please.")
if platform == 'pc':
    i = battlenet.find('-')
    bnetshort = battlenet[0:i]
else:
    bnetshort = battlenet
url = urlpre + battlenet + urlpost + platform
loopdelay = None
while not loopdelay:
    i = input("How long to wait between updates, in minutes: ")
    try:
        loopdelay = float(i)
    except ValueError:
        print("Needs to be a number.")

looptimes = 0
while True:
    looptimes += 1
    print("--------------------------")
    print("Run " + str(looptimes) + ", at " + str(strftime('%I:%M:%S', localtime())))
    print("Getting stats.")

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    try:
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode('utf-8')
        #print(data)
    except:
        print("Either player doesn't exist, or a connection can't be made.")
        break

    rankpos = data.find('comprank')
    #print(rankpos)
    comprank = data[rankpos+11:rankpos+15]
    comprank = int(re.sub('[^0-9]', '', str(comprank)))
    print(bnetshort + "'s rank is " + str(comprank))

    with open(battlenet + '.txt', 'w') as out:
        out.write(str(comprank))

    with open(platform + '.txt', 'r+') as out:
        if battlenet not in out.read():
            out.write(battlenet + '\n')
            print("Saved player to " + platform + '.txt (first time seen)')

    print("Waiting for " + str(loopdelay) + " minutes.")
    time.sleep(loopdelay * 60)
