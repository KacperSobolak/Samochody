import csv
import requests
from bs4 import BeautifulSoup

index = 0

def get_dedails(link):
    global index
    index = index + 1
    print(index, link)
    response = requests.get(link)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    marka = None
    model = None
    rok_produkcji = None
    pojemnosc_silnika = None
    przebieg = None
    moc = None
    skrzynia_biegow = None
    kolor = None
    rodzaj_paliwa = None
    cena = None

    for el in soup.select(".techData table"):
        label = el.th.get_text().strip()
        value = el.td.get_text().strip()
        if value == "---":
            return None
        if label == "Marka":
            marka = value
        elif label == "Model":
            model = value
        elif label == "Pojemność silnika":
            pojemnosc_silnika = value
            pojemnosc_silnika = pojemnosc_silnika[:-1]
        elif label == "Rok produkcji":
            rok_produkcji = value
        elif label == "Moc silnika":
            moc = value
        elif label == "Rodzaj paliwa":
            rodzaj_paliwa = value
        elif label == "Skrzynia biegów":
            skrzynia_biegow = value
        elif label == "Kolor":
            kolor = value
    try:
        przebieg = soup.select("#wypos b")[0].get_text().strip()
        cena = soup.select(".presPrice span")[0].get_text().strip()
    except:
        return None
    if cena == "---" or przebieg == "---":
        return None
    return (marka, model, rok_produkcji, przebieg, pojemnosc_silnika, moc, rodzaj_paliwa, skrzynia_biegow, kolor, cena)

def get_page(s):
    URL = f"https://brzozowiak.pl/samochody-osobowe/?str={s}"
    return URL

with open("samochody.csv", "w") as csvfile:

    page_number = 129
    fieldnames = ["Marka", "Model", "Rok produkcji", "Przebieg", "Pojemnosc silnika", "Moc", "Rodzaj paliwa", "Skrzynia biegow" , "Kolor", "Cena"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for i in range(1, page_number + 1):
        URL = get_page(i)
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        for offer in soup.find_all("div", class_="rightCell"):
            href = offer.find("a", href=True)["href"]
            link = f"https://brzozowiak.pl{href}"
            results = get_dedails(link)
            if results != None:
                writer.writerow({
                    "Marka" : str(results[0]),
                    "Model" : str(results[1]),
                    "Rok produkcji" : int(results[2]),
                    "Przebieg" : int(results[3].rstrip("km").replace(" ", "")),
                    "Pojemnosc silnika" : int(results[4].rstrip("cm").replace(" ","")),
                    "Moc" : int(results[5].rstrip("KM").replace(" ","")),
                    "Rodzaj paliwa" : str(results[6]),
                    "Skrzynia biegow" : str(results[7]),
                    "Kolor" : str(results[8]),
                    "Cena" : int(results[9].replace(" ",""))
                })