n = int(input("Introdueix un numero mes gran que 1:"))
for i in range(1, n + 1):
    if n % i == 0:
        print(i)
