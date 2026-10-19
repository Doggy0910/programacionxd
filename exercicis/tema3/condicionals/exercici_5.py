edat = int(input("Introdueix la teva edat"))
if edat: 
    if edat < 5:
        print("La teva entrada es gratis")
    elif 5 <= edat <=17:
        print("La teva entrada costa 5€")
    elif 18 <= edat <= 64:
        print("La teva entrada costa 10€")
    else:
        print("La teva entrada costa 4€")
    