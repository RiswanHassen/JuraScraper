# Jurascraper – Version 3.0

Jurascraper ist ein vollautomatischer PDF-Scraper für das deutsche Gesetzesportal [gesetze-im-internet.de](https://www.gesetze-im-internet.de), bereit für den produktiven Einsatz und juristische Datenverarbeitung.

## 🚀 Funktionen

- Durchsucht systematisch alle Teillisten (A–Z und 0–9)
- Filtert PDF-Dateien nach Präfix, Substring und Suffix
- Unterstützt parallele Downloads via `--threads`
- Vorschau-Modus zur Anzeige potenzieller Treffer (`--preview`)
- Vollautomatische Installation fehlender Python-Module inkl. PEP-668-Kompatibilität
- Robust, restartfähig und kompatibel mit `python3`

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/dein-user/jurascraper.git
cd jurascraper

# (Optional) Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Starten
python3 jurascraper.py --output_dir ./downloads --limit 20 --contains schul
```

## ⚙️ Optionen

```bash
--output_dir     Zielverzeichnis (Pflicht)
--limit          Maximale Anzahl an Downloads (0 = alle)
--startswith/-x  Nur PDFs mit diesem Präfix im Dateinamen
--contains/-y    Nur PDFs, die diesen String enthalten
--endswith/-z    Nur PDFs mit diesem Suffix
--preview/-p     Nur Treffer anzeigen, nicht herunterladen
--threads        Anzahl paralleler Downloads (Standard: 1)
```

## 🔒 Hinweis zu `--threads`
> Mehrere gleichzeitige Downloads erhöhen die Last auf dem Server. Bitte mit Bedacht einsetzen (z. B. `--threads 2` bis `--threads 4`). Zu viele parallele Anfragen können blockiert werden.

## 🧠 Beispiel

Nur Schulgesetze anzeigen, aber nicht herunterladen:
```bash
python3 jurascraper.py --output_dir ./test -y schul -p
```

PDFs, die mit "B" beginnen und "2023.pdf" enden, herunterladen (max. 10):
```bash
python3 jurascraper.py --output_dir ./test -x B -z 2023.pdf --limit 10
```

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz – siehe [LICENSE](./LICENSE).

## ✨ Autor

Riswan Hassen – 2025

Für Feedback, Forks und PRs: [github.com/dein-user](https://github.com/dein-user)
