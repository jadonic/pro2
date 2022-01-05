import json

from flask import Flask
from flask import render_template
from flask import request
from random import randrange

app = Flask("Hello World")

@app.route("/hello", methods=["GET", "POST"])
def hello_post():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)

    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)

    counter = 0
    loszuteilung = [0]
    aktiveslos = 0
    listevornamen = ["Lukas", "Jonas", "Carl", "Hermann", "Paul", "Fabian", "Walter", "Joel", "Pascal", "Renato", "Benjamin", "Michael", "Jürg", "Silvan", "Flavio", "Andreas", "Samuel", "Dominik", "Janis", "Maurus"]
    listenachnamen = ["Müller", "Schmid", "Fischer", "Zimmermann", "Bauer", "Freuler", "Baumgartner", "Stieger", "Meyer", "Scholz", "Vetsch", "Wieland", "Freuler", "Kaiser", "Altmann", "Weber", "Kaufmann", "Wolf", "Knorr", "Zogg"]
    listelaender = ["Schweiz", "Österreich", "Deutschland", "Italien", "Kanada", "Kuba", "China", "Russland", "Georgien", "Argentinien", "Schweden", "Ukraine", "Indien", "Südafrika", "Spanien", "Chile", "Mexiko", "Türkei", "Japan", "Liechtenstein"]
    listegewichter = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74]

    if request.method == "POST":
        if request.form.get("eintragen") == "Eintragen":
            if int(request.form["gewicht"]) < 65:
                print("sie sind leider zu leicht, um mitzumachen!")
            elif int(request.form["gewicht"]) > 74:
                print("sie sind leider zu schwer, um mitzumachen!")
            else:
                if ringerdatenbank_dict != []:
                    ringerID = ringerdatenbank_dict[-1]["ringerID"] + 1
                elif ringerdatenbank_dict == []:
                    ringerID = 100000
                # nimmt daten von erstem Formular entgegen
                vorname = request.form["vorname"]
                nachname = request.form["nachname"]
                land = request.form["land"]
                gewicht = request.form["gewicht"]
                # zufällige Loszuteilung der ringer, https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
                while aktiveslos in loszuteilung:
                    aktiveslos = randrange(1, 100)
                losnummer = aktiveslos
                loszuteilung.append(losnummer)
                # 1. Eintrag Ringer ins Json übertragen
                ringerdatenbank_dict.append(
                    {"ringerID": ringerID, "vorname": vorname, "nachname": nachname, "land": land, "turniere": [
                        {"beispielturnier": {"gewicht": int(gewicht), "losnummer": losnummer, "gewichtsklasse": 74}}]})
                with open('ringerdatenbank.json', 'w') as f:
                    json.dump(ringerdatenbank_dict, f, indent=4, separators=(',', ':'), sort_keys=True)
                print(loszuteilung)
        if request.form.get("zufaellig") == "Zufälligen Ringer erstellen":
            if ringerdatenbank_dict != []:
                ringerID = ringerdatenbank_dict[-1]["ringerID"] + 1
            elif ringerdatenbank_dict == []:
                ringerID = 100000
            vorname = listevornamen[randrange(0, 19)]
            nachname = listenachnamen[randrange(0, 19)]
            land = listelaender[randrange(0, 19)]
            gewicht = listegewichter[randrange(0,9)]
            while aktiveslos in loszuteilung:
                aktiveslos = randrange(1, 100)
            losnummer = aktiveslos
            loszuteilung.append(losnummer)
            # 1. Eintrag Ringer ins Json übertragen
            ringerdatenbank_dict.append(
                {"ringerID": ringerID, "vorname": vorname, "nachname": nachname, "land": land, "turniere": [
                    {"beispielturnier": {"gewicht": int(gewicht), "losnummer": losnummer, "gewichtsklasse": 74}}]})
            with open('ringerdatenbank.json', 'w') as f:
                json.dump(ringerdatenbank_dict, f, indent=4, separators=(',', ':'), sort_keys=True)

    for ringer in ringerdatenbank_dict:
        # habe ich von https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
        if not any(d["ringerID"] == ringerdatenbank_dict[counter]["ringerID"] for d in
                   turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"]):
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].append(
                {"ringerID": ringerdatenbank_dict[counter]["ringerID"],
                 "losnummer": ringerdatenbank_dict[counter]["turniere"][0]["beispielturnier"]["losnummer"],
                 "vornameNachname": ringerdatenbank_dict[counter]["vorname"] + " " + ringerdatenbank_dict[counter][
                     "nachname"], "turnierPunkte": 0})
        counter = counter + 1
    # sortiert Teilnehmer in der Gewichtsklasse nach der Losnummer, von https://linuxhint.com/sort-json-objects-python/
    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(key=lambda x: x["losnummer"])

    with open('turnierdatenbank.json', 'w') as t:
        json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'))

    # alle ringer für html in tuple
    ringerindex = 0
    output_ringer_fix = ()
    for ringer in ringerdatenbank_dict:
        output_ringer_temp = ((ringerdatenbank_dict[ringerindex]["turniere"][0]["beispielturnier"][
                                   "losnummer"], ringerdatenbank_dict[ringerindex]["vorname"],
                               ringerdatenbank_dict[ringerindex]["nachname"],
                               ringerdatenbank_dict[ringerindex]["land"]),)
        output_ringer_fix = output_ringer_fix + output_ringer_temp
        ringerindex = ringerindex + 1

    # habe ich von https://www.gkindex.com/python-tutorial/python-nested-tuples.jsp
    output_ringer_fix = sorted(output_ringer_fix, key=lambda x: x[0])
    neededringer = 8 - len(output_ringer_fix)


    return render_template("index.html", anzahlringer=len(output_ringer_fix), ringerliste=output_ringer_fix, neededringer=neededringer)


@app.route("/matte1", methods=["GET", "POST"])
def matte1():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)
    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)

    runde3sortierung = [0, 3, 1, 4]
    endsortierung = [13, 4, 10, 1, 12, 3, 9, 0]
    ringerrot = ""
    ringerblau = ""
    sessionid = 0
    kampfhistorie = []
    buttoneintragen = False

    if request.method == "POST":
        if request.form.get("kampfinitiieren") == "Kampf starten / nächster Kampf":
            buttoneintragen = True
            if turnierdatenbank_dict["rundencounter"] <= 3:
                turnierdatenbank_dict["kampfcounter"] = turnierdatenbank_dict["kampfcounter"] + 1
                if turnierdatenbank_dict["kampfcounter"] > 4:
                    turnierdatenbank_dict["kampfcounter"] = 0
                    turnierdatenbank_dict["kampfcounter"] = turnierdatenbank_dict["kampfcounter"] + 1
                    turnierdatenbank_dict["rundencounter"] = turnierdatenbank_dict["rundencounter"] + 1
                    turnierdatenbank_dict["rundenpunkte"] = turnierdatenbank_dict["rundenpunkte"] * 3
                    turnierdatenbank_dict["ringerindex"] = 0

                if turnierdatenbank_dict["rundencounter"] == 2 and turnierdatenbank_dict["kampfcounter"] == 1:
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(key=lambda x: x["turnierPunkte"])

                if turnierdatenbank_dict["rundencounter"] == 3 and turnierdatenbank_dict["kampfcounter"] == 1:
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(key=lambda x: runde3sortierung.index(x["turnierPunkte"]))

                if turnierdatenbank_dict["kampfcounter"] <= 4:
                    if turnierdatenbank_dict["kampfcounter"] > 1:
                        turnierdatenbank_dict["ringerindex"] = turnierdatenbank_dict["ringerindex"] + 2
                    ringerrot = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["vornameNachname"]
                    ringerblau = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["vornameNachname"]
                    turnierdatenbank_dict["kampfid"] = turnierdatenbank_dict["kampfid"] + 1
                    sessionid = sessionid + 1
            else:
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(
                    key=lambda x: endsortierung.index(x["turnierPunkte"]))
            for element in turnierdatenbank_dict["kampfhistorie"]:
                kampfhistorie.append((element["kampfId"], element["ringerVNrot"], element["punkteRot"], element["ringerVNblau"], element["punkteBlau"]))

        if request.form.get("dateneintragen") == "daten eintragen":
            buttoneintragen = False
            sessionid = sessionid + 1
            if request.form["punkterot"] > request.form["punkteblau"]:
                siegerfarbe = "rot"
                sieger = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["ringerID"]
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["turnierPunkte"] = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["turnierPunkte"] + turnierdatenbank_dict["rundenpunkte"]

            elif request.form["punkteblau"] > request.form["punkterot"]:
                siegerfarbe ="blau"
                sieger = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["ringerID"]
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["turnierPunkte"] = \
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["turnierPunkte"] + turnierdatenbank_dict["rundenpunkte"]

            turnierdatenbank_dict["kampfhistorie"].append(
                {"kampfId": turnierdatenbank_dict["kampfid"], "ringerBlau": turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["ringerID"], "ringerVNblau": turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1]["vornameNachname"],
                 "ringerRot": turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["ringerID"], "ringerVNrot": turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]]["vornameNachname"],
                 "punkteRot": request.form["punkterot"], "punkteBlau": request.form["punkteblau"], "sieger": sieger})
            for element in turnierdatenbank_dict["kampfhistorie"]:
                kampfhistorie.append((element["kampfId"], element["ringerVNrot"], element["punkteRot"], element["ringerVNblau"], element["punkteBlau"]))
            if turnierdatenbank_dict["kampfid"] == 112:
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(
                    key=lambda x: endsortierung.index(x["turnierPunkte"]))


    with open('ringerdatenbank.json', 'w') as r:
        json.dump(ringerdatenbank_dict, r, indent=4, separators=(',', ':'), sort_keys=True)
    with open('turnierdatenbank.json', 'w') as t:
        json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'))


    return render_template("matte1.html", buttoneintragen=buttoneintragen, kampfhistorie=kampfhistorie, ringerrot=ringerrot, ringerblau=ringerblau, runde=turnierdatenbank_dict["rundencounter"], kampfid=turnierdatenbank_dict["kampfid"])


@app.route("/rangliste", methods=["GET", "POST"])
def rangliste():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)
    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)
    rang = 0
    rangliste = []

    for teilnehmer in turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"]:
        for ringer in ringerdatenbank_dict:
            if teilnehmer["ringerID"] == ringer["ringerID"]:
                rang = rang + 1
                name = teilnehmer["vornameNachname"]
                nationalitaet = ringer["land"]
                punkte = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][0]["turnierPunkte"]
                rangliste.append((rang, name, nationalitaet, punkte))

    if request.method == "POST":
        if request.form.get("neustart") == "Turnier neu starten!":
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"] = []
            turnierdatenbank_dict["kampfhistorie"] = []
            turnierdatenbank_dict["ringerindex"] = 0
            turnierdatenbank_dict["rundencounter"] = 1
            turnierdatenbank_dict["kampfcounter"] = 0
            turnierdatenbank_dict["rundenpunkte"] = 1
            turnierdatenbank_dict["kampfid"] = 100
            ringerdatenbank_dict = []

            with open('ringerdatenbank.json', 'w') as r:
                json.dump(ringerdatenbank_dict, r, indent=4, separators=(',', ':'), sort_keys=True)
            with open('turnierdatenbank.json', 'w') as t:
                json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'))

            return render_template("index.html", anzahlringer=0, ringerliste=[], neededringer=8)

    return render_template("rangliste.html", rangliste=rangliste)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
