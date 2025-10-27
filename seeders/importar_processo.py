import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.processo import Processo
from data.repo import processo_repo
import pandas as pd

def importar_processos(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        processos_inseridos = 0
        processos_com_erro = 0
        
        for index, row in df.iterrows():
            try:
                codigo_edocs = str(row['Código Edocs']).strip() if pd.notna(row['Código Edocs']) else None
                numero_processo = str(row['Processo florestal nº']).strip() if pd.notna(row['Processo florestal nº']) else None
                codigo_empreendimento = str(row['Código do empreendimento nº']).strip() if pd.notna(row['Código do empreendimento nº']) else None
                
                if not numero_processo or numero_processo == 'nan':
                    print(f"Linha {index + 2}: Processo sem número, pulando...")
                    continue
                    
                if not codigo_empreendimento or codigo_empreendimento == 'nan':
                    print(f"Linha {index + 2}: Processo {numero_processo} sem código de empreendimento, pulando...")
                    continue
                
                if codigo_edocs == 'nan' or codigo_edocs == 'Ainda não Digitalizado':
                    codigo_edocs = None
                
                processo = Processo(
                    cod_processo=None,
                    codigo_edocs=codigo_edocs,
                    numero_processo_florestal=numero_processo,
                    codigo_empreendimento=codigo_empreendimento
                )
                
                cod = processo_repo.inserir(processo)
                processos_inseridos += 1
                
                if codigo_edocs:
                    print(f"Processo {numero_processo} (e-Docs: {codigo_edocs}) inserido (ID: {cod})")
                else:
                    print(f"Processo {numero_processo} inserido (ID: {cod})")
                    
            except Exception as e:
                processos_com_erro += 1
                print(f"Erro ao inserir processo linha {index + 2}: {e}")
        
        print(f"\nImportação concluída.")
        print(f"Processos inseridos: {processos_inseridos}")
        print(f"Processos com erro: {processos_com_erro}")
        print(f"Total processado: {processos_inseridos + processos_com_erro}/{len(df)}")

    except Exception as e:
        print(f"Erro na importação: {e}")