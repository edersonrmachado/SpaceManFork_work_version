from collections import Counter

def analisar_inclinacoes_tle(arquivo_consolidado):
    inclinacoes = []
    
    with open(arquivo_consolidado, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        
    # Os TLEs consistem em pares de linhas (Linha 1 e Linha 2)
    # A Linha 2 contém a inclinação nos caracteres de índice 8 a 16
    for i in range(len(linhas)):
        linha = linhas[i].strip()
        # Identifica a Linha 2 do TLE (geralmente começa com '2 ')
        if linha.startswith('2 '):
            try:
                # Extrai o valor da inclinação (colunas 8 a 16 na especificação TLE)
                val_inc_str = linha[8:16].strip()
                # Arredonda para 2 casas decimais para agrupar planos próximos
                inc = round(float(val_inc_str), 2)
                inclinacoes.append(inc)
            except ValueError:
                continue

    # Conta quantos satélites pertencem a cada plano de inclinação
    contagem_planos = Counter(inclinacoes)
    
    print("--- Distribuição dos Planos Orbitais (Inclinação) ---")
    print(f"{'Inclinação (°)':<15} | {'Qtd de Satélites':<15}")
    print("-" * 35)
    for inc, qtd in sorted(contagem_planos.items(), key=lambda x: x[1], reverse=True):
        print(f"{inc:<15} | {qtd:<15}")

# --- Exemplo de uso ---
# Certifique-se de que o arquivo consolidado gerado anteriormente está na pasta
analisar_inclinacoes_tle('all.tle')