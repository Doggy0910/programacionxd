import  random

tornar_a_jugar="s"

while tornar_a_jugar=="s":
    numeropy=random.randint(1,100)
    intents=0
    trobat=False

    print("---------JOC DE TROBAR UN NUMERO-----------")
    print("He escollit un nombre entre 1 i 100")
    print("Tens 7 intents per poder trobar-ho")
 
    while intents < 7 and not trobat:
            numero = int(input("Endevina el número: "))
            intents += 1

            if numero < numeropy:
                print("El nombre ha de ser mes gran!")

            elif numero > numeropy:
                print("El numero es mes petit!")

            else: 
                trobat = True
                print("L'has trobat en" ,intents, "intents !")

    if not trobat:
        print("Has perdut..., el numero era" , numeropy)

    tornar_a_jugar = input("Vols tornar a jugar s/n")



            

            
    

