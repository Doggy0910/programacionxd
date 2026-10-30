usuari_valid = "alumne"
contrasenya_valida = "python123"
max_intents = 3
saldo = 100.0

print("----- CAIXER AUTOMATIC -----")

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

if not acces:
    print("Compte bloquejat per seguretat")

else:
    print("Benvingut/da!")

    sortir = False

    while not sortir:

        print("----- MENU -----")
        print("1. Consultar saldo")
        print("2. Ingressar diners")
        print("3. Retirar diners")
        print("4. Sortir")

        opcio = int(input("Escull una opcio: "))

        if opcio == 1:
            print("El teu saldo es de", round(saldo, 2), "EUR")

        elif opcio == 2:
            quantitat = float(input("Quant vols ingressar? "))

            if quantitat > 0:
                saldo += quantitat
                print("Ingres fet! Nou saldo:", round(saldo, 2), "EUR")
            else:
                print("Error: la quantitat ha de ser positiva!")

        elif opcio == 3:
            quantitat = float(input("Quant vols retirar? "))

            if quantitat <= 0:
                print("Error: la quantitat ha de ser positiva!")
            elif quantitat > saldo:
                print("Error: no tens prou saldo!")
            else:
                saldo -= quantitat
                print("Retirada feta! Nou saldo:", round(saldo, 2), "EUR")

        elif opcio == 4:
            sortir = True

        else:
            print("Opcio no valida!")

    print("Gracies per utilitzar el caixer!")
    print("Fins aviat!")