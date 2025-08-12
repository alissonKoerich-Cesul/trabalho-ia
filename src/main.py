def coletar_dados():
    print("=== Sistema Especialista: Manutenção Preditiva de Veículos ===\n")

    marca = input("1. Qual a marca do veículo? (Ex: Chevrolet, Volkswagen, etc.): ").strip().capitalize()
    modelo = input("2. Qual o modelo do veículo? (Ex: Onix, Gol): ").strip()
    ano = int(input("3. Qual o ano do veículo? (Ex: 2018): ").strip())
    combustivel = input("4. Tipo de combustível (Gasolina, Etanol, Flex, Diesel): ").strip().capitalize()
    uso = input("5. Tipo de uso do veículo (Urbano, Rodoviário, Misto, Serviço pesado): ").strip().lower()
    km = int(input("6. Quilometragem atual do veículo (Ex: 48000): ").strip())

    print("\n7. O motor apresenta algum dos seguintes comportamentos?")
    superaquecimento = input("   - Superaquecimento? (s/n): ").strip().lower() == 's'
    partida_dificil = input("   - Dificuldade na partida? (s/n): ").strip().lower() == 's'
    fumaca = input("   - Emissão de fumaça incomum? (s/n): ").strip().lower() == 's'
    ruidos = input("   - Ruídos incomuns? (s/n): ").strip().lower() == 's'

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

    # Perguntas específicas
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
    comportamentos = dados["comportamentos"]
    falhas = dados["falhas"]
    extras = dados.get("verificacoes_extras", {})

    # --- Regras por quilometragem ---
    if km >= 10000:
        recomendacoes.append("Troca de óleo e filtro de óleo recomendada.")
    if km >= 20000:
        recomendacoes.append("Verificar filtro de ar e filtro de combustível.")
    if km >= 40000:
        recomendacoes.append("Verificar sistema de freios.")
    if km >= 60000 and marca == "chevrolet" and modelo == "onix":
        recomendacoes.append("Verificar correia dentada (padrão para Chevrolet Onix).")

    # --- Regras por tipo de uso ---
    if uso == "urbano" and km >= 5000:
        recomendacoes.append("Verificar desgaste prematuro por uso urbano intenso.")

    # --- Regras por comportamento do motor ---
    if comportamentos["superaquecimento"] or "superaquecimento" in falhas:
        recomendacoes.append("Inspeção urgente do sistema de arrefecimento.")
    if comportamentos["partida_dificil"]:
        recomendacoes.append("Verificar bateria e sistema de ignição.")
    if comportamentos["fumaca"]:
        recomendacoes.append("Verificar queima de óleo ou mistura rica.")
    if comportamentos["ruidos"]:
        recomendacoes.append("Verificar folgas no motor ou desgaste interno.")

    # --- Regras por falhas anteriores ---
    if "sensor_oxigenio" in falhas:
        recomendacoes.append("Avaliar substituição do sensor de oxigênio.")
    if "pane_eletrica" in falhas:
        recomendacoes.append("Revisar chicote elétrico e sistema de alternador.")

    # --- Regras específicas por modelo/marca/ano com checagem das verificações ---
    if marca == "chevrolet" and modelo == "onix" and ano > 2018:
        if not extras.get("correia_onix_verificada", False):
            recomendacoes.append("Verificar estado da correia banhada a óleo (Onix pós-2018).")

    if marca == "volkswagen" and modelo == "gol":
        if not extras.get("lubrificacao_gol_verificada", False):
            recomendacoes.append("Verificar lubrificação do motor (problemas comuns de carbonização no Gol).")

    if marca == "ford" and ano < 2012:
        if not extras.get("superaquecimento_ford_verificado", False):
            recomendacoes.append("Monitorar risco de superaquecimento (modelos Ford antigos).")

    # --- Caso não haja nenhuma recomendação ---
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
