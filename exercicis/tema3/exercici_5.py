segons = int(input("Quants segons?"))

hores = segons // 3600
minuts = (segons % 3600) // 60
segons_restants = segons % 60

print(segons, "segons són", hores, "hores,", minuts, "minuts i", segons_restants, "segons.")


