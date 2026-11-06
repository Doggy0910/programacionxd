def convertir_divisa(quantitat, moneda):
    if moneda == "Yens":
        conversio = quantitat * 177
    elif moneda == "Lliures":
        conversio = quantitat * 0.85
    elif moneda == "Dolars":
        conversio = quantitat * 1.08

    return conversio


quantitat = float(input("Introdueix la quantitat de diners en euros: "))

while True:
    print("A quina moneda vols canviar?")
    print("1. Lliures")
    print("2. Dolars")
    print("3. Yens")
    print("4. Sortir")
    opcio = int(input("Tria una opcio: "))

    if opcio == 1:
        moneda = "Lliures"
        conversio = convertir_divisa(quantitat, moneda)
        print("La quantitat de", quantitat, "euros es equivalent a", conversio, moneda)
    elif opcio == 2:
        moneda = "Dolars"
        conversio = convertir_divisa(quantitat, moneda)
        print("La quantitat de", quantitat, "euros es equivalent a", conversio, moneda)
    elif opcio == 3:
        moneda = "Yens"
        conversio = convertir_divisa(quantitat, moneda)
        print("La quantitat de", quantitat, "euros es equivalent a", conversio, moneda)
    elif opcio == 4:
        print("Sortint...")
        break
    else:
        print("Opcio no valida. Torna a intentar.")


