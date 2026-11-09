import requests


# versio amb una api de la conversio

def convertir_divisa(quantitat, moneda):

    if moneda == "JPY":
        comissio = 0.07

    elif moneda == "GBP":
        comissio = 0.02

    elif moneda == "USD":
        comissio = 0.035

    quantitat_final = quantitat - (quantitat * comissio)

    dades = {
        "from": "EUR",
        "to": moneda,
        "amount": quantitat_final
    }

    resposta = requests.post(
        "https://api.botoi.com/v1/currency/convert",
        json=dades
    )

    return resposta.json(), quantitat * comissio


quantitat = float(input("Introdueix la quantitat de diners en euros: "))

while True:
    print("\nA quina moneda vols canviar?")
    print("1. Lliures")
    print("2. Dolars")
    print("3. Yens")
    print("4. Sortir")

    opcio = int(input("Tria una opcio: "))

    if opcio == 1:
        moneda = "GBP"
    elif opcio == 2:
        moneda = "USD"
    elif opcio == 3:
        moneda = "JPY"
    elif opcio == 4:
        print("Sortint...")
        break
    else:
        print("Opcio no valida.")
        continue

    conversio, comissio = convertir_divisa(quantitat, moneda)

    print("Comissio:", round(comissio, 2), "EUR")
    print("Resultat:", conversio["data"]["result"], moneda)

    # http POST https://api.botoi.com/v1/currency/convert from=EUR to=USD amount:=100 la peti.