# PoincareDisk
Part of my Bachelor Thesis. Processing programm for hyperbolic Geometrie on the Poincare Disk , inspired from Geogebra.

Instructions
GERMAN:

Das Programm operiert über einem Layer System welche mit den Zahlen Button (Rechts oben) oder Tastatur ausgewählt werden kann.
Diese Layer System fungiert um gezeilt Figuren auszuwählen um diese transformieren. Es können auch mehr als 10 Layer benutzt werden diese müssen allerding über die Tastatur wingaben ausgewählt werden.

Sämtliche Iformationen für den Benutzer sowie die Eingaben des Benutzers werden unten rechts in einer Textbox Ausgegeben.
Eingaben können mit den Tastendruck ENTER abgegeben werden.

Oben links befinden sich die Werkzeug Buttons , dessen Funktionen in folgendem von Oben nach unten Reihenweise von links nach rechts erläutert werden:

- Geraden Werkzeug
  Dieses Werzeug erzeug nach Wahl von zwei Punkten auf der Kreisscheibe , über der Maus, die passende Hyberbolische Gerade auf dem ausgewählten Layer.

- Strecken Werkzeug
  Dieses Werzeug erzeug nach Wahl von zwei Punkten auf der Kreisscheibe , über der Maus, die passende Hyberbolische Strecke auf dem ausgewählten Layer.

- Spiegel Werkzeug
  Bei Wahl dieses Werkzeuges müssen zuerst zwei Layer ausgewählt werden, der erste ausgewählte Layer wird folgend über den zweiten ausgewählten Layer gespiegelt.
  Die Spieglung wird auf den nächsten freien Layer gespeichert.

- Translations Werkzeug
- Dieses Werzeug erzeug nach Wahl von zwei Punkten auf der Kreisscheibe, über der Maus, den passenden svektor und transliert den ausgewählten Layer um diese Richtung.
  Die Transaltion wird auf den nächsten Layer gespeichert.

- Rotations Werkzeug ( kein Button erscheint an dieser Position)
  nicht implementiert

- gleichseitiges n-eck Werkzeug
  Bei Wahl dieses Werkzeuges müssen zuerst die Anzahl Kanten ausgewählt werden ( Über den Zahlen Button oder der Tastatur).
  Dannach muss ein Radius angegeben werden ( Über zwei Punkten auf der Kreisscheibe oder über der Tastatur[Punktschreibweise für Kommazahlen]).
  Folgend wird auf den nächsten freien Layer die passende gleichseitge n-eck Figur gezeichnet.

- Parkettierungs Werkzeug
  Bei Wahl dieses Werkzeuges müssen zuerst die Anzahl an Rekursionen ausgewählt werden. Dannach muss der gewünschte Layer ausgewählt werden.
  Folgend wird eine Parkettierung der Kreischeibe bis zur Rekursionanzahl gestartet. Jede einzelze resultierende Figur wird auf seinen nächsten freien layer      gespeichert (Bei Figuren mit vielen Geraden/Kanten kann bereits eine Rekursionanzahl von 4 oder mehr dauern!)

- Auswahl Werkzeug
 Bei Wahl dieses Werkzeuges muss ein Layer ausgewählt werden, folgend werden nur die Geraden/Strecke dargestellt welche sich auf diesem Layer befinden.

- Screenshot Werkzeug
  Bei Aushwal dieses Werkzeug wird direkt ein Bild der Kreisscheibe ohne Benutzeroberfläche im Verzeichnis Ornder hinterlegt.

- Lösch Werkzeug
- Bei Wahl dieses Werkzeuges muss ein Layer ausgewählt werden, folgend werden die Geraden/Strecke entfernt welche sich auf diesen Layer befinden.
  Sollte das Werkzeug 2 mal hintereinander ausgewählt werden , so werden die Inhalte alle Layer gelöscht.
