costat1 = float(input("Introdueix la longitud del primer costat: "))
costat2 = float(input("Introdueix la longitud del segon costat: "))
costat3 = float(input("Introdueix la longitud del tercer costat: "))

if costat1 <= 0 or costat2 <= 0 or costat3 <= 0:
    print("Les longituds han de ser positives.")
elif (costat1 + costat2 <= costat3
      or costat1 + costat3 <= costat2
      or costat2 + costat3 <= costat1):
    print("Aquestes longituds no formen un triangle.")
elif costat1 == costat2 == costat3:
    print("El triangle és equilater.")
elif costat1 == costat2 or costat1 == costat3 or costat2 == costat3:
    print("El triangle és isosceles.")
else:
    print("El triangle és escale.")
