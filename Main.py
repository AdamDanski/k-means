import csv
import random

def odleglosc(punkt, centroid):
    return sum((a-b)**2 for a, b in zip(punkt, centroid))

def przypisz_do_centroidow(dane, centroidy):
    przypisania = []
    for punkt in dane:
        najmniejsza_odl = None
        najblizszy_cent = None

        for i in range(len(centroidy)):
            odl_do_centroid = odleglosc(punkt, centroidy[i])

            if najmniejsza_odl is None or odl_do_centroid < najmniejsza_odl:
                najmniejsza_odl = odl_do_centroid
                najblizszy_cent = i

        przypisania.append(najblizszy_cent)

    return przypisania

def policz_centroidy(dane, przypisania, k):
    liczba_cech=len(dane[0])
    nowe_centroidy = []
    licznik = []
    for i in range(k):
        centroid = []
        for j in range(liczba_cech):
            centroid.append(0.0)
        nowe_centroidy.append(centroid)
        licznik.append(0)
    for i in range(len(dane)):
        grupa = przypisania[i]
        licznik[grupa] += 1
        for j in range(liczba_cech):
            nowe_centroidy[grupa][j] += dane[i][j]
    for i in range(k):
        if licznik[i] > 0:
            for j in range(liczba_cech):
                nowe_centroidy[i][j] /= licznik[i]

    return nowe_centroidy

def wczytaj_dane(nazwa_pliku):
    dane = []
    with open(nazwa_pliku, 'r') as plik:
        reader = csv.reader(plik)
        for row in reader:
            dane.append([float(x) for x in row[:-1]])
    return dane

def czy_nowy_centroid(stare, nowe):
    for i in range(len(stare)):
        for j in range(len(stare[i])):
            if stare[i][j] != nowe[i][j]:
                return True
    return False

def suma_kwadratow(dane, przypisania, centroidy):
    suma = 0.0
    for i in range(len(dane)):
        grupa = przypisania[i]
        suma += odleglosc(dane[i], centroidy[grupa])
    return suma


def main():
    plik_csv = "iris.csv"  # nazwa pliku
    k = 4  # liczba grup

    dane = wczytaj_dane(plik_csv)
    print("wczytano ", len(dane), " punktów")
    print("pierwsze 3 dane: ", dane[:3])

    centroidy = random.sample(dane, k)
    for i, c in enumerate(centroidy):
        print(f"Centroid {i + 1}: {c}")

    licznik_iter = 0

    while True:
        przypisania = przypisz_do_centroidow(dane, centroidy)
        nowe_centroidy = policz_centroidy(dane, przypisania, k)
        suma = suma_kwadratow(dane, przypisania, nowe_centroidy)

        licznik_iter += 1
        print(f"Suma kwadratow: {suma}")

        grupy = [[] for _ in range(k)]
        for i in range(len(dane)):
            grupa = przypisania[i]
            grupy[grupa].append((i+1, dane[i]))

        if not czy_nowy_centroid(centroidy, nowe_centroidy):
            for i in range(k):
                print(f"Grupa: {i + 1} (centroid {nowe_centroidy[i]}):")
                for nr_punktu, punkt in grupy[i]:
                    print(f" - punkt {nr_punktu}: {punkt}")
            print("Koncymy dzialanie")
            break

        centroidy = nowe_centroidy



if __name__ == "__main__":
    main()