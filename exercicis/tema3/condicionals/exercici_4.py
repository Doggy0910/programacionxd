nota = float(input("Introdueix la teva nota: "))
if nota > 10 or nota < 0:
    print("La nota no és valida")
 
if nota >= 5 and nota < 6:
    print("Suficient")
 
elif nota >= 6 and nota < 7:
    print("Bé")
elif nota >= 7 and nota < 9:
    print("Notable")
elif nota>= 9 and nota <= 10:
    print("Excel·lent ")


else: 
    print("Has suspes")
