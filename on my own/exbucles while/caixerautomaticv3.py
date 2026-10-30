def iniciar_sessio(usuari_correcte, contrasenya_correcta):
    max_intents = 3
    intents = 0
    acces = False

    while intents < max_intents and not acces:

        usuari = input("Usuari: ")
        contrasenya = input("Contrasenya: ") 
        intents += 1

        if usuari == usuari_correcte and contrasenya == contrasenya_correcta:
            acces = True
        else:
            print("Error: usuari o contrasenya incorrectes!")

            if intents < max_intents:
                print("Et queden", max_intents - intents, "intents")
            print("---------------------------------")

    return acces


def mostrar_menu():
    print("")
    print("-------- MENU PRINCIPAL --------")
    print("1. Consultar saldo")
    print("2. Ingressar diners")
    print("3. Retirar diners")
    print("4. Sortir")


def consultar_saldo(saldo):
    print("El teu saldo actual es de", round(saldo, 2), "EUR")


def ingressar_diners(saldo):
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
        print("Has ingressat", round(quantitat, 2), "EUR")
        print("Nou saldo:", round(saldo, 2), "EUR")

    return saldo


def retirar_diners(saldo):
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
    else:
        saldo -= quantitat
        print("Has retirat", round(quantitat, 2), "EUR")
        print("Nou saldo:", round(saldo, 2), "EUR")

    return saldo


print("---------------------------------")
print("     BANC - CAIXER")
print("---------------------------------")

acces = iniciar_sessio("alumne", "python123")

if not acces:
    print("Compte bloquejat per seguretat!")

else:
    saldo = 100.0
    sortir = False

    print("")
    print("Benvingut/da!")

    while not sortir:

        mostrar_menu()
        opcio = input("Escull una opcio: ")

        if opcio == "1":
            consultar_saldo(saldo)

        elif opcio == "2":
            saldo = ingressar_diners(saldo)

        elif opcio == "3":
            saldo = retirar_diners(saldo)

        elif opcio == "4":
            sortir = True

        else:
            print("Opcio no valida, escull un numero del 1 al 4")

    print("")
    print("---------------------------------")
    print("Saldo final:", round(saldo, 2), "EUR")
    print("Gracies per utilitzar el caixer!")
    print("Fins aviat!")