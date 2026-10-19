print("Comptador de vocals d'una frase")

frase = input("Escriu la frase: ")
vocals = 0

for lletra in frase.lower():
    if lletra in "aeiouàèéíïòóúü":
        print(lletra)
        vocals += 1

print("El nombre total de vocals és:", vocals)
    
    

    
