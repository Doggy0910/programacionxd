usuari_valid = "alumne"
contrasenya_valida = "python123"
max_intents = 3

saldo = 100.0
limit_retirada = 300.0
saldo_baix = 20.0

total_ingressat = 0.0
total_retirat = 0.0
operacions = 0
historial = []

print("---------------------------------")
print("     BANC - CAIXER")
print("---------------------------------")

intents = 0
acces = False

while intents < max_intents and not acces:

    usuari = input("Usuari: ")
    contrasenya = input("Contrasenya: ")
    intents += 1

    if usuari == usuari_valid and contrasenya == contrasenya_valida:
        acces = True
    else:
        print("Error: usuari o contrasenya incorrectes!")

        if intents < max_intents:
            print("Et queden", max_intents - intents, "intents")
        print("---------------------------------")

if not acces:
    print("Compte bloquejat per seguretat!")

else:
    print("")
    print("Benvingut/da,", usuari_valid, "!")

    sortir = False

    while not sortir:

        print("")
        print("-------- MENU PRINCIPAL --------")
        print("1. Consultar saldo")
        print("2. Ingressar diners")
        print("3. Retirar diners")
        print("4. Veure historial")
        print("5. Veure estadistiques")
        print("6. Sortir")

        opcio = input("Escull una opcio: ")

        if opcio == "1":
            print("Saldo actual:", round(saldo, 2), "EUR")

            if saldo < saldo_baix:
                print("Atencio: tens el saldo molt baix!")

        elif opcio == "2":
            text = input("Quanta quantitat vols ingressar? ")
            text = text.replace(",", ".")

            try:
                quantitat = float(text)
            except ValueError:
                quantitat = 0

            if quantitat <= 0:
                print("Error: la quantitat ha de ser un numero positiu!")
            else:
                saldo += quantitat
                total_ingressat += quantitat
                operacions += 1
                historial.append("Ingres: +" + str(round(quantitat, 2)) + " EUR")
                print("Has ingressat", round(quantitat, 2), "EUR")
                print("Nou saldo:", round(saldo, 2), "EUR")

        elif opcio == "3":
            text = input("Quanta quantitat vols retirar? ")
            text = text.replace(",", ".")

            try:
                quantitat = float(text)
            except ValueError:
                quantitat = 0

            if quantitat <= 0:
                print("Error: la quantitat ha de ser un numero positiu!")

            elif quantitat > saldo:
                print("Error: no tens prou saldo!")
                print("Saldo disponible:", round(saldo, 2), "EUR")

            elif total_retirat + quantitat > limit_retirada:
                print("Error: has superat el limit de retirada de la sessio")
                print("Encara pots retirar", round(limit_retirada - total_retirat, 2), "EUR")

            else:
                saldo -= quantitat
                total_retirat += quantitat
                operacions += 1
                historial.append("Retirada: -" + str(round(quantitat, 2)) + " EUR")
                print("Has retirat", round(quantitat, 2), "EUR")
                print("Nou saldo:", round(saldo, 2), "EUR")

                if saldo < saldo_baix:
                    print("Atencio: et queda poc saldo!")

        elif opcio == "4":
            print("-------- HISTORIAL --------")

            if len(historial) == 0:
                print("Encara no has fet cap moviment")
            else:
                numero = 1
                for moviment in historial:
                    print(numero, "-", moviment)
                    numero += 1

        elif opcio == "5":
            print("------- ESTADISTIQUES -------")
            print("Operacions fetes:", operacions)
            print("Total ingressat:", round(total_ingressat, 2), "EUR")
            print("Total retirat:", round(total_retirat, 2), "EUR")
            print("Saldo actual:", round(saldo, 2), "EUR")
            print("Limit de retirada que et queda:", round(limit_retirada - total_retirat, 2), "EUR")

        elif opcio == "6":
            sortir = True

        else:
            print("Opcio no valida, escull un numero del 1 al 6")

    print("")
    print("---------------------------------")
    print("Has fet", operacions, "operacions")
    print("Saldo final:", round(saldo, 2), "EUR")
    print("Gracies per confiar en nosaltres!")
    print("Fins aviat!")