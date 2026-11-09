# segona versio mes eficient

def convertir_emmagatzematge(quantitat, unitat_origen, unitat_desti):

    unitats = {"MB": 1, "GB": 1024, "TB": 1048576}

    resultat = quantitat * unitats[unitat_origen] / unitats[unitat_desti]

    return resultat


while True:

    quantitat = float(input("Quantitat (0 per sortir): "))

    if quantitat == 0:
        break

    unitat_origen = input("Unitat d'origen (MB, GB, TB): ")
    unitat_desti = input("Unitat de destí (MB, GB, TB): ")

    resultat = convertir_emmagatzematge(quantitat, unitat_origen, unitat_desti)

    print("Resultat:", resultat, unitat_desti)
