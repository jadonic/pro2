import jinja2
import random
from flask import Flask
from flask import render_template
from flask import request

app = Flask("Hello World")

gewichtsklassen = {
    57: {

    },
    65: {

    },
    70: {

    },
    79: {

    },
    96: {

    },
    130: {

    }
}


@app.route("/hello", methods=["GET", "POST"])
def hello_post():
    # von https://stackoverflow.com/questions/19794695/flask-python-buttons
    if request.method == "POST":
        if request.form.get("eintragen") == "Eintragen":
            # global variables von hier: https://www.w3schools.com/python/python_variables_global.asp
            global vollername
            vollername = request.form["vollername"]
            gewicht = request.form["gewicht"]
            counter57 = 0
            counter65 = 0
            counter70 = 0
            counter79 = 0
            counter96 = 0
            counter130 = 0
            gesamtcounter = counter65 + counter70 + counter79 + counter96 + counter130
            if int(gewicht) <= 57 and counter57 <= 8:
                gewichtsklassen[57][vollername] = {}
                gewichtsklassen[57][vollername]["Gewicht"] = gewicht
                gewichtsklassen[57][vollername]["Name"] = vollername
            elif int(gewicht) <= 65 and counter65 <= 8:
                gewichtsklassen[65][vollername] = {}
                gewichtsklassen[65][vollername]["Gewicht"] = gewicht
            elif int(gewicht) <= 70 and counter70 <= 8:
                gewichtsklassen[70][vollername] = {}
                gewichtsklassen[70][vollername]["Gewicht"] = gewicht
            elif int(gewicht) <= 79 and counter79 <= 8:
                gewichtsklassen[79][vollername] = {}
                gewichtsklassen[79][vollername]["Gewicht"] = gewicht
            elif int(gewicht) <= 96 and counter96 <= 8:
                gewichtsklassen[96][vollername] = {}
                gewichtsklassen[96][vollername]["Gewicht"] = gewicht
            elif int(gewicht) <= 130 and counter130 <= 8:
                gewichtsklassen[130][vollername] = {}
                gewichtsklassen[130][vollername]["Gewicht"] = gewicht

            # Überprüfung, ob in jedem Gewicht schon 8 Ringer sind
            for i in gewichtsklassen[57]:
                counter57 = counter57 + 1
            for i in gewichtsklassen[65]:
                counter65 = counter65 + 1
            for i in gewichtsklassen[70]:
                counter70 = counter70 + 1
            for i in gewichtsklassen[79]:
                counter79 = counter79 + 1
            for i in gewichtsklassen[96]:
                counter96 = counter96 + 1
            for i in gewichtsklassen[130]:
                counter130 = counter130 + 1

            # Überprüfung, ob die Limite von 48 Ringern überschritten worden ist (6 Gewichtsklassen à 8 Teilnehmer)
            while gesamtcounter <= 48:
                return render_template("index.html")
            return gewichtsklassen
        elif request.form.get("gewichteanzeigen") == "Gewichte Anzeigen":
            return gewichtsklassen
    else:
        return render_template("index.html")


@app.route("/gewichterliste")
def gewichterliste():
    # idee, so zu machen von https://stackoverflow.com/questions/5750664/python-iterating-through-a-dictionary-gives-me-int-object-not-iterable
    return render_template("gewichterliste.html", gewichtsklassen57=gewichtsklassen[57],
                           gewichtsklassen65=gewichtsklassen[65], gewichtsklassen70=gewichtsklassen[70],
                           gewichtsklassen79=gewichtsklassen[79], gewichtsklassen96=gewichtsklassen[96],
                           gewichtsklassen130=gewichtsklassen[130])


@app.route("/matte1", methods=["GET", "POST"])
def matte1():
    index = 0
    indexodd = 1
    indexeven = 0
    activewrestler1 = ""
    activewrestler2 = ""
    if request.method == "POST":
        if request.form.get("kampfbeenden") == "Kampf beenden":
            indexodd = indexodd + 2
            indexeven = indexeven + 2
            print(indexeven, indexodd)
            for ringer in gewichtsklassen[57]:
                if indexeven == gewichtsklassen[57][ringer]["Startnummer"]:
                    activewrestler1 = gewichtsklassen[57][ringer]["Name"]
                elif indexodd == gewichtsklassen[57][ringer]["Startnummer"]:
                    activewrestler2 = gewichtsklassen[57][ringer]["Name"]

            print(activewrestler1, activewrestler2)
            return render_template("matte1.html", activewrestler1=activewrestler1, activewrestler2=activewrestler2)
    for gewicht in gewichtsklassen:
        for ringer in gewichtsklassen[gewicht]:
            gewichtsklassen[gewicht][ringer]["Startnummer"] = index
            index = index + 1
        index = 1
    print(gewichtsklassen[57])
    for ringer in gewichtsklassen[57]:
        if indexeven == gewichtsklassen[57][ringer]["Startnummer"]:
            activewrestler1 = gewichtsklassen[57][ringer]["Name"]
        elif indexodd == gewichtsklassen[57][ringer]["Startnummer"]:
            activewrestler2 = gewichtsklassen[57][ringer]["Name"]

    print(activewrestler1, activewrestler2)
    return render_template("matte1.html", activewrestler1=activewrestler1, activewrestler2=activewrestler2)


@app.route("/matte2")
def matte2():
    return render_template("matte2.html")


@app.route("/matte3")
def matte3():
    return render_template("matte3.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
