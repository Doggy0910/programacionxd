salari_brut = float(input("Introdueix el teu salari brut mensual: "))

if salari_brut <= 1000:
    percentatge_retencio = 5
elif salari_brut <= 2000:
    percentatge_retencio = 15
else:
    percentatge_retencio = 20

descomptat = salari_brut * percentatge_retencio / 100
salari_net = salari_brut - descomptat

print("Retenció aplicada:", percentatge_retencio, "%")
print("Quantitat descomptada:", float(descomptat), "€")
print("Salari net:", float(salari_net), "€")