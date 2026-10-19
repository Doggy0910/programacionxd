pes = float(input("Introdueix el pes en kg: "))
alcada = float(input("Introdueix l'alçada en metres: "))

imc = pes / (alcada ** 2)

print("El teu IMC és", imc)

if imc < 18.5:
    print("Diagnòstic: baix pes")
elif imc < 25:
    print("Diagnòstic: pes normal")
elif imc < 30:
    print("Diagnòstic: sobrepès")
else:
    print("Diagnòstic: obesitat")