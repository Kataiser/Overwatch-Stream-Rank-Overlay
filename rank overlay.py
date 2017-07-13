import urllib.request
import time
from time import localtime, strftime
import re
import winsound
import configparser
import ast

print("Overwatch Stream Rank Overlay - made by Kataiser")
dev = False

#url = 'https://owapi.net/api/v3/u/Kataiser-11855/stats?platform=pc'
urlpre = 'https://owapi.net/api/v3/u/'
urlpost = '/stats?platform='

battlenet = ''
while battlenet == '':
    battlenet = input('Battle.net ID (formatted as "Example-1234" if PC and "Example" if not): ')
    if battlenet == '':
        if dev:
            battlenet = 'Kataiser-11855'
        else:
            print('Please actually enter an ID.')

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

loopdelay = 0
if dev:
    loopdelaymin = 0.1
else:
    loopdelaymin = 0.5
while loopdelay < loopdelaymin:
    i = input("How long to wait between updates, in minutes: ")
    try:
        loopdelay = float(i)
        if loopdelay < loopdelaymin:
            print("Needs to be " + str(loopdelaymin) + " or larger, to avoid overstressing the API.")
    except ValueError:
        print("Needs to be a number.")

config = configparser.ConfigParser()
with open('settings.ini', 'r') as configfile:
    config.read('settings.ini')
    maxtime = float(config['MAIN']['maxhours'])
    playsound = ast.literal_eval(config['MAIN']['playsound'])
    prefix = str(config['MAIN']['prefix'])
print("Max running time is " + str(maxtime) + " hours (edit with settings.ini).")

print("Starting main loop.\n")

looptimes = 0
loops_t1 = time.time()
while (time.time() - loops_t1) < (maxtime * 3600):
    looptimes += 1
    print("--------------------------")
    print("Run " + str(int(looptimes)) + ", at " + str(strftime('%I:%M:%S', localtime())) + " (" + str((time.time() - loops_t1) / 60)[0:3] + " minutes since start)")
    print("Getting stats...")

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    try:
        request = urllib.request.Request(url, None, headers)
        api_t1 = time.time()
        response = urllib.request.urlopen(request)
        api_t2 = time.time()
        searchtime = str(api_t2 - api_t1)[0:3]
        data = response.read().decode('utf-8')
        print("Stats found in " + searchtime + " seconds.")
        #print(data)
    except:
        print("Either player doesn't exist, or a connection can't be made.")
        break

    rankpos = data.find('comprank')
    #print(rankpos)
    comprank = data[rankpos+11:rankpos+15]
    if str(comprank) != 'null':
        comprank = int(re.sub('[^0-9]', '', str(comprank)))
        print(bnetshort + "'s rank is " + str(comprank) + ".")
    else:
        print("This player doesn't seem to have a rank for this season.")
        comprank = 0

    fname = battlenet + '.txt'
    try:
        file = open(fname, 'r')
    except FileNotFoundError:
        file = open(fname, 'w')
    with open(fname, 'r') as out:
        if str(comprank) not in out.read() and playsound:
            try:
                winsound.PlaySound('rankchange.wav', winsound.SND_FILENAME)
            except:
                print("Sound effect can't be played.")
    with open(fname, "w") as out:
        out.write(prefix + ' ' + str(comprank))
    print("Saved to user's file, point streaming program at it.")
    #print("Couldn't save to user's file!")

    try:
        with open(platform + '.txt', 'r+') as out:
            if battlenet not in out.read():
                out.write(battlenet + '\n')
                print("Saved player to " + platform + '.txt (first time seen)')
    except:
        print("Couldn't save to platform file!")

    print("Waiting for " + str(loopdelay) + " minutes...")
    time.sleep(loopdelay * 60)

print("\nReached max loop time (" + str(maxtime) + " hours), exiting. If that's too short, edit maxhours.txt.")
