import random

def kolkoIkrzyzyk():
    plansza = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

    def wyswietlPlansze(mapa2D):
        print("  1 2 3")
        numerWiersza = 1
        for wiersz in mapa2D:
            print(numerWiersza, end=" ")
            for element in wiersz:
                print(element, end=" ")
            print()
            numerWiersza += 1

    def wygrana(mapa2D):
        for x in range(0, 3):
            if mapa2D[x][0] == mapa2D[x][1] and mapa2D[x][1] == mapa2D[x][2] and (
                    mapa2D[x][2] == "X" or mapa2D[x][2] == "O"):
                return True
        for y in range(0, 3):
            if mapa2D[0][y] == mapa2D[1][y] and mapa2D[1][y] == mapa2D[2][y] and (
                    mapa2D[2][y] == "X" or mapa2D[2][y] == "O"):
                return True
        if mapa2D[0][0] == mapa2D[1][1] and mapa2D[1][1] == mapa2D[2][2] and (
                mapa2D[2][2] == "X" or mapa2D[2][2] == "O"):
            return True
        if mapa2D[0][2] == mapa2D[1][1] and mapa2D[1][1] == mapa2D[2][0] and (
                mapa2D[2][0] == "X" or mapa2D[2][0] == "O"):
            return True

        return False

    def remis(mapa2D):
        if not wygrana(mapa2D):
            for wiersz in mapa2D:
                for element in wiersz:
                    if element == "*":
                        return False
            return True
        else:
            return False

    graKrzyzyk = False
    print("Najpierw podawaj wiersz a potem kolumnę.")
    pobrana = input("Jeżeli mają zacząć krzyżyki wpisz X, a jeżeli kółka wpisz O: ")
    if pobrana == "X":
        graKrzyzyk = True
        plansza = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

    while (not remis(plansza)) and (not wygrana(plansza)):
        wyswietlPlansze(plansza)
        x, y = [int(x) for x in input("Podaj współrzędne pola na którym chcesz postawić krzyżyk bądź kółko: ").split()]
        if plansza[x - 1][y - 1] == "*":
            if graKrzyzyk:
                plansza[x - 1][y - 1] = "X"
                graKrzyzyk = False
            else:
                plansza[x - 1][y - 1] = "O"
                graKrzyzyk = True

    wyswietlPlansze(plansza)

    if wygrana(plansza):
        if graKrzyzyk:
            print("Wygrał gracz grający kółkami! Gratulujemy!")
        else:
            print("Wygrał gracz grający krzyżykami! Gratulujemy!")
    else:
        print("Nastąpił remis.")


def kolkoIkrzyzyk1():
    planszaTimer = 0
    plansza = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

    def wyswietlPlansze(mapa2D):
        print("  1 2 3")
        numerWiersza = 1
        for wiersz in mapa2D:
            print(numerWiersza, end=" ")
            for element in wiersz:
                print(element, end=" ")
            print()
            numerWiersza += 1

    def wygrana(mapa2D):
        for x in range(0, 3):
            if mapa2D[x][0] == mapa2D[x][1] and mapa2D[x][1] == mapa2D[x][2] and (
                    mapa2D[x][2] == "X" or mapa2D[x][2] == "O"):
                return True
        for y in range(0, 3):
            if mapa2D[0][y] == mapa2D[1][y] and mapa2D[1][y] == mapa2D[2][y] and (
                    mapa2D[2][y] == "X" or mapa2D[2][y] == "O"):
                return True
        if mapa2D[0][0] == mapa2D[1][1] and mapa2D[1][1] == mapa2D[2][2] and (
                mapa2D[2][2] == "X" or mapa2D[2][2] == "O"):
            return True
        if mapa2D[0][2] == mapa2D[1][1] and mapa2D[1][1] == mapa2D[2][0] and (
                mapa2D[2][0] == "X" or mapa2D[2][0] == "O"):
            return True

        return False

    def remis(mapa2D):
        if not wygrana(mapa2D):
            for wiersz in mapa2D:
                for element in wiersz:
                    if element == "*":
                        return False
            return True
        else:
            return False

    if planszaTimer == 0:
        wyswietlPlansze(plansza)
        graKrzyzyk = True
        graKolko = False
        ktoGraKIK1 = False
        print("Najpierw podawaj wiersz a potem kolumnę")
        ktoGraKIK = input("Jeżeli chcesz być krzyżykiem wpisz X, a jeżeli kółkiem wpisz O: ")
        if ktoGraKIK == "O":
            ktoGraKIK1 == False
        else:
            ktoGraKIK1 = True

    if ktoGraKIK1 == True:
        while (not remis(plansza)) and (not wygrana(plansza)):
            AIx = random.randint(0, 3)
            AIy = random.randint(0, 3)
            if graKrzyzyk == True:
                x, y = [int(x) for x in input("Podaj współrzędne pola na którym chcesz postawić krzyżyk: ").split()]
                if plansza[x - 1][y - 1] == "*":
                    plansza[x - 1][y - 1] = "X"
                    wyswietlPlansze(plansza)
                    graKrzyzyk = False

            if graKrzyzyk == False:
                if planszaTimer == 1:
                    wyswietlPlansze(plansza)
                if plansza[AIx - 1][AIy - 1] == "*":
                    plansza[AIx - 1][AIy - 1] = "O"
                    print("-----------------------------------------------------------------------------")
                    wyswietlPlansze(plansza)
                    graKrzyzyk = True
                else:
                    while plansza[AIx - 1][AIy - 1] == "*":
                        AIx = random.randint(0, 3)
                        AIy = random.randint(0, 3)
                        if plansza[AIx - 1][AIy - 1] == "*":
                            plansza[AIx - 1][AIy - 1] = "O"
                            print("-----------------------------------------------------------------------------")
                            wyswietlPlansze(plansza)
                            graKrzyzyk = True

    if ktoGraKIK1 == False:
        while (not remis(plansza)) and (not wygrana(plansza)):
            AIx = random.randint(0, 3)
            AIy = random.randint(0, 3)
            if graKolko == False:
                x, y = [int(x) for x in input("Podaj współrzędne pola na którym chcesz postawić kółko: ").split()]
                if plansza[x - 1][y - 1] == "*":
                    plansza[x - 1][y - 1] = "O"
                    wyswietlPlansze(plansza)
                    graKolko = True

            if graKolko == True:
                if planszaTimer == 1:
                    wyswietlPlansze(plansza)
                if plansza[AIx - 1][AIy - 1] == "*":
                    plansza[AIx - 1][AIy - 1] = "X"
                    print("-----------------------------------------------------------------------------")
                    wyswietlPlansze(plansza)
                    graKolko = False
                else:
                    while plansza[AIx - 1][AIy - 1] == "*":
                        AIx = random.randint(0, 3)
                        AIy = random.randint(0, 3)
                        if plansza[AIx - 1][AIy - 1] == "*":
                            plansza[AIx - 1][AIy - 1] = "X"
                            print("-----------------------------------------------------------------------------")
                            wyswietlPlansze(plansza)
                            graKolko = False

    if wygrana(plansza):
        if graKolko:
            print("Wygrał gracz grający kółkami! Gratulujemy!")
        else:
            print("Wygrał gracz grający krzyżykami! Gratulujemy!")
    else:
        print("Nastąpił remis.")

    planszaTimer = 1

wybor = int(input("Wpisz 1 jeśli chcesz grać z innym graczem lub 2 jeśli chcesz grać z komputerem: "))
if wybor == 1:
    kolkoIkrzyzyk()
elif wybor == 2:
    kolkoIkrzyzyk1()
