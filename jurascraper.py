#!/usr/bin/env python3
"""
Jurascraper – Version 3.0

Ein Open-Source-Tool zum automatisierten Herunterladen juristischer PDF-Dokumente von gesetze-im-internet.de.

Dieses Tool durchsucht systematisch die Teillisten A–Z und 0–9, filtert PDF-Links nach optionalen Kriterien
(Start, Enthalten, Ende des Dateinamens) und lädt sie in ein angegebenes Zielverzeichnis herunter.

© 2025 – MIT Lizenz
"""

# ——— Importierte Bibliotheken (Kern) ———
import os
import sys
import argparse
import subprocess
import importlib
import shutil
from urllib.parse import urljoin
from string import ascii_uppercase, digits
from concurrent.futures import ThreadPoolExecutor

# ——— Python-Version & automatische Modulinstallation ———
if sys.version_info < (3, 8):
    print("❌ Python 3.8 oder höher ist erforderlich. Deine Version:", sys.version)
    sys.exit(1)

REQUIRED_MODULES = ["requests", "bs4"]
for module in REQUIRED_MODULES:
    try:
        importlib.import_module(module)
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", module], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            # Automatische Installation fehlgeschlagen: Hinweise für manuelle Installation
            print("❌ Automatische Installation von '{}' fehlgeschlagen.".format(module))
            print("💡 Du kannst das Modul manuell installieren mit:")
            print("   pip install {}".format(module))
            sys.exit(1)

# ggf. automatisch mit 'python3' neu starten wenn nur 'python3' existiert
if shutil.which("python3") and not shutil.which("python") and not sys.executable.endswith("python3"):
    os.execv(shutil.which("python3"), ["python3"] + sys.argv)

# ——— Jetzt die restlichen Module importieren ———
import requests
from bs4 import BeautifulSoup

# ——— CLI-Argumente parsen ———
parser = argparse.ArgumentParser(
    description="PDF-Scraper für juristische Inhalte von gesetze-im-internet.de"
)
parser.add_argument("--output_dir", type=str, required=True, help="Zielverzeichnis für heruntergeladene PDFs")
parser.add_argument("--limit", type=int, default=0, help="Maximale Anzahl herunterzuladender PDFs (0 = unbegrenzt)")
parser.add_argument("--startswith", "-x", type=str, default="", help="Nur Dateien mit diesem Präfix im Dateinamen")
parser.add_argument("--contains", "-y", type=str, default="", help="Nur Dateien, die diesen Teilstring enthalten")
parser.add_argument("--endswith", "-z", type=str, default="", help="Nur Dateien mit diesem Suffix")
parser.add_argument("--preview", "-p", action="store_true", help="Nur Treffer anzeigen, aber nicht herunterladen")
parser.add_argument("--threads", type=int, default=1, help="Anzahl paralleler Downloads (Standard: 1). ⚠️ Nicht übertreiben – zu viele gleichzeitige Verbindungen können vom Server blockiert werden!")
args = parser.parse_args()

# ——— Verzeichnis vorbereiten ———
os.makedirs(args.output_dir, exist_ok=True)

# ——— Ziel-URLs generieren (Teillisten A-Z + 0–9) ———
TEILLISTEN = [f"https://www.gesetze-im-internet.de/Teilliste_{c}.html" for c in ascii_uppercase + digits]

# ——— PDF-Links sammeln ———
print("\U0001f4e1 Durchsuche Teillisten auf PDF-Links...")
pdf_links = []

for url in TEILLISTEN:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                full_url = urljoin(url, href)
                pdf_links.append(full_url)
    except Exception as e:
        print(f"❌ Fehler beim Laden von {url}: {e}")

print(f"\n🔍 Gefunden: {len(pdf_links)} PDF-Links insgesamt")

# ——— Filter anwenden ———
filtered_links = []
for link in pdf_links:
    name = os.path.basename(link).lower()
    if args.startswith and not name.startswith(args.startswith.lower()):
        continue
    if args.contains and args.contains.lower() not in name:
        continue
    if args.endswith and not name.endswith(args.endswith.lower()):
        continue
    filtered_links.append(link)

print(f"✅ Nach Filterung: {len(filtered_links)} passende Links")

# ——— Vorschau-Modus ———
if args.preview:
    print("\n📝 Vorschau-Modus aktiviert. Diese Dateien würden gespeichert werden:")
    for link in filtered_links:
        print("➡️", os.path.basename(link))
    sys.exit(0)

# ——— Download-Funktion ———
def download(link):
    global count
    filename = os.path.basename(link)
    filepath = os.path.join(args.output_dir, filename)

    if os.path.exists(filepath):
        print(f"⚠️ Datei existiert bereits: {filename}")
        return

    try:
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Gespeichert: {filename}")
    except Exception as e:
        print(f"❌ Fehler bei {filename}: {e}")

# ——— Paralleles Herunterladen ———
count = 0
print(f"\n⬇️ Starte Download mit {args.threads} Thread(s)...")

if args.limit:
    filtered_links = filtered_links[:args.limit]

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    executor.map(download, filtered_links)

# ——— (Kommendes Feature) Asynchrone Download-Logik mit asyncio ———
# Hinweis: Dieses Feature ist für zukünftige Versionen vorgesehen.
# Es ermöglicht effizientere Downloads bei sehr vielen kleinen Dateien und reduziert Ressourcenverbrauch.
#
# import aiohttp
# import asyncio
#
# async def async_download(session, url, output_path):
#     async with session.get(url) as resp:
#         if resp.status == 200:
#             with open(output_path, 'wb') as f:
#                 f.write(await resp.read())
#
# async def async_main(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in urls:
#             path = os.path.join(args.output_dir, os.path.basename(url))
#             tasks.append(async_download(session, url, path))
#         await asyncio.gather(*tasks)
#
# asyncio.run(async_main(filtered_links))

# ——— Abschlussmeldung ———
print(f"\n📄 Fertig: {len(filtered_links)} PDF-Dateien verarbeitet in '{args.output_dir}'")
