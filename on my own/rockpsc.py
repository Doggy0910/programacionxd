import random
opciones = ["piedra", "papel", "tijeras"]
empates = 0
wins = 0
losses = 0

while True:
    jugador = input("Escoje uno.")
    python = random.choice(opciones)



    print("Tu:", jugador) 
    print("Python", python)

    if jugador == python:
        print("empate")
    elif jugador == "piedra" and python == "papel":
        print("Has perdido")
    elif jugador == "piedra" and python == "tijeras":
        print ("Has ganado")
    elif jugador == "piedra" and python == "papel":
        print("Has perdido")
    elif jugador == "papel" and python == "piedra":
        print("Has ganado")
    elif jugador == "papel" and python == "tijeras":
        print("Has perdido")
    elif jugador == "tijeras" and python == "piedra":
        print("Has perdido")
    elif jugador == "tijeras" and python == "papel":
        print("Has ganado")
    else:
        print("Error, no has escogido bien")

    if jugador == python: 
        empates +=1

    elif jugador == "piedra" and python == "papel":
        losses +=1
    elif jugador == "piedra" and python == "tijeras":
        wins +=1
    elif jugador == "piedra" and python == "papel":
        losses +=1
    elif jugador == "papel" and python == "piedra":
        wins +=1
    elif jugador == "papel" and python == "tijeras":
        losses +=1
    elif jugador == "tijeras" and python == "piedra":
        losses+=1
    elif jugador == "tijeras" and python == "papel":
        wins +=1


    if wins == 1:
        print("Wins", wins)
    elif losses == 1:
        print("Losses", losses)
    elif empates == 1:
        print("Draws", empates)

    else:
        print("Tus muertos pisaos")
    
