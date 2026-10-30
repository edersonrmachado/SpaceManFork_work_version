from pathlib import Path

def consolidar_tles(arquivo_saida):
    # Usa o diretório atual (.)
    pasta = Path('.')

    total_arquivos = 0
    
    # Abre o arquivo final para escrita
    with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
        # Percorre todos os arquivos .tle na pasta atual
        for arquivo_tle in sorted(pasta.glob('*.tle')):
            # Ignora o próprio arquivo de saída se ele já existir na pasta
            if arquivo_tle.name == arquivo_saida:
                continue
                
            print(f"Lendo: {arquivo_tle.name}")
            with open(arquivo_tle, 'r', encoding='utf-8') as f_in:
                f_out.write(f_in.read())
                f_out.write('\n')
            total_arquivos += 1

    print(f"\nSucesso! {total_arquivos} arquivos TLE foram consolidados em '{arquivo_saida}'.")

# Nome do arquivo final gerado
consolidar_tles('consolidado.tle')