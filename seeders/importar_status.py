import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.status import Status
from data.repo import status_repo
import pandas as pd
from datetime import datetime

def parse_data(data_str):
    if not data_str or str(data_str).strip() in ['nan', '', '00/00/2025 00:00:00', 'NaT']:
        return None
    
    data_str = str(data_str).strip()
    
    formatos = [
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(data_str, formato)
        except:
            continue
    
    print(f"Não foi possível converter data: '{data_str}'")
    return None

def importar_status(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        status_inseridos = 0
        status_com_erro = 0
        
        for index, row in df.iterrows():
            try:
                tipo_status = str(row['Status']).strip() if pd.notna(row['Status']) else None
                data_atualizacao_str = str(row['Data e Hora da ultima atualização de Status']).strip() if pd.notna(row['Data e Hora da ultima atualização de Status']) else None

                if not tipo_status or tipo_status == 'nan':
                    continue
                
                data_atualizacao = parse_data(data_atualizacao_str)
                
                status = Status(
                    cod_status=None,
                    data_hora_ultima_atualizacao=data_atualizacao,
                    tipo_status=tipo_status
                )
                
                cod = status_repo.inserir(status)
                status_inseridos += 1
                
                if data_atualizacao:
                    data_formatada = data_atualizacao.strftime('%d/%m/%Y %H:%M:%S')
                else:
                    data_formatada = 'Sem data'
                    
                print(f"Status '{tipo_status}' ({data_formatada}) inserido (ID: {cod})")
                
            except Exception as e:
                status_com_erro += 1
                print(f"Erro ao inserir status linha {index + 2}: {e}")
        
        print(f"\nImportação de Status concluída.")
        print(f"Status inseridos: {status_inseridos}")
        print(f"Status com erro: {status_com_erro}")
        print(f"Total processado: {status_inseridos + status_com_erro}/{len(df)}\n")

    except Exception as e:
        print(f"Erro na importação: {e}")