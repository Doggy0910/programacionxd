import requests


# versio amb una api de la conversio

def convertir_divisa(quantitat, moneda):
    dades = {
        "from": "EUR",
        "to": moneda,
        "amount": quantitat
    }

    resposta = requests.post(
        "https://api.botoi.com/v1/currency/convert",
        json=dades
    )

    return resposta.json()


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

    conversio = convertir_divisa(quantitat, moneda)
    print(conversio["data"]["result"], moneda)