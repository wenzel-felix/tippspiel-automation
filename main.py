from twill.commands import *
import pandas as pd
import math
from files import *
import random
import datetime
import os


# login
go("https://www.kicktipp.de/ewaldbuli/profil/login")
fv('1', 'kennung', os.getenv("EMAIL"))
fv('1', 'passwort', os.getenv("PASSWORD"))
submit('1')

# evaluate best tipps
go("https://www.kicktipp.de/ewaldbuli/tippabgabe")
tipps = []

# favorite = 0 => tendency for awayTeam
favorite = int

html = show()
tables = pd.read_html(html)[0]
firstMatch = tables.iat[0, 0]

try:
    if datetime.datetime.strptime(firstMatch, "%d.%m.%y %H:%M") > datetime.datetime.now():
    # print("matching date")
        for index, row in tables.iterrows():
            try:
                if (home := float(row[4])) > (away := float(row[6])):
                    tendency = home/away
                    favorite = 0
                else:
                    tendency = away/home
                    favorite = 1
                tipps.append([favorite, int(math.log2(tendency+0.5))])
            except:
                print("no bet-ratings")
                tipps.append([0, 0])

        for i in tipps:
            if i[1] == 0:
                result, probability = zip(*remis)
            elif i[1] == 1:
                result, probability = zip(*oneahead)
            elif i[1] == 2:
                result, probability = zip(*twoahead)
            elif i[1] == 3:
                result, probability = zip(*threeahead)
            elif i[1] == 4:
                result, probability = zip(*fourahead)
            else:
                result = [str(i[1])+":0"]
                probability = [1]

            i[1] = random.choices(result, probability, k=1)[0]
            if i[0] == 0:
                i[1] = i[1][::-1]

        _, scores = zip(*tipps)
        scores = list(scores)

        for index in range(len(scores)):
            try:
                leftTeam, rightTeam = scores[index].split(":")
                fv(1, 5+(index*3), leftTeam)
                fv(1, 6+(index*3), rightTeam)
            except Exception:
                del scores[index]
                print("non valid input field")

        print(scores)

        submit('1')
except:
    print("except")

# logout
go("https://www.kicktipp.de/ewaldbuli/profil/logout")
