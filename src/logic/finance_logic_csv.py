import csv

# Stałe do identyfikacji kolumn
POZYCJA_INDEX = 0
POZYCJA_NR_ALBUMU = 3
POZYCJA_ZAPLACONE = 4

# Ścieżki do plików
LOKALIZACJA_PLIKU_CSV = r'C:\Developer\Python\BankSS\bank.csv'
LOKALIZACJA_PLIKU_TXT = r'C:\Developer\Python\BankSS\Wpłaty 19.03.24.pdf'


def wczytaj_csv(sciezka):
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        return list(csv.reader(plik, delimiter=';'))


def zapisz_csv(sciezka, dane):
    with open(sciezka, mode='w', newline='', encoding='utf-8') as plik:
        pisarz_csv = csv.writer(plik, delimiter=';')
        pisarz_csv.writerows(dane)


# Funkcja do wyszukiwania numeru albumu w pliku txt
def znajdz_w_pliku_txt(sciezka, szukany_numer):
    with open(sciezka, 'r', encoding='latin-1', errors='ignore') as fp:
        # Wyszukuje numer albumu w pliku txt
        for numer_linii, linia in enumerate(fp, 1):
            if szukany_numer in linia:
                return numer_linii
    return None


def aktualizuj_dane(dane_csv):
    liczbaZnalezionych = 0

    for wiersz in dane_csv:
        if wiersz[POZYCJA_INDEX].strip('.') and wiersz[POZYCJA_NR_ALBUMU] != "brak" and wiersz[
            POZYCJA_NR_ALBUMU] != "Nr albumu" and wiersz[POZYCJA_NR_ALBUMU] != '':
            numer_albumu = wiersz[POZYCJA_NR_ALBUMU]
            numer_linii = znajdz_w_pliku_txt(LOKALIZACJA_PLIKU_TXT, numer_albumu)
            if numer_linii:
                liczbaZnalezionych += 1
                print(f"Numer albumu: {numer_albumu} istnieje w pliku.")
                print('Zawartość komórki:', wiersz[POZYCJA_NR_ALBUMU])
                print('Numer linii:', numer_linii)
                wiersz[POZYCJA_ZAPLACONE] = 'Tak'

    print(f"Znaleziono {liczbaZnalezionych} studentów.")


def finance_logic_function():
    try:
        dane_csv = wczytaj_csv(LOKALIZACJA_PLIKU_CSV)
        aktualizuj_dane(dane_csv)
        zapisz_csv(LOKALIZACJA_PLIKU_CSV, dane_csv)

    except FileNotFoundError:
        print("Plik 'lista.csv' nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    finance_logic_function()
