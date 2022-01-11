# PROG-2 Projekt Nicolas Steiger

Als mein PROG-2 Projekt simuliere ich ein Ringerturnier. Um es möglichst einfach zu halten besteht das Ringerturnier aus lediglich einer Gewichtsklasse. Wie an internationalen Turnieren üblich besteht eine Gewichtsklasse aus acht Teilnehmern.

## Teilnehmer erfassen

Als erstes wird ein neuer Teilnehmer angelegt. Dies kann man über die angezeigten Inputfelder, wobei wichtig ist, dass sämtliche Felder ausgefüllt werden. Mit dem Button "Eintragen" wird der Teilnehmer eingetragen. Wenn man möchte, kann man auch einen zufälligen Ringer generieren. Dieser wird aus einer Auswahl von 20 Vornamen, 20 Nachnamen, 20 Ländern und 10 Gewichten zufällig zusammengesetzt.

Bei der Eintragung wird automatisch ein zufälliges Los zwischen 1 und 99 zugeteilt. Dieser Vorgang simuliert die Losziehung während der Abwaage bei einem realen Turnier. Das Los dient (wie bei einem echten Turnier) als Grundlage für die erste Kampfeinteilung. 

Für das Beginnen der Kampfsimulation **müssen** acht Teilnehmer erfasst werden. Vor der Kampfsimulation kann die Teilnehmerliste bei Bedarf gelöscht und neu erstellt werden.

## Kampfsimulation
Das Turnier funktioniert im Poolsystem. Die Gewinner der 1. Runde landen im Gewinner- und die Verlierer der 1. Runde landen im Verliererpool. Ein Gewinner der 2. Runde muss gegen den anderen Gewinner des entsprechenden Pools kämpfen. Bei den Verlierern der 2. Runde dasselbe. Nach der Austragung der Kämpfe in der 3. Runde steht die Reihenfolge und somit die Rangliste bereits fest.

![Screenshot Turnierlogik](/assets/images/ScreenshotTurnierlogik.jpg)

### Regeln 
Bei einem Ringerkampf gewinnt der Teilnehmer, der nach Ablauf der Zeit mehr Punkte hat, oder es während dem Kampf schafft, 15 Punkte unterschied zum Gegner aufzubauen (z.B. 15:0 oder 18:3). In der Praxis geht ein einzelner Punktestand selten bis gar nie über 30 Punkte, deshalb wurde im Programm diese Punktelimite gesetzt.

In der Simulation können wir also die jeweiligen Punkte der Ringer und damit den Sieger eines Kampfes erfassen. Ob der Kampf während der Kampfzeit oder mit Ablauf dessen beendet wurde ist dabei irrelevant. 

#### Gleichstand
Obwohl eher selten, kann es vorkommen, dass ein Kampf mit der gleichen Punktzahl beendet wird. In der Praxis kommen in diesem Fall verschiedene Regeln zum Zug:
* Anzahl Strafpunkte
* Höhe der einzelnen Wertungen
* wer den letzen Punkt gemacht hat

**Es gibt also IMMER einen Sieger.** In der Kampfsimulation wird bei einem Gleichstand deshalb ein zufälliger Sieger ausgewählt.

## Rangliste und Neustart
Die Rangliste ist relativ selbsterklärend. Die Ringer werden anhand ihrer Punktzahl aufsteigend sortiert und in der Liste eingeordnet. 

Bei Bedarf hat man die Möglichkeit, sämtliche Datenbanken zurückzusetzen und anschliessend das Ringerturnier neu zu starten.

## Json Ringerdatenbank und Turnierdatenbank
### Ringerdatenbank
Die Ringerdatenbank ist so aufgebaut, dass  sie einerseits die Grundinformationen über einen Ringer speichert, sowie die Daten an Turnieren, die er gewesen ist. 

#### Grundinformationen

* ringerID
* vorname
* nachname
* land

#### Turnierdaten

* gewicht
* gewichtsklasse
* losnummer

Diese Datenbank wurde bewusst so simpel gehalten, mit dem Hintergrund, dass Sie jederzeit ausgebaut werden kann, falls weiter am Projekt gearbeitet werden würde.

### Turnierdatenbank
Die Turnierdatenbank ist eine Temporäre Datenbank, welche das jeweils laufende Turnier abbildet. In dieser Datenbank sind einerseits Grundinformationen über das Turnier vorhanden

* Turniername
* Gewichtsklassen
* Kampfhistorie

und andererseits Werte, welche für die Kampflogik abgespeichert werden müssen:

* ringerindex
* rundencounter
* kampfcounter
* rundenpunkte
* kampfid

Diese Datenbank wurde mit der Aussicht konzipiert, dass bei einer Funktionserweiterung statt nur ein Turnier mehrere Turniere in einer Art "Turnierverlauf" gespeichert werden können.