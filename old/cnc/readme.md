## Rembr/CNC

### Dateien:

#### prepare.py

*   Klasse, um die einzelnen G-CODE-Dateien aus dem SVG zu erzeugen
*   Todo: Inkstitch anbinden, SVG-Datei splitten

#### print.py

*   Klasse, die als G-CODE-Interpreter dient
*   Sie führt den G-CODE auf einem 2-Achsen-Tisch aus
*   Der G-CODE muss das Format...

```g-code
G1 X121.3025 Y-73.6630
G1 X121.3597 Y-73.7080
G1 X121.4547 Y-73.7786
G1 X121.4150 Y-73.8223
G1 X121.3160 Y-73.9364
```

        ...haben

*   Todo: Beide Achsen gleichzeitig ansteuern, damit schräge Bewegungen ausgeführt werden können.

#### test.txt

*   G-CODE Testdatei (Kaktus)
