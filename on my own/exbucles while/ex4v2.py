
import random

tornar_a_jugar = "s"
partides = 0
victories = 0
millor_puntuacio = 0

while tornar_a_jugar == "s":

    numeropy = random.randint(1, 100)
    intents = 0
    trobat = False

    print("-----------------------------------")
    print("----- JOC DE TROBAR UN NUMERO -----")
    print("-----------------------------------")
    print("He escollit un nombre entre 1 i 100")

    print("Dificultats:")
    print("1. Facil (10 intents)")
    print("2. Mitja (7 intents)")
    print("3. Dificil (5 intents)")

    dificultat = input("Escull la dificultat: ")

    if dificultat == "1":
        max_intents = 10
    elif dificultat == "3":
        max_intents = 5
    else:
        max_intents = 7

    print("Tens", max_intents, "intents per trobar-lo")

    while intents < max_intents and not trobat:

        numero = int(input("Endevina el numero: "))
        intents += 1

        if numero < numeropy:
            print("El nombre ha de ser mes gran!")

        elif numero > numeropy:
            print("El nombre ha de ser mes petit!")

        else:
            trobat = True
            victories += 1
            print("L'has trobat en", intents, "intents!")

            punts = (max_intents - intents + 1) * 10
            print("Has aconseguit", punts, "punts")

            if punts > millor_puntuacio:
                millor_puntuacio = punts
                print("Has fet un nou record!")

        if not trobat:
            diferencia = abs(numero - numeropy)

            if diferencia <= 5:
                print("Estas molt a prop!")
            elif diferencia <= 15:
                print("Estas a prop!")
            else:
                print("Estas lluny!")

            print("Et queden", max_intents - intents, "intents")

    if not trobat:
        print("Has perdut! El numero era", numeropy)

    partides += 1

    print("--------- ESTADISTIQUES ---------")
    print("Partides jugades:", partides)
    print("Partides guanyades:", victories)
    print("Partides perdudes:", partides - victories)
    print("Millor puntuacio:", millor_puntuacio)

    tornar_a_jugar = input("Vols tornar a jugar? (s/n): ")

    while tornar_a_jugar != "s" and tornar_a_jugar != "n":
        tornar_a_jugar = input("Escriu s o n: ")

print("-----------------------------------")
print("Gracies per jugar")
print("Has guanyat", victories, "de", partides, "partides")
print("Fins aviat!")
