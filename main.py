from twill.commands import *
import pandas as pd
import math
import random
import datetime
import os
import json


historic_data = json.load(open("historic_data.json"))
tipp_group = os.getenv("NAME")
# login
go(f"https://www.kicktipp.de/{tipp_group}/profil/login")
fv('1', 'kennung', os.getenv("EMAIL"))
fv('1', 'passwort', os.getenv("PASSWORD"))
submit('1')

# evaluate best tipps
go(f"https://www.kicktipp.de/{tipp_group}/tippabgabe")
tipps = []

html = show()
tables = pd.read_html(html)[0]
firstMatch = tables.iat[0, 0]

try:
    match_date = datetime.datetime.strptime(firstMatch, "%d.%m.%y %H:%M")
    now = datetime.datetime.now()

    if match_date > now:
        for index, row in tables.iterrows():
            try:
                if (home := float(row[4].split("/")[0])) > (away := float(row[6])):
                    tendency = home/away
                    favorite = 0
                else:
                    tendency = away/home
                    favorite = 1
                tipps.append([favorite, int(math.log2(tendency+0.5))])
            except Exception as e:
                print("no bet-ratings")
                tipps.append([0, 0])

        for i in tipps:
            if i[1] == 0:
                result, probability = historic_data["remis"]
            elif i[1] == 1:
                result, probability = historic_data["oneahead"]
            elif i[1] == 2:
                result, probability = historic_data["twoahead"]
            elif i[1] == 3:
                result, probability = historic_data["threeahead"]
            elif i[1] == 4:
                result, probability = historic_data["fourahead"]
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
go(f"https://www.kicktipp.de/{tipp_group}/profil/logout")
