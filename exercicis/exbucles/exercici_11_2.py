files = int(input("Posa quantes files vols: "))
k = 0

for i in range(1, files + 1):
    for space in range(1, files - i + 1):
        print(" ", end="")

    while k != (2 * i - 1):
        print("*", end="")
        k = k + 1

    k = 0
    print()
