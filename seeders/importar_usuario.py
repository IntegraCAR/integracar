import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.usuario import Usuario
from data.repo import usuario_repo, campus_repo
import pandas as pd

def importar_usuarios(caminho_arquivo):
    try:
        df = importar_csv(caminho_arquivo)
        
        usuarios_inseridos = 0
        usuarios_com_erro = 0
        
        campus_bd = campus_repo.obter_todos()
        campus_map = {c.nome_campus: c.cod_campus for c in campus_bd}
        
        usuarios_inseridos_set = set()
        
        for index, row in df.iterrows():
            try:
                nome_avaliador = str(row['Nome completo do avaliador Ifes do processo CAR']).strip() if pd.notna(row['Nome completo do avaliador Ifes do processo CAR']) else None
                campus_nome = str(row['Campus']).strip() if pd.notna(row['Campus']) else None
                
                if nome_avaliador and nome_avaliador != 'nan' and nome_avaliador not in usuarios_inseridos_set:
                    cod_campus = campus_map.get(campus_nome)
                    
                    email_padrao = f"{nome_avaliador.lower().replace(' ', '.').replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}@ifes.edu.br"
                    cpf_padrao = '00000000000'
                    senha_padrao = 'PLACEHOLDER_SENHA'
                    
                    usuario = Usuario(
                        cod_usuario=None,
                        cod_campus=cod_campus,
                        cod_orientador=None,
                        nome_usuario=nome_avaliador,
                        email_usuario=email_padrao,
                        senha_usuario=senha_padrao,
                        cpf_usuario=cpf_padrao,
                        role_usuario='ORIENTADOR',
                        organizacao_usuario='IFES'
                    )
                    
                    try:
                        cod = usuario_repo.inserir(usuario)
                        usuarios_inseridos_set.add(nome_avaliador)
                        usuarios_inseridos += 1
                        print(f"Usuário '{nome_avaliador}' (ORIENTADOR - Campus: {campus_nome}) inserido (ID: {cod})")
                    except (IndexError, TypeError) as e:
                        print(f"Erro ao inserir '{nome_avaliador}': {e}")
                        usuarios_com_erro += 1
                
                nome_ponto_focal = str(row['Nome completo do ponto focal Idaf']).strip() if pd.notna(row['Nome completo do ponto focal Idaf']) else None
                campus_nome = str(row['Campus']).strip() if pd.notna(row['Campus']) else None

                if nome_ponto_focal and nome_ponto_focal != 'nan' and nome_ponto_focal not in usuarios_inseridos_set:
                    cod_campus = campus_map.get(campus_nome)

                    email_padrao = f"{nome_ponto_focal.lower().replace(' ', '.').replace('ç', 'c').replace('ã', 'a').replace('õ', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}@idaf.es.gov.br"
                    cpf_padrao = '00000000000'
                    senha_padrao = 'PLACEHOLDER_SENHA'
                    
                    usuario = Usuario(
                        cod_usuario=None,
                        cod_campus=cod_campus,
                        cod_orientador=None,
                        nome_usuario=nome_ponto_focal,
                        email_usuario=email_padrao,
                        senha_usuario=senha_padrao,
                        cpf_usuario=cpf_padrao,
                        role_usuario='CONSULTOR',
                        organizacao_usuario='IDAF'
                    )
                    
                    try:
                        cod = usuario_repo.inserir(usuario)
                        usuarios_inseridos_set.add(nome_ponto_focal)
                        usuarios_inseridos += 1
                        print(f"Usuário '{nome_ponto_focal}' (CONSULTOR - Campus: {campus_nome}) inserido (ID: {cod})")
                    except (IndexError, TypeError) as e:
                        print(f"Erro ao inserir '{nome_ponto_focal}': {e}")
                        usuarios_com_erro += 1
                    
            except Exception as e:
                usuarios_com_erro += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nImportação de Usuários concluída.")
        print(f"Usuários inseridos: {usuarios_inseridos}")
        print(f"Usuários com erro: {usuarios_com_erro}")

    except Exception as e:
        print(f"Erro na importação: {e}")

if __name__ == "__main__":
    caminho = "seeders/processos.csv"
    importar_usuarios(caminho)