import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.analise_processos import AnaliseProcessos
from data.repo import analise_processos_repo, processo_repo, usuario_repo, status_repo, notificacao_repo, campus_repo
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
    
    return None

def importar_analise_processos(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        analises_inseridas = 0
        analises_com_erro = 0
        
        processos = processo_repo.obter_todos()
        processo_map = {p.numero_processo_florestal: p.cod_processo for p in processos}
        
        usuarios = usuario_repo.obter_todos()
        usuario_map = {u.nome_usuario: u.cod_usuario for u in usuarios}
        
        campus_bd = campus_repo.obter_todos()
        campus_map = {c.nome_campus: c.cod_campus for c in campus_bd}
        
        status_list = status_repo.obter_todos()
        notificacoes = notificacao_repo.obter_todos()
        notificacao_map = {n.motivo_notificacao: n.cod_notificacao for n in notificacoes}
        
        for index, row in df.iterrows():
            try:
                numero_processo = str(row['Processo florestal nº']).strip() if pd.notna(row['Processo florestal nº']) else None
                nome_avaliador = str(row['Nome completo do avaliador Ifes do processo CAR']).strip() if pd.notna(row['Nome completo do avaliador Ifes do processo CAR']) else None
                campus_nome = str(row['Campus']).strip() if pd.notna(row['Campus']) else None
                
                if not numero_processo or numero_processo == 'nan':
                    continue
                
                cod_processo = processo_map.get(numero_processo)
                cod_usuario = usuario_map.get(nome_avaliador)
                cod_campus = campus_map.get(campus_nome)
                
                data_inicio_str = str(row['Data e Hora do início da análise']).strip() if pd.notna(row['Data e Hora do início da análise']) else None
                data_inicio = parse_data(data_inicio_str)
                
                data_previsao_str = str(row['Meta de prazo de andamento do processo']).strip() if pd.notna(row['Meta de prazo de andamento do processo']) else None
                data_previsao_fim = parse_data(data_previsao_str)
                
                cod_status = status_list[index].cod_status if index < len(status_list) else None
                
                motivo_notificacao = str(row['Motivo da notificação ao proprietário (se aplicável)']).strip() if pd.notna(row['Motivo da notificação ao proprietário (se aplicável)']) else None
                cod_notificacao = notificacao_map.get(motivo_notificacao) if motivo_notificacao and motivo_notificacao != 'nan' else None
                
                analise = AnaliseProcessos(
                    cod_analise=None,
                    data_hora_inicio_analise=data_inicio,
                    data_previsao_fim_analise=data_previsao_fim,
                    cod_campus=cod_campus,
                    cod_usuario=cod_usuario,
                    cod_status=cod_status,
                    cod_notificacao=cod_notificacao,
                    cod_processo=cod_processo
                )
                
                cod = analise_processos_repo.inserir(analise)
                analises_inseridas += 1
                print(f"Análise do processo {numero_processo} inserida (ID: {cod})")
                
            except Exception as e:
                analises_com_erro += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nImportação de Análises concluída.")
        print(f"Análises inseridas: {analises_inseridas}")
        print(f"Análises com erro: {analises_com_erro}")

    except Exception as e:
        print(f"Erro na importação: {e}")