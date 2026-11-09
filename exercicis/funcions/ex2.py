def convertir_divisa(quantitat, moneda):

    if moneda == "Yens":
        comissio = 0.07
        canvi = 177

    elif moneda == "Lliures":
        comissio = 0.02
        canvi = 0.85

    elif moneda == "Dolars":
        comissio = 0.035
        canvi = 1.08

    euros_nets = quantitat - (quantitat * comissio)
    conversio = euros_nets * canvi

    return round(conversio, 2)


while True:

    quantitat = float(input("Introdueix la quantitat de diners en euros: "))

    if quantitat == 0:
        print("Sortint...")
        break

    print("A quina moneda vols canviar?")
    print("1. Lliures")
    print("2. Dolars")
    print("3. Yens")

    opcio = int(input("Tria una opcio: "))

    if opcio == 1:
        moneda = "Lliures"

    elif opcio == 2:
        moneda = "Dolars"

    elif opcio == 3:
        moneda = "Yens"

    else:
        print("Opcio no valida. Torna a intentar.")
        continue

    conversio = convertir_divisa(quantitat, moneda)

    print("La quantitat de", quantitat, "euros es equivalent a", conversio, moneda)
