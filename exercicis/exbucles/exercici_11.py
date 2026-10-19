files = int(input("Quantes files vols? "))

for i in range(1, files + 1):
    espais = files - i
    ast = 2 * i - 1

    print(" " * espais + "*" * ast)