# Python para análise de logs

with open("data/access.log", "r") as arquivo:
    linhas = arquivo.readlines()

total_sucessos = 0
total_falhas = 0

for linha in linhas:
    dados = linha.strip().split(",")

    data_hora = dados[0]
    evento = dados[1]
    usuario = dados[2]
    ip = dados[3]

    if evento == "LOGIN_SUCCESS":
        total_sucessos += 1

    elif evento == "LOGIN_FAILED":
        total_falhas += 1

    print("Data:", data_hora)
    print("Evento:", evento)
    print("Usuário:", usuario)
    print("IP:", ip)
    print()

print("Logins bem-sucedidos:", total_sucessos)
print("Logins malsucedidos:", total_falhas)