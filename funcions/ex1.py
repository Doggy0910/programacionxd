def nota_mitjana(nota1, nota2, nota3):
    mitja = (nota1 + nota2 + nota3) / 3
    if nota1 < 5 or nota2 < 5 or nota3 < 5:
        mitja = min(mitja, 4)

    return round(mitja, 2)


def nota_text(nota):
    if nota < 5:
        return "Insuficient"
    elif nota < 6:
        return "Suficient"
    elif nota < 7:
        return "Bé"
    elif nota < 9:
        return "Notable"
    else:
        return "Excel·lent"


n1 = float(input("Introdueix la primera nota: "))
n2 = float(input("Introdueix la segona nota: "))
n3 = float(input("Introdueix la tercera nota: "))

mitjana = nota_mitjana(n1, n2, n3)
print("Nota mitjana:", mitjana)
print("Qualificació:", nota_text(mitjana))



    