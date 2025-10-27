import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.notificacao import Notificacao
from data.repo import notificacao_repo
import pandas as pd

def importar_notificacoes(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        motivos_unicos = df['Motivo da notificação ao proprietário (se aplicável)'].dropna().unique()
        
        notificacoes_inseridas = 0
        notificacoes_com_erro = 0
        
        for motivo in motivos_unicos:
            try:
                motivo = str(motivo).strip()
                
                if not motivo or motivo == 'nan' or motivo == '':
                    continue
                
                notificacao = Notificacao(
                    cod_notificacao=None,
                    motivo_notificacao=motivo
                )
                
                cod = notificacao_repo.inserir(notificacao)
                notificacoes_inseridas += 1
                print(f"Notificação '{motivo}' inserida (ID: {cod})")
                    
            except Exception as e:
                notificacoes_com_erro += 1
                print(f"Erro ao inserir notificação: {e}")
        
        print(f"\nImportação de Notificações concluída.")
        print(f"Notificações inseridas: {notificacoes_inseridas}")
        print(f"Notificações com erro: {notificacoes_com_erro}")
        print(f"Total processado: {notificacoes_inseridas + notificacoes_com_erro}/{len(motivos_unicos)}")

    except Exception as e:
        print(f"Erro na importação: {e}")

if __name__ == "__main__":
    caminho = "seeders/processos.csv"
    importar_notificacoes(caminho)