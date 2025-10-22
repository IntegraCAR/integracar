from importar_csv import importar_csv
from data.model.campus import Campus
from data.repo import campus_repo

def importar_campus(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        campi_unicos = df['Campus'].dropna().unique()
        print(f"Campus únicos encontrados: {len(campi_unicos)}\n")

        for nome_campus in campi_unicos:
            nome_campus = str(nome_campus).strip()
            
            if nome_campus and nome_campus != 'nan':
                try:
                    campus = Campus(nome_campus=nome_campus)
                    cod = campus_repo.inserir(campus)
                    print(f"Campus '{nome_campus}' inserido (ID: {cod})")
                except Exception as e:
                    print(f"Erro ao inserir '{nome_campus}': {e}")
        
        print(f"\nImportação concluída!")

    except Exception as e:
        print(f"Erro: {e}")

caminho = "processos.csv"
importar_campus(caminho)