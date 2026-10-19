x = int(input("Introdueix un numero"))
y = int(input("Introdueix un altre numero"))
operacio = input("Introdueix la operacio que vols utilitzar (+,-,* o /)")
if operacio == "+":
    resultat = x + y
    print("Resultat", resultat)
elif operacio == "-":
    resultat = x - y
    print("Resultat", resultat)
elif operacio == "*":
    resultat = x*y
    print("Resultat", resultat)
elif operacio == "/":
    resultat = x/y
    print("Resultat", resultat)
else: print("Input no valid")

