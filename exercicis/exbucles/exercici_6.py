n = int(input("Quants números vols introduir? "))
positius = 0
negatius = 0

for i in range(n):
    numero = float(input("Introdueix un número: "))
    if numero >= 0:
        positius += 1
    else:
        negatius += 1
print("Hi ha", positius, "numeros positius i", negatius, "numeros negatius")


