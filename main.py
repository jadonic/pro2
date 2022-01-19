import json
from flask import Flask
from flask import render_template
from flask import request
from random import randrange

app = Flask("Hello World")


@app.route("/", methods=["GET", "POST"])
def hello_post():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)

    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)

    aktiveslos = 0

    # Listen für Zufallsringer
    listevornamen = ["Lukas", "Jonas", "Carl", "Hermann", "Paul", "Fabian", "Walter", "Joel", "Pascal", "Renato",
                     "Benjamin", "Michael", "Jürg", "Silvan", "Flavio", "Andreas", "Samuel", "Dominik", "Janis",
                     "Maurus"]
    listenachnamen = ["Müller", "Schmid", "Fischer", "Zimmermann", "Bauer", "Freuler", "Baumgartner", "Stieger",
                      "Meyer", "Scholz", "Vetsch", "Wieland", "Freuler", "Kaiser", "Altmann", "Weber", "Kaufmann",
                      "Wolf", "Knorr", "Zogg"]
    listelaender = ["Schweiz", "Österreich", "Deutschland", "Italien", "Kanada", "Kuba", "China", "Russland",
                    "Georgien", "Argentinien", "Schweden", "Ukraine", "Indien", "Südafrika", "Spanien", "Chile",
                    "Mexiko", "Türkei", "Japan", "Liechtenstein"]
    listegewichter = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74]

    if request.method == "POST":
        if request.form.get(
                "eintragen") == "Eintragen":  # wenn der Button zum manuellen Eintragen eines Ringers gedrückt wird
            if int(request.form["gewicht"]) < 65:  # Prüfung ob Minimalgewicht erreicht
                print("sie sind leider zu leicht, um mitzumachen!")
            elif int(request.form["gewicht"]) > 74:  # Prüfung ob Maximalgewicht erreicht
                print("sie sind leider zu schwer, um mitzumachen!")
            else:
                if ringerdatenbank_dict != []:  # wenn mindestens ein Ringer erfasst ist, dann basierend auf dem Letzten Datenbankeintrag eine neue RingerID erstellen
                    ringerID = ringerdatenbank_dict[-1]["ringerID"] + 1
                elif ringerdatenbank_dict == []:  # wenn noch kein Ringer erfasst ist, erste RingerID setzen
                    ringerID = 100000
                # nimmt Daten von erstem Formular entgegen
                vorname = request.form["vorname"]
                nachname = request.form["nachname"]
                land = request.form["land"]
                gewicht = request.form["gewicht"]
                # zufällige Loszuteilung der Ringer, https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
                while aktiveslos in turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"]:
                    aktiveslos = randrange(1, 100)
                turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"].append(aktiveslos)

                # 1. Ringer eintragen und ins Json übertragen
                ringerdatenbank_dict.append(
                    {"ringerID": ringerID, "vorname": vorname, "nachname": nachname, "land": land, "turniere": [
                        {"beispielturnier": {"gewicht": int(gewicht), "losnummer": aktiveslos, "gewichtsklasse": 74}}]})
                with open('ringerdatenbank.json', 'w') as f:
                    json.dump(ringerdatenbank_dict, f, indent=4, separators=(',', ':'), sort_keys=True)

        if request.form.get(
                "zufaellig") == "Zufälligen Ringer erstellen":  # wenn Button für zufälligen Ringer gedrückt wird
            if ringerdatenbank_dict != []:
                ringerID = ringerdatenbank_dict[-1]["ringerID"] + 1
            elif ringerdatenbank_dict == []:
                ringerID = 100000
            vorname = listevornamen[randrange(0, 19)]
            nachname = listenachnamen[randrange(0, 19)]
            land = listelaender[randrange(0, 19)]
            gewicht = listegewichter[randrange(0, 9)]
            while aktiveslos in turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"]:
                aktiveslos = randrange(1, 100)
            turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"].append(aktiveslos)

            ringerdatenbank_dict.append(
                {"ringerID": ringerID, "vorname": vorname, "nachname": nachname, "land": land, "turniere": [
                    {"beispielturnier": {"gewicht": int(gewicht), "losnummer": aktiveslos, "gewichtsklasse": 74}}]})
            with open('ringerdatenbank.json', 'w') as f:
                json.dump(ringerdatenbank_dict, f, indent=4, separators=(',', ':'), sort_keys=True)

        if request.form.get(
                "neu") == "Teilnehmer neu eintragen":  # falls alle Teilnehmer gelöscht und neu eingetragen werden sollen
            ringerdatenbank_dict = []
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"] = []
            turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"] = [0]

            # alle Änderungen ins Json übernehmen
            with open('ringerdatenbank.json', 'w') as r:
                json.dump(ringerdatenbank_dict, r, indent=4, separators=(',', ':'), sort_keys=True)
            with open('turnierdatenbank.json', 'w') as t:
                json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'))

    # Ringer aus Ringerdatenbank in Turnierdatenbank übernehmen
    for ringer in ringerdatenbank_dict:
        # habe ich von https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
        if not any(d["ringerID"] == ringer["ringerID"] for d in
                   turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"]):
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].append(
                {"ringerID": ringer["ringerID"],
                 "losnummer": ringer["turniere"][0]["beispielturnier"]["losnummer"],
                 "vornameNachname": ringer["vorname"] + " " + ringer["nachname"], "turnierPunkte": 0})

    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(key=lambda x: x[
        "losnummer"])  # sortiert Teilnehmer in der Gewichtsklasse nach der Losnummer, von https://linuxhint.com/sort-json-objects-python/

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

    # Hinzufügen von nested Tuples, habe ich von https://www.gkindex.com/python-tutorial/python-nested-tuples.jsp
    output_ringer_fix = sorted(output_ringer_fix, key=lambda x: x[0])
    neededringer = 8 - len(output_ringer_fix)

    return render_template("index.html", anzahlringer=len(output_ringer_fix), ringerliste=output_ringer_fix,
                           neededringer=neededringer)


@app.route("/matte1", methods=["GET", "POST"])
def matte1():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)
    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)

    runde3sortierung = [0, 3, 1, 4]  # Sortierreihenfolge für Runde 3
    endsortierung = [13, 4, 10, 1, 12, 3, 9, 0]  # Sortierreihenfolge für Rangvergabe
    ringerrot = ""
    ringerblau = ""
    kampfhistorie = []  # Liste für Kampfhistorie-Darstellung im HTML
    siegerfarbe = ""
    buttoneintragen = False  # Boolean zur Anzeigereglung von HTML Elementen, siehe matte1.html

    if request.method == "POST":
        if request.form.get(
                "kampfinitiieren") == "Kampf starten / nächster Kampf":  # wenn der nächste Kampf gestartet werden soll
            buttoneintragen = True
            if turnierdatenbank_dict[
                "rundencounter"] <= 3:  # gilt nur für 3 Runden (8 Teilnehmer sind genau drei Runden à 4 Kämpfe)
                turnierdatenbank_dict["kampfcounter"] = turnierdatenbank_dict["kampfcounter"] + 1

                # prüft ob eine Runde abgeschlossen wurde und passt nötige Variabeln an
                if turnierdatenbank_dict["kampfcounter"] > 4:
                    turnierdatenbank_dict["kampfcounter"] = 0
                    turnierdatenbank_dict["kampfcounter"] = turnierdatenbank_dict["kampfcounter"] + 1
                    turnierdatenbank_dict["rundencounter"] = turnierdatenbank_dict["rundencounter"] + 1
                    turnierdatenbank_dict["rundenpunkte"] = turnierdatenbank_dict["rundenpunkte"] * 3
                    turnierdatenbank_dict["ringerindex"] = 0

                # sortiert Teilnehmerliste nach der ersten Runde für die korrekte Turnierlogik
                if turnierdatenbank_dict["rundencounter"] == 2 and turnierdatenbank_dict["kampfcounter"] == 1:
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(key=lambda x: x["turnierPunkte"])

                # sortiert Teilnehmerliste nach der zweiten Runde für die korrekte Turnierlogik
                if turnierdatenbank_dict["rundencounter"] == 3 and turnierdatenbank_dict["kampfcounter"] == 1:
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(
                        key=lambda x: runde3sortierung.index(x["turnierPunkte"]))

                if turnierdatenbank_dict["kampfcounter"] <= 4:
                    # index passt sich erst nach dem 1. Kampf je Runde an (beim 1. Kampf werden die zurückgesetzten
                    # Variabeln verwendet)
                    if turnierdatenbank_dict["kampfcounter"] > 1:
                        turnierdatenbank_dict["ringerindex"] = turnierdatenbank_dict["ringerindex"] + 2
                    ringerrot = \
                        turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                            "vornameNachname"]
                    ringerblau = \
                        turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][
                            turnierdatenbank_dict["ringerindex"] + 1][
                            "vornameNachname"] #ringerindex + 1 damit ich nicht zwei Variabeln (einmal für roten und einmal für blauen Ringer) brauche
                    turnierdatenbank_dict["kampfid"] = turnierdatenbank_dict["kampfid"] + 1

            #sind 3 Runden vorbei geht es zur Rangliste
            else:
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(
                    key=lambda x: endsortierung.index(x["turnierPunkte"]))

            #für laufende Anzeige der Kampfhistorie während der Kampfsimulation
            for element in turnierdatenbank_dict["kampfhistorie"]:
                kampfhistorie.append((element["kampfId"], element["ringerVNrot"], element["punkteRot"],
                                      element["ringerVNblau"], element["punkteBlau"], element["ringerRot"],
                                      element["ringerBlau"], element["sieger"]))

    if request.form.get("dateneintragen") == "daten eintragen": #wenn die Daten des aktuellen Kampfes eingetragen werden sollen
        buttoneintragen = False
        if int(request.form["punkterot"]) > int(request.form["punkteblau"]):
            print("Rot hat mehr Punkte",
                  turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                      "vornameNachname"])
            siegerfarbe = "rot"
            sieger = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                "ringerID"]
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                "turnierPunkte"] = \
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                    "turnierPunkte"] + turnierdatenbank_dict["rundenpunkte"]

        elif int(request.form["punkteblau"]) > int(request.form["punkterot"]):
            print("Blau hat mehr Punkte",
                  turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                      "vornameNachname"])
            siegerfarbe = "blau"
            sieger = \
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                    "ringerID"]
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                "turnierPunkte"] = \
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                    "turnierPunkte"] + turnierdatenbank_dict["rundenpunkte"]

        #bei Gleichstand wird ein zufälliger Sieger gewählt (Erklärung im readme)
        if request.form["punkterot"] == request.form["punkteblau"]:
            gleichstandssieger = randrange(0, 2)
            if gleichstandssieger == 0:
                siegerfarbe = "rot"
                sieger = \
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                        "ringerID"]
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                    "turnierPunkte"] = \
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                        "turnierPunkte"] + turnierdatenbank_dict["rundenpunkte"]
            elif gleichstandssieger == 1:
                siegerfarbe = "blau"
                sieger = \
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                        "ringerID"]
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                    "turnierPunkte"] = \
                    turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][
                        turnierdatenbank_dict["ringerindex"] + 1]["turnierPunkte"] + turnierdatenbank_dict[
                        "rundenpunkte"]

        turnierdatenbank_dict["kampfhistorie"].append(
            {"kampfId": turnierdatenbank_dict["kampfid"], "ringerBlau":
                turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                    "ringerID"], "ringerVNblau":
                 turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"] + 1][
                     "vornameNachname"],
             "ringerRot":
                 turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                     "ringerID"], "ringerVNrot":
                 turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][turnierdatenbank_dict["ringerindex"]][
                     "vornameNachname"],
             "punkteRot": int(request.form["punkterot"]), "punkteBlau": int(request.form["punkteblau"]),
             "sieger": sieger, "siegerfarbe": siegerfarbe})

        # für laufende Anzeige der Kampfhistorie während der Kampfsimulation
        for element in turnierdatenbank_dict["kampfhistorie"]:
            kampfhistorie.append((element["kampfId"], element["ringerVNrot"], element["punkteRot"],
                                  element["ringerVNblau"], element["punkteBlau"], element["ringerRot"],
                                  element["ringerBlau"], element["sieger"]))

        #Da es genau 12 Kämpfe sind wird mit dem 12 Kampf die Endsortierung vorgenommen
        if turnierdatenbank_dict["kampfid"] == 112:
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"].sort(
                key=lambda x: endsortierung.index(x["turnierPunkte"]))

    with open('ringerdatenbank.json', 'w') as r:
        json.dump(ringerdatenbank_dict, r, indent=4, separators=(',', ':'), sort_keys=True)
    with open('turnierdatenbank.json', 'w') as t:
        json.dump(turnierdatenbank_dict, t, indent=4, separators=(',', ':'))

    return render_template("matte1.html", buttoneintragen=buttoneintragen,
                           kampfhistorie=kampfhistorie, ringerrot=ringerrot, ringerblau=ringerblau,
                           runde=turnierdatenbank_dict["rundencounter"], kampfid=turnierdatenbank_dict["kampfid"])


@app.route("/rangliste", methods=["GET", "POST"])
def rangliste():
    r = open("ringerdatenbank.json")
    ringerdatenbank_dict = json.load(r)
    t = open("turnierdatenbank.json")
    turnierdatenbank_dict = json.load(t)
    rang = 0
    rangliste = []

    #holt die benötigten Daten des Teilnehmers(Turnierdatenbank) aus der Ringerdatenbank
    for teilnehmer in turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"]:
        for ringer in ringerdatenbank_dict:
            if teilnehmer["ringerID"] == ringer["ringerID"]:
                rang = rang + 1
                name = teilnehmer["vornameNachname"]
                nationalitaet = ringer["land"]
                punkte = turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"][0]["turnierPunkte"]
                rangliste.append((rang, name, nationalitaet, punkte))

    if request.method == "POST":
        if request.form.get("neustart") == "Datenbanken zurücksetzen":
            turnierdatenbank_dict["gewichtsklassen"][0]["teilnehmer"] = []
            turnierdatenbank_dict["gewichtsklassen"][0]["loszuteilung"] = [0,]
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



    return render_template("rangliste.html", rangliste=rangliste)


if __name__ == "__main__":
    app.run(debug=True, port=5000)