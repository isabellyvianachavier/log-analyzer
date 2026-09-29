LIMITE_FALHAS = 5


def ler_logs(caminho):
    """
    Lê o arquivo de logs e retorna uma lista com as linhas.
    """

    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()

    return linhas


def analisar_logs(linhas):
    """
    Analisa os logs e retorna as informações coletadas.
    """

    total_sucessos = 0
    total_falhas = 0

    falhas_por_usuario = {}
    falhas_por_ip = {}

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

            # Falhas por usuário
            if usuario not in falhas_por_usuario:
                falhas_por_usuario[usuario] = 0

            falhas_por_usuario[usuario] += 1

            # Falhas por IP
            if ip not in falhas_por_ip:
                falhas_por_ip[ip] = 0

            falhas_por_ip[ip] += 1

    return {
        "total_eventos": len(linhas),
        "total_sucessos": total_sucessos,
        "total_falhas": total_falhas,
        "falhas_por_usuario": falhas_por_usuario,
        "falhas_por_ip": falhas_por_ip
    }


def encontrar_maiores_falhas(falhas_por_usuario, falhas_por_ip):
    """
    Encontra o usuário e o IP com maior número de falhas.
    """

    usuario_mais_falhas = max(
        falhas_por_usuario,
        key=falhas_por_usuario.get
    )

    ip_mais_falhas = max(
        falhas_por_ip,
        key=falhas_por_ip.get
    )

    return usuario_mais_falhas, ip_mais_falhas


def detectar_ips_suspeitos(falhas_por_ip):
    """
    Identifica IPs que ultrapassaram o limite de falhas.
    """

    ips_suspeitos = {}

    for ip, quantidade in falhas_por_ip.items():

        if quantidade >= LIMITE_FALHAS:
            ips_suspeitos[ip] = quantidade

    return ips_suspeitos


def gerar_relatorio(analise, usuario_mais_falhas, ip_mais_falhas, ips_suspeitos):
    """
    Exibe o relatório final no terminal.
    """

    print("================================")
    print("         LOG ANALYZER")
    print("================================")

    print("\nResumo:")

    print(
        "Total de eventos:",
        analise["total_eventos"]
    )

    print(
        "Logins bem-sucedidos:",
        analise["total_sucessos"]
    )

    print(
        "Logins malsucedidos:",
        analise["total_falhas"]
    )

    print("\nFalhas por usuário:")

    for usuario, quantidade in analise["falhas_por_usuario"].items():

        print(
            usuario,
            "→",
            quantidade
        )

    print("\nFalhas por IP:")

    for ip, quantidade in analise["falhas_por_ip"].items():

        print(
            ip,
            "→",
            quantidade
        )

    print("\nUsuário com mais falhas:")

    print(
        usuario_mais_falhas,
        "→",
        analise["falhas_por_usuario"][usuario_mais_falhas]
    )

    print("\nIP com mais falhas:")

    print(
        ip_mais_falhas,
        "→",
        analise["falhas_por_ip"][ip_mais_falhas]
    )

    print("\nIPs potencialmente suspeitos:")

    if ips_suspeitos:

        for ip, quantidade in ips_suspeitos.items():

            print(
                ip,
                "→",
                quantidade,
                "tentativas malsucedidas"
            )

    else:

        print("Nenhum IP atingiu o limite de falhas.")


def main():

    caminho_logs = "data/access.log"

    linhas = ler_logs(caminho_logs)

    analise = analisar_logs(linhas)

    usuario_mais_falhas, ip_mais_falhas = encontrar_maiores_falhas(
        analise["falhas_por_usuario"],
        analise["falhas_por_ip"]
    )

    ips_suspeitos = detectar_ips_suspeitos(
        analise["falhas_por_ip"]
    )

    gerar_relatorio(
        analise,
        usuario_mais_falhas,
        ip_mais_falhas,
        ips_suspeitos
    )


if __name__ == "__main__":
    main()