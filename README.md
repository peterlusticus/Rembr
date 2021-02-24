# Rembr

###### RaspberryPi CNC embroidery library

## Unser Projekt

Wir wollen den PC einer alten Fortron-Stickmaschine mit einem RaspberryPi 4 ersetzen.

## Ablauf

####  Usersicht

1.  SVG-Datei auf einen bestimmten Stick spielen und an den Raspberry stecken.
2.  Die Datei totalPrint.py ausführen

####  Entwicklersicht

1.  Beim ausführen der totalPrint.py, wird das SVG in einzelne Farben aufgesplittet, sodass auf dem Stick nun einzelne SVG-Dateien der verschiedenen Farben liegen
2.  Die einzelnen SVG-Dateien werden in einzelne G-GCODE-Dateien mithilfe der inkstitch-Library umgewandelt
3.  Nun wird nacheinander jede Farbe gestickt \[print()\]:
    1.  Die Farbe wird gewechselt \[changecolor()\]
    2.  Die G-CODE-Dateien werden ausgeführt \[cnc()\]
        1.  Währenddessen wird der Stickvorgang gestartet \[embroiderystart()\]
        2.  Sobald der G-CODE durchgelaufen ist, wird der Stickvorgang beendet \[embroiderystop()\]
        3.  Und der Faden abgeschnitten \[cut()\]

## Todo

*    [ ]  Methoden: embroideryStart()  embroideryStop()  changeColor()
*    [ ]  Architektur: Zusammenführung von changecolor.py und print.py; jj
*    [ ]  Fehlerbehebung: Paralleles ausführen von Methoden um schräg zu sticken; jj
