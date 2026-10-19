n = int(input("Cuants numeros "))

suma = 0

for i in range(n):
    num = float(input("Introdueix un numero: "))

    suma = suma + num

    if i == 0:
        mayor = num
        menor = num
    else:
        if num > mayor:
            mayor = num
        if num < menor:
            menor = num

mitjana = suma / n

print("La suma es:", suma)
print("La meitja es:", mitjana)
print("El mayor es:", mayor)
print("El menor es:", menor)





