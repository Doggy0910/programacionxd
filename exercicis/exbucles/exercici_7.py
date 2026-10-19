n = int(input("Introdueix un nombre enter positiu: "))

factorial = 1
if n==0:
    print("El factorial de 0 es 1")
else:
    for i in range(1, n + 1):
        factorial = factorial * i
    print("El factorial de", n, "és:", factorial)