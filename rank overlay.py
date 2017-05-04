import urllib.request
import time
from time import gmtime, strftime
import re
#import tkinter as tk
#import pygubu

'''class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('gui2.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()'''
#This gui can wait

#url = 'https://owapi.net/api/v3/u/Kataiser-11855/stats?platform=pc'
urlpre = 'https://owapi.net/api/v3/u/'
urlpost = '/stats?platform='
battlenet = input('Battle.net ID (formatted as "Example-1234" if PC and "Example" if not): ')
if battlenet == '':
    battlenet = 'Kataiser-11855'
platform = input("Platform (pc, xbl, or psn): ").lower()
url = urlpre + battlenet + urlpost + platform
loopdelay = float(input("How long to wait between updates, in minutes: "))

looptimes = 0
while True:
    looptimes += 1
    print("--------------------------")
    print("Run " + str(looptimes) + ", at " + str(strftime('%H:%M:%S', gmtime())))
    print("Getting stats.")

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    #path = 'us.stats.competitive.overall_stats.comprank'

    try:
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read().decode('utf-8')
        #print(data)
    except:
        print("Either player doesn't exist, or a connection can't be made.")
        break

    #print('\n')
    rankpos = data.find('comprank')
    #print(rankpos)
    comprank = data[rankpos+11:rankpos+15]
    comprank = int(re.sub('[^0-9]', '', str(comprank)))
    print(battlenet + "'s rank is " + str(comprank))

    with open(battlenet + '.txt', 'w') as out:
        out.write(str(comprank))

    with open(platform + '.txt', 'r+') as out:
        if battlenet not in out.read():
            out.write(battlenet + '\n')
            print("Saved player to " + platform + '.txt (first time seen)')

    print("Waiting for " + str(loopdelay) + " minutes.")
    time.sleep(loopdelay * 60)

#with urllib.request.urlopen(url, None) as f:
#     print(f.read(300))
