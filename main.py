"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Radka Filipová
email: r.filipova@email.cz
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def ziskani_vstupu():
    """
    Získá a zkontroluje vstupní argumenty.
    """
    vstup = sys.argv
    if len(vstup) != 3:
        print("Chybné zadání. Ukončuji.")
        quit()
    if "https://www.volby.cz/pls/ps2017nss/" not in vstup[1]:
        print("První argument musí obsahovat adresu volby.cz. Ukončuji.")
        quit()
    if not vstup[2].endswith(".csv"):
        print("Druhý argument musí být .csv soubor. Ukončuji.")
        quit()
    return vstup

def seznam_obci(url):
    """
    Získá seznam obcí a odpovídajících odkazů na výsledky voleb.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = ["https://www.volby.cz/pls/ps2017nss/" + a["href"] for a in soup.select("td.cislo a")]
    obce = []
    for row in soup.select("table tr")[2:]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            kod = cols[0].text.strip()
            nazev = cols[1].text.strip()
            obce.append([kod, nazev])
    return obce, links

def ziskani_stran(url):
    """
    Získá seznam všech kandidujících stran.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    strany = [td.text.strip() for td in soup.select("td.overflow_name")]
    return strany

def ziskani_vysledku(url, vypis=False):
    """
    Získá volební výsledky pro jednu obec.
    Vrací list: [voliči, obálky, platné hlasy, ...hlasy pro každou stranu]
    """

    if vypis:
        print(f"Stahuji výsledek obce z: {url}")

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        volici = soup.find("td", headers="sa2").text.strip().replace('\xa0', '').replace(' ', '')
        obalky = soup.find("td", headers="sa3").text.strip().replace('\xa0', '').replace(' ', '')
        platne = soup.find("td", headers="sa6").text.strip().replace('\xa0', '').replace(' ', '')
    except:
        return ["0", "0", "0"] + []

    hlasy = []
    for td in soup.select("td[headers$='t1sb3'], [headers$='t2sb3']"):
        hlasy.append(td.text.strip().replace('\xa0', '').replace(' ', ''))
    return [volici, obalky, platne] + hlasy

def zapis_csv(data, vystup):
    """
    Uloží data do CSV souboru.
    """

    with open(vystup, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def hlavni():
    """
    Hlavní funkce programu.
    """

    vstup = ziskani_vstupu()
    obce, odkazy = seznam_obci(vstup[1])
    if not odkazy:
        print("Nenačteny žádné obce.")
        quit()

    hlavicka = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
    strany = ziskani_stran(odkazy[0])
    hlavicka.extend(strany)
    data = [hlavicka]

    print("Zpracovávám, bude to chvilku trvat...")

    for i, (obec, url) in enumerate(zip(obce, odkazy)):
        vypis = (i == 0)
        radek = obec + ziskani_vysledku(url, vypis=vypis)
        data.append(radek)

    zapis_csv(data, vstup[2])

    print(f"Uloženo do souboru: {vstup[2]}")
    print("Ukončuji election_scraper")

if __name__ == "__main__":
    hlavni()