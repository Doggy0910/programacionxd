any = int(input("Introdueix l'any: "))

if any % 400 == 0 or (any % 4 == 0 and any % 100 != 0):
    print("És un any de traspàs (366 dies).")
else:
    print("No és un any de traspàs (365 dies).")