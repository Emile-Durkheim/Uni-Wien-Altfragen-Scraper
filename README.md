# Uni Wien Altfragen Scraper

### Requirements:

Python 3 (Microsoft store)
`pip install selenium` in Kommandozeile
Ausführen: src/AltfragenScraper/main.py

### Funktionsweise:

Der Altfragen Scraper öffnet ein Fenster, über welches ein Browser geöffnet wird. In diesem Browser kann die Online Prüfung problemlos geschrieben werden. Der Altfragen Scraper speichert sich die Fragen und Antworten.
Sobald die Prüfung fertig ist, lassen sich alle Fragen + Antworten als .txt oder .docx (Word) Datei exportieren.

### Limitationen:

Der Altfragen Scraper funktioniert ausschließlich mit multiple choice Prüfungen. Sind non-multiple-choice Prüfungen gegeben, ist das Verhalten des Programms undefiniert. Der Browser wird nie während der Prüfung abstürzen, aber es ist möglich, dass *neue* Fragen/Antworten nicht mehr aufgezeichnet werden, wenn eine non-multiple-choice Frage gefunden wird.
