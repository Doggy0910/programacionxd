n = int(input("Introdueix un nombre enter positiu mes gran que 1:"))

divisors = 0

for i in range(2, n):
    if n % i == 0:
        divisors = divisors + 1

if divisors == 0:
    print("Es un nombre primer")
else:
    print("Es un nombre compost")

