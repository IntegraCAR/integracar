import sys
import os
import pandas as pd
import re
from typing import Set, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.usuario import Usuario
from data.repo import usuario_repo, campus_repo

def padronizar_nome(nome: str) -> str:
    if not nome or nome == 'nan':
        return nome
    
    excecoes = {'de', 'da', 'do', 'dos', 'das', 'e'}
    palavras = nome.strip().split()
    palavras_formatadas = []
    
    for i, palavra in enumerate(palavras):
        if i == 0 or palavra.lower() not in excecoes:
            palavras_formatadas.append(palavra.capitalize())
        else:
            palavras_formatadas.append(palavra.lower())
    
    return ' '.join(palavras_formatadas)

def limpar_nome(nome: str) -> str:
    substituicoes = {
        'ç': 'c', 'ã': 'a', 'á': 'a', 'â': 'a', 'à': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'ô': 'o',
        'õ': 'o', 'ú': 'u', 'ü': 'u'
    }
    nome_limpo = nome.lower()
    for k, v in substituicoes.items():
        nome_limpo = nome_limpo.replace(k, v)
    return re.sub(r'[^a-z]', '', nome_limpo)

def gerar_email_placeholder(nome: str, organizacao: str) -> str:
    nome_limpo = limpar_nome(nome)
    return f"placeholder_{nome_limpo}@{organizacao.lower()}.temporario"

def obter_cod_campus(campus_nome: str) -> Optional[int]:
    if not campus_nome or campus_nome == 'nan':
        return None
    campus = campus_repo.obter_por_nome(campus_nome)
    return campus.cod_campus if campus else None

def criar_usuario(nome: str, email: str, role: str, organizacao: str, 
                  cod_campus: Optional[int] = None, cod_orientador: Optional[int] = None) -> Usuario:
    return Usuario(
        cod_usuario=None,
        cod_campus=cod_campus,
        cod_orientador=cod_orientador,
        nome_usuario=nome,
        email_usuario=email,
        senha_usuario='PLACEHOLDER_SENHA',
        cpf_usuario='00000000000',
        role_usuario=role,
        organizacao_usuario=organizacao
    )

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    try:
        cod = usuario_repo.inserir(usuario)
        usuario.cod_usuario = cod
        usuario_repo.atualizar(usuario)
        return cod
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return None


def importar_orientadores_csv(caminho_arquivo: str) -> Set[str]:
    try:
        df = importar_csv(caminho_arquivo)
        orientadores_inseridos = set()
        contador = 0
        erros = 0
        
        for index, row in df.iterrows():
            try:
                nome = str(row.get('Nome Completo', '')).strip()
                email = str(row.get('Endereço de e-mail', '')).strip()
                
                if not nome or nome == 'nan':
                    continue
                
                nome = padronizar_nome(nome)
                
                if nome in orientadores_inseridos:
                    continue
                
                if not email or email == 'nan':
                    email = gerar_email_placeholder(nome, 'ifes')
                
                usuario = criar_usuario(
                    nome=nome,
                    email=email,
                    role='ORIENTADOR',
                    organizacao='IFES'
                )
                
                cod = inserir_usuario(usuario)
                
                if cod:
                    orientadores_inseridos.add(nome)
                    contador += 1
                    print(f"{nome} (Email: {email}) - ID: {cod}")
                else:
                    erros += 1
                    
            except Exception as e:
                erros += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nOrientadores inseridos: {contador} | Erros: {erros}")
        return orientadores_inseridos
        
    except Exception as e:
        print(f"Erro crítico na importação: {e}")
        return set()


def complementar_orientadores_processos(caminho_arquivo: str, orientadores_existentes: Set[str]) -> Set[str]:
    try:
        df = importar_csv(caminho_arquivo)
        contador = 0
        atualizados = 0
        erros = 0
        
        for index, row in df.iterrows():
            try:
                nome = str(row.get('Nome completo do avaliador Ifes do processo CAR', '')).strip()
                campus_nome = str(row.get('Campus', '')).strip()
                
                if not nome or nome == 'nan':
                    continue
                
                nome = padronizar_nome(nome)
                cod_campus = obter_cod_campus(campus_nome)

                if nome in orientadores_existentes:
                    usuario = usuario_repo.obter_por_nome(nome)
                    if usuario and cod_campus and usuario.cod_campus != cod_campus:
                        usuario.cod_campus = cod_campus
                        usuario_repo.atualizar(usuario)
                        atualizados += 1
                        print(f"{nome} - Campus atualizado para: {campus_nome}")
                    continue

                usuario = criar_usuario(
                    nome=nome,
                    email=gerar_email_placeholder(nome, 'ifes'),
                    role='ORIENTADOR',
                    organizacao='IFES',
                    cod_campus=cod_campus
                )
                
                cod = inserir_usuario(usuario)
                
                if cod:
                    orientadores_existentes.add(nome)
                    contador += 1
                    print(f"{nome} (Campus: {campus_nome}) - ID: {cod}")
                else:
                    erros += 1
                    
            except Exception as e:
                erros += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nNovos orientadores: {contador} | Atualizados: {atualizados} | Erros: {erros}")
        return orientadores_existentes
        
    except Exception as e:
        print(f"Erro crítico: {e}")
        return orientadores_existentes


def importar_consultores(caminho_arquivo: str, usuarios_existentes: Set[str]) -> None:
    try:
        df = importar_csv(caminho_arquivo)
        contador = 0
        erros = 0
        
        for index, row in df.iterrows():
            try:
                nome = str(row.get('Nome completo do ponto focal Idaf', '')).strip()
                campus_nome = str(row.get('Campus', '')).strip()
                
                if not nome or nome == 'nan':
                    continue

                nome = padronizar_nome(nome)
                
                if nome in usuarios_existentes:
                    continue
                
                cod_campus = obter_cod_campus(campus_nome)
                
                usuario = criar_usuario(
                    nome=nome,
                    email=gerar_email_placeholder(nome, 'idaf'),
                    role='CONSULTOR',
                    organizacao='IDAF',
                    cod_campus=cod_campus
                )
                
                cod = inserir_usuario(usuario)
                
                if cod:
                    usuarios_existentes.add(nome)
                    contador += 1
                    print(f"{nome} (Campus: {campus_nome}) - ID: {cod}")
                else:
                    erros += 1
                    
            except Exception as e:
                erros += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nConsultores inseridos: {contador} | Erros: {erros}")
        
    except Exception as e:
        print(f"Erro crítico: {e}")

def extrair_senha_telefone(telefone: str) -> str:
    if not telefone or telefone == 'nan':
        return 'PLACEHOLDER_SENHA'
    
    digitos = re.sub(r'\D', '', str(telefone))
    
    if len(digitos) >= 6:
        return digitos[-6:]
    
    return 'PLACEHOLDER_SENHA'

def importar_bolsistas(caminho_arquivo: str, usuarios_existentes: Set[str]) -> None:
    try:
        df = importar_csv(caminho_arquivo)
        contador = 0
        erros = 0
        sem_orientador = 0
        
        for index, row in df.iterrows():
            try:
                nome_bolsista = str(row.get('BOLSISTA', '')).strip()
                email_bolsista = str(row.get('E-MAIL', '')).strip()
                telefone_bolsista = str(row.get('TELEFONE', '')).strip()
                campus_nome = str(row.get('CAMPUS', '')).strip()
                nome_orientador = str(row.get('ORIENTADOR', '')).strip()
                
                if not nome_bolsista or nome_bolsista == 'nan':
                    continue
                
                nome_bolsista = padronizar_nome(nome_bolsista)
                nome_orientador = padronizar_nome(nome_orientador) if nome_orientador and nome_orientador != 'nan' else None
                
                if nome_bolsista in usuarios_existentes:
                    continue
                
                cod_campus = obter_cod_campus(campus_nome)
                
                cod_orientador = None
                if nome_orientador:
                    orientador = usuario_repo.obter_por_nome(nome_orientador)
                    if orientador:
                        cod_orientador = orientador.cod_usuario
                    else:
                        sem_orientador += 1
                        print(f"Orientador '{nome_orientador}' não encontrado para bolsista '{nome_bolsista}'")
                
                if not email_bolsista or email_bolsista == 'nan':
                    email_bolsista = gerar_email_placeholder(nome_bolsista, 'ifes')
                
                senha = extrair_senha_telefone(telefone_bolsista)
                
                usuario = Usuario(
                    cod_usuario=None,
                    cod_campus=cod_campus,
                    cod_orientador=cod_orientador,
                    nome_usuario=nome_bolsista,
                    email_usuario=email_bolsista,
                    senha_usuario=senha,
                    cpf_usuario='00000000000',
                    role_usuario='BOLSISTA',
                    organizacao_usuario='IFES'
                )
                
                cod = inserir_usuario(usuario)
                
                if cod:
                    usuarios_existentes.add(nome_bolsista)
                    contador += 1
                    orientador_info = f"Orientador: {nome_orientador}" if nome_orientador else "Sem orientador"
                    print(f"{nome_bolsista} (Campus: {campus_nome} - {orientador_info} - Senha: {senha}) - ID: {cod}")
                else:
                    erros += 1
                    
            except Exception as e:
                erros += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nBolsistas inseridos: {contador} | Sem orientador: {sem_orientador} | Erros: {erros}")
        
    except Exception as e:
        print(f"Erro crítico: {e}")


def importar_usuarios(orientadores_csv: str, processos_csv: str) -> None:
    # Etapa 1: Orientadores + email do arquivo orientadores.csv
    orientadores = importar_orientadores_csv(orientadores_csv)
    
    # Etapa 2: Complementar orientadores dos processos.csv
    todos_usuarios = complementar_orientadores_processos(processos_csv, orientadores)
    
    # Etapa 3: Consultores IDAF
    importar_consultores(processos_csv, todos_usuarios)

    # Etapa 4: Bolsistas
    importar_bolsistas(processos_csv, todos_usuarios)