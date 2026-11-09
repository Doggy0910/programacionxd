n = int(input("Un numero (0 per acabar): "))
suma = 0
comptador = 0

while True:
    if n == 0:
        break

    suma = suma + n
    comptador = comptador + 1
    n = int(input("Un altre numero: "))

print("La suma es", suma)
print("Has introduit", comptador, "numeros")





