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

    loszuteilung = [0]
    aktiveslos = 0

    if request.method == "POST":
        if request.form.get("eintragen") == "Eintragen":
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
                    {"weltmeisterschaft_freistil": {"gewicht": int(gewicht), "losnummer": losnummer}}]})
            with open('ringerdatenbank.json', 'w') as f:
                json.dump(ringerdatenbank_dict, f, indent=4, separators=(',', ':'), sort_keys=True)
            print(loszuteilung)
    return render_template("index.html")


@app.route("/gewichterliste")
def gewichterliste():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)
    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)
    ringerindex = 0
    gewichtseinteilung = 0
    anz_gewichtsklassen = len(turnierdatenbank_dict[0]["2021"][0]["weltmeisterschaft_freistil"]["gewichtsklassen"])
    gewichtsklassenindex = 0

    # die ringer mit den gewichten in Gewichtsklassen einteilen
    for ringer in ringerdatenbank_dict: #für jeden Ringer
        gewichtseinteilung = ringerdatenbank_dict[ringerindex]["turniere"][0]["weltmeisterschaft_freistil"]["gewicht"] #Variable "gewichtseintelung" gesetzt, damit der wert im json unverändert bleibt
        ringerdatenbank_dict[ringerindex]["turniere"][0]["weltmeisterschaft_freistil"]["gewichtsklasse"] = "" #leeren wwert der Gewichtsklasse bei jedem Ringer hinterlegt, damit der Wert überprüft werden kann
        while ringerdatenbank_dict[ringerindex]["turniere"][0]["weltmeisterschaft_freistil"]["gewichtsklasse"] == "": #solange dieser Wert (siehe Zeile oben) gleich "" ist muss wiederholt werden
            for gewicht in turnierdatenbank_dict[0]["2021"][0]["weltmeisterschaft_freistil"]["gewichtsklassen"]: #für jedes Gewicht bei den Erfassten Gewichtern in der Turnierdatenbank
                if gewichtseinteilung == turnierdatenbank_dict[0]["2021"][0]["weltmeisterschaft_freistil"]["gewichtsklassen"][gewichtsklassenindex]["gewicht"]: #stimmt das Prüfgewicht (gewichtseinteilung) mit der Gewichtsklasse in der TurnierDB überein, dann kann dieses eingetragen werden
                    ringerdatenbank_dict[ringerindex]["turniere"][0]["weltmeisterschaft_freistil"]["gewichtsklasse"] = gewichtseinteilung
                    if ringerdatenbank_dict[ringerindex]["ringerID"] not in turnierdatenbank_dict[0]["2021"][0]["weltmeisterschaft_freistil"]["gewichtsklassen"][gewichtsklassenindex]["teilnehmer"]: #damit die ringerIDs nur einmal in der Turnierdatenbank erfasst werden
                        turnierdatenbank_dict[0]["2021"][0]["weltmeisterschaft_freistil"]["gewichtsklassen"][gewichtsklassenindex]["teilnehmer"].append(ringerdatenbank_dict[ringerindex]["ringerID"]) #ordnet ringerID dem entsprechendem Gewicht zu.
                else:
                    gewichtsklassenindex = gewichtsklassenindex + 1
            gewichtsklassenindex = 0
            gewichtseinteilung = gewichtseinteilung + 1
        ringerindex = ringerindex + 1
    with open('ringerdatenbank.json', 'w') as r:
        json.dump(ringerdatenbank_dict, r, indent=4, separators=(',', ':'), sort_keys=True)
    with open('turnierdatenbank.json', 'w') as t:
        json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'), sort_keys=True)
    # alle ringer für html in tuple
    ringerindex = 0
    output_ringer_fix = ()
    for ringer in ringerdatenbank_dict:
        output_ringer_temp = ((ringerdatenbank_dict[ringerindex]["turniere"][0]["weltmeisterschaft_freistil"][
                                   "gewichtsklasse"], ringerdatenbank_dict[ringerindex]["vorname"],
                               ringerdatenbank_dict[ringerindex]["nachname"],
                               ringerdatenbank_dict[ringerindex]["land"]),)
        output_ringer_fix = output_ringer_fix + output_ringer_temp
        ringerindex = ringerindex + 1
    #habe ich von https://www.gkindex.com/python-tutorial/python-nested-tuples.jsp
    output_ringer_fix = sorted(output_ringer_fix, key=lambda x: x[0])

    return render_template("gewichterliste.html", ringerliste=output_ringer_fix)


@app.route("/matte1", methods=["GET", "POST"])
def matte1():
    return render_template("matte1.html")


@app.route("/matte2")
def matte2():
    return render_template("matte2.html")


@app.route("/matte3")
def matte3():
    return render_template("matte3.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
