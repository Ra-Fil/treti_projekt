
## Scraper volebních výsledků

Scraper k získání volebních výsledků pro volby do Poslanecké sněmovny ČR v roce 2017 z webu https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.

## Instalace knihoven

Potřebné knihovny jsou vypsané v souboru reqirements.txt, který je součástí projektu.
pip3 --version
pip3 install -r requirements.txt``

## Aktivace virtuálního prostředí

.\venv\Scripts\Activate.ps1

## Použití

Projekt je nutné spouštět z příkazového řádku - spusťte skript se dvěma argumenty:
- První argument: URL územního celku (např. okres Benešov)
  Výběr okresu lze provádět na stránce `https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ` kliknutím na X ve sloupci "Výběr obce".
- Druhý argument: název výstupního souboru CSV

např:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"

## Výstup

Soubor CSV obsahuje:
- Kód obce
- Název obce
- Počet registrovaných voličů
- Počet vydaných obálek
- Počet platných hlasů
- Počet hlasů pro každou kandidující stranu