import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.campus import Campus
from data.repo import campus_repo
import pandas as pd

def importar_campus(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        campi_unicos = df['Campus'].dropna().unique()
        
        campus_inseridos = 0
        campus_existentes = 0
        campus_com_erro = 0
        
        campus_existentes_bd = campus_repo.obter_todos()
        nomes_existentes = {c.nome_campus for c in campus_existentes_bd}

        for nome_campus in campi_unicos:
            try:
                nome_campus = str(nome_campus).strip()
                
                if not nome_campus or nome_campus == 'nan':
                    continue
                
                if nome_campus in nomes_existentes:
                    campus_existentes += 1
                    print(f"Campus '{nome_campus}' já existe, pulando...")
                    continue
                
                campus = Campus(
                    cod_campus=None,
                    nome_campus=nome_campus
                )
                
                cod = campus_repo.inserir(campus)
                nomes_existentes.add(nome_campus)
                campus_inseridos += 1
                print(f"Campus '{nome_campus}' inserido (ID: {cod})")
                
            except Exception as e:
                campus_com_erro += 1
                print(f"Erro ao inserir '{nome_campus}': {e}")
        
        print(f"\nImportação concluída.")
        print(f"Campus inseridos: {campus_inseridos}")
        print(f"Campus já existentes: {campus_existentes}")
        print(f"Campus com erro: {campus_com_erro}")
        print(f"Total processado: {campus_inseridos + campus_existentes + campus_com_erro}/{len(campi_unicos)}\n")

    except Exception as e:
        print(f"Erro na importação: {e}")