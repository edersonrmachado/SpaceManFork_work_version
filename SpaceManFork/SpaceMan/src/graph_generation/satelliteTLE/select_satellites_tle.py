import json

def filter_and_save_tle(list_filename, all_tle_filename, output_tle_filename):
    # 1. Carregar a lista de satélites
    # (Se for um arquivo JSON de lista, use json.load(f). Se for um .txt com um por linha, use f.read().splitlines())
    with open(list_filename, "r", encoding="utf-8") as f:
        satellites_to_find = set(json.load(f)) 

    found_satellites = []
    
    # 2. Ler o arquivo grande 'all.tle' procurando os satélites
    with open(all_tle_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Verifica se o satélite atual está na lista
        matched_sat = None
        for sat in satellites_to_find:
            if sat in line:
                matched_sat = sat
                break
        
        if matched_sat:
            # Captura o bloco de linhas do TLE (geralmente 3 linhas por satélite)
            block = []
            for j in range(3):
                if i + j < len(lines):
                    block.append(lines[i + j])
            
            found_satellites.extend(block)
            i += len(block)
        else:
            i += 1

    # 3. Salvar o novo arquivo 'satellites.tle' diretamente
    with open(output_tle_filename, "w", encoding="utf-8") as f:
        f.writelines(found_satellites)

    print(f"Arquivo '{output_tle_filename}' gerado com sucesso!")

# Exemplo de uso:
filter_and_save_tle("../../../data/satellites.json", "all.tle", "satellites.tle")