def coletar_dados():
    print("=== Sistema Especialista: Manutenção Preditiva de Veículos ===\n")

    marca = input("1. Qual a marca do veículo? (Ex: Chevrolet, Volkswagen, etc.): ").strip().capitalize()
    modelo = input("2. Qual o modelo do veículo? (Ex: Onix, Gol): ").strip()

    # Validação do ano
    while True:
        try:
            ano = int(input("3. Qual o ano do veículo? (Ex: 2018): ").strip())
            if 1900 <= ano <= 2025:
                break
            else:
                print("Ano inválido. Digite um valor entre 1900 e 2025.")
        except ValueError:
            print("Por favor, digite um número válido.")

    combustivel = input("4. Tipo de combustível (Gasolina, Etanol, Flex, Diesel): ").strip().capitalize()
    uso = input("5. Tipo de uso do veículo (Urbano, Rodoviário, Misto, Serviço pesado): ").strip().lower()

    # Validação da quilometragem
    while True:
        try:
            km = int(input("6. Quilometragem atual do veículo (Ex: 48000): ").strip())
            if km >= 0:
                break
            else:
                print("Quilometragem não pode ser negativa.")
        except ValueError:
            print("Por favor, digite um número válido.")

    print("\n7. O motor apresenta algum dos seguintes comportamentos?")
    superaquecimento = input("   - Superaquecimento? (s/n): ").strip().lower() == 's'
    partida_dificil = input("   - Dificuldade na partida? (s/n): ").strip().lower() == 's'
    fumaca = input("   - Emissão de fumaça incomum? (s/n): ").strip().lower() == 's'
    ruidos = input("   - Ruídos incomuns? (s/n): ").strip().lower() == 's'
    vibracao = input("   - Vibração incomum ao dirigir? (s/n): ").strip().lower() == 's'

    print("\n8. Histórico de falhas:")
    falhas = []
    if input("   - Já teve falha no sensor de oxigênio? (s/n): ").strip().lower() == 's':
        falhas.append("sensor_oxigenio")
    if input("   - Já teve superaquecimento? (s/n): ").strip().lower() == 's':
        falhas.append("superaquecimento")
    if input("   - Já teve pane elétrica? (s/n): ").strip().lower() == 's':
        falhas.append("pane_eletrica")
    if input("   - Já teve falha na injeção eletrônica? (s/n): ").strip().lower() == 's':
        falhas.append("falha_injecao")
    if input("   - Já abasteceu com combustível de origem duvidosa? (s/n): ").strip().lower() == 's':
        falhas.append("combustivel_ruim")

    modelo_lower = modelo.lower()
    marca_lower = marca.lower()
    verificacoes_extras = {}

    if modelo_lower == "onix":
        resposta = input("\n9. Você já verificou o estado da correia banhada a óleo? (s/n): ").strip().lower()
        verificacoes_extras["correia_onix_verificada"] = resposta == 's'

    if modelo_lower == "gol":
        resposta = input("\n9. Você já verificou a lubrificação do motor? (s/n): ").strip().lower()
        verificacoes_extras["lubrificacao_gol_verificada"] = resposta == 's'

    if marca_lower == "ford" and superaquecimento:
        resposta = input("\n9. O sistema de arrefecimento já foi revisado? (s/n): ").strip().lower()
        verificacoes_extras["superaquecimento_ford_verificado"] = resposta == 's'

    dados = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "combustivel": combustivel,
        "uso": uso,
        "quilometragem": km,
        "comportamentos": {
            "superaquecimento": superaquecimento,
            "partida_dificil": partida_dificil,
            "fumaca": fumaca,
            "ruidos": ruidos,
            "vibracao": vibracao
        },
        "falhas": falhas,
        "verificacoes_extras": verificacoes_extras
    }

    return dados


def aplicar_regras(dados):
    recomendacoes = []

    km = dados["quilometragem"]
    uso = dados["uso"]
    marca = dados["marca"].lower()
    modelo = dados["modelo"].lower()
    ano = dados["ano"]
    combustivel = dados["combustivel"].lower()
    comportamentos = dados["comportamentos"]
    falhas = dados["falhas"]
    extras = dados.get("verificacoes_extras", {})

    idade_veiculo = 2025 - ano

    # --- Quilometragem e idade ---
    if km >= 10000:
        recomendacoes.append("Troca de óleo e filtro de óleo recomendada.")
    if km >= 20000:
        recomendacoes.append("Verificar filtro de ar e filtro de combustível.")
    if km >= 40000:
        recomendacoes.append("Verificar sistema de freios.")
    if km >= 60000 and marca == "chevrolet" and modelo == "onix":
        recomendacoes.append("Verificar correia dentada (padrão para Chevrolet Onix).")
    if km >= 80000 or idade_veiculo >= 8:
        recomendacoes.append("Avaliar troca da bomba d'água e mangueiras.")
    if km >= 100000:
        recomendacoes.append("Inspeção completa do sistema de suspensão.")

    # --- Tipo de uso ---
    if uso == "urbano" and km >= 5000:
        recomendacoes.append("Verificar desgaste prematuro por uso urbano intenso.")
    if uso == "rodoviário" and km >= 80000:
        recomendacoes.append("Verificar desgaste de pneus e balanceamento.")
    if uso == "serviço pesado":
        recomendacoes.append("Revisão frequente de suspensão e embreagem (uso severo).")

    # --- Combustível ---
    if combustivel == "diesel":
        recomendacoes.append("Verificar sistema de injeção diesel (alta pressão e bicos).")
    if combustivel == "flex" and km >= 50000:
        recomendacoes.append("Limpeza dos bicos injetores recomendada para veículos Flex.")

    # --- Comportamentos do motor ---
    if comportamentos["superaquecimento"] or "superaquecimento" in falhas:
        recomendacoes.append("Inspeção urgente do sistema de arrefecimento.")
    if comportamentos["partida_dificil"]:
        recomendacoes.append("Verificar bateria e sistema de ignição.")
    if comportamentos["fumaca"]:
        recomendacoes.append("Verificar queima de óleo ou mistura rica.")
    if comportamentos["ruidos"]:
        recomendacoes.append("Verificar folgas no motor ou desgaste interno.")
    if comportamentos["vibracao"]:
        recomendacoes.append("Verificar balanceamento das rodas e estado dos coxins.")

    # --- Histórico de falhas ---
    if "sensor_oxigenio" in falhas:
        recomendacoes.append("Avaliar substituição do sensor de oxigênio.")
    if "pane_eletrica" in falhas:
        recomendacoes.append("Revisar chicote elétrico e sistema de alternador.")
    if "combustivel_ruim" in falhas:
        recomendacoes.append("Verificar filtro de combustível e limpar sistema de injeção.")
    if len(falhas) >= 2:
        recomendacoes.append("Histórico de falhas indica necessidade de revisão geral.")

    # --- Específicas por modelo ---
    if marca == "chevrolet" and modelo == "onix" and ano > 2018:
        if not extras.get("correia_onix_verificada", False):
            recomendacoes.append("Verificar estado da correia banhada a óleo (Onix pós-2018).")
    if marca == "volkswagen" and modelo == "gol":
        if not extras.get("lubrificacao_gol_verificada", False):
            recomendacoes.append("Verificar lubrificação do motor (problemas comuns de carbonização no Gol).")
    if marca == "ford" and ano < 2012:
        if not extras.get("superaquecimento_ford_verificado", False):
            recomendacoes.append("Monitorar risco de superaquecimento (modelos Ford antigos).")
    if marca == "fiat" and modelo == "uno":
        recomendacoes.append("Verificar estado do cabeçote (modelos Uno com motor Fire).")
    if marca == "hyundai" and modelo == "hb20" and ano < 2015:
        recomendacoes.append("Verificar ruídos na suspensão dianteira (problema comum em HB20 até 2014).")

    # --- Subutilização ---
    if km < 5000 and idade_veiculo >= 2:
        recomendacoes.append("Veículo com baixa quilometragem para a idade: risco de ressecamento de borrachas e fluídos vencidos.")

    # --- Revisão periódica próxima ---
    if km % 10000 < 1000:
        recomendacoes.append("Revisão periódica próxima: agendar check-up preventivo.")

    # --- Sem recomendações ---
    if not recomendacoes:
        recomendacoes.append("Sem necessidade de manutenção imediata detectada.")

    return recomendacoes


def main():
    dados = coletar_dados()
    print("\n=== Recomendações de Manutenção ===")
    recomendacoes = aplicar_regras(dados)
    for rec in recomendacoes:
        print(f"- {rec}")


if __name__ == "__main__":
    main()
