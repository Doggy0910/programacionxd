#

def convertir_emmagatzematge(quantitat, unitat_origen, unitat_desti):

    if unitat_origen == unitat_desti:
        return quantitat

    elif unitat_origen == "TB" and unitat_desti == "GB":
        return quantitat * 1024

    elif unitat_origen == "GB" and unitat_desti == "MB":
        return quantitat * 1024

    elif unitat_origen == "TB" and unitat_desti == "MB":
        return quantitat * 1024 * 1024

    elif unitat_origen == "MB" and unitat_desti == "GB":
        return quantitat / 1024

    elif unitat_origen == "GB" and unitat_desti == "TB":
        return quantitat / 1024

    elif unitat_origen == "MB" and unitat_desti == "TB":
        return quantitat / 1024 / 1024


while True:

    quantitat = float(input("Quantitat (0 per sortir): "))

    if quantitat == 0:
        break

    unitat_origen = input("Unitat d'origen (MB, GB, TB): ").upper()
    unitat_desti = input("Unitat de destí (MB, GB, TB): ").upper()

    resultat = convertir_emmagatzematge(quantitat, unitat_origen, unitat_desti)

    print("Resultat:", resultat, unitat_desti)
