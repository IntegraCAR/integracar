import sys
import os
import pandas as pd
import re
from typing import Set, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeders.importar_csv import importar_csv
from data.model.usuario import Usuario
from data.repo import usuario_repo, campus_repo

#Funções auxiliares
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
    return nome_limpo

def comparar_nomes(nome1: str, nome2: str) -> bool:
    def pegar_primeiro_segundo(nome):
        palavras = nome.split()
        palavras = [p for p in palavras if p.lower() not in {'de', 'da', 'do', 'dos', 'das', 'e'}]
        if len(palavras) >= 2:
            return f"{palavras[0]} {palavras[1]}"
        return palavras[0] if palavras else ""
    
    nome1_limpo = limpar_nome(pegar_primeiro_segundo(nome1))
    nome2_limpo = limpar_nome(pegar_primeiro_segundo(nome2))
    
    return nome1_limpo == nome2_limpo

def buscar_orientador(nome_orientador: str) -> Optional[Usuario]:
    if not nome_orientador:
        return None
    
    # Tentar busca exata primeiro
    orientador = usuario_repo.obter_por_nome(nome_orientador)
    if orientador:
        return orientador
    
    # Busca flexível: comparar com todos os orientadores
    todos = usuario_repo.obter_todos()
    for usuario in todos:
        if usuario.role_usuario == 'ORIENTADOR':
            if comparar_nomes(nome_orientador, usuario.nome_usuario):
                return usuario
    
    return None

def gerar_email_placeholder(nome: str, organizacao: str) -> str:
    nome_limpo = re.sub(r'[^a-z]', '', limpar_nome(nome))
    return f"placeholder_{nome_limpo}@{organizacao.lower()}.temporario"

def extrair_senha_telefone(telefone: str) -> str:
    if not telefone or telefone == 'nan':
        return 'PLACEHOLDER_SENHA'
    
    digitos = re.sub(r'\D', '', str(telefone))
    
    if len(digitos) >= 6:
        return digitos[-6:]
    
    return 'PLACEHOLDER_SENHA'


#Funções principais de importação
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
        
        df = df.drop_duplicates(subset=['Nome Completo'], keep='last')
        
        print(f"Total de orientadores únicos: {len(df)}\n")
        
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
        
        print(f"\nOrientadores inseridos: {contador} | Erros: {erros}\n")
        return orientadores_inseridos
        
    except Exception as e:
        print(f"Erro crítico na importação: {e}")
        return set()

def identificar_bolsistas_avaliadores(caminho_bolsistas: str, caminho_processos: str) -> Set[str]:
    try:
        df_bolsistas = importar_csv(caminho_bolsistas)
        df_processos = importar_csv(caminho_processos)
        
        bolsistas_nomes = set()
        for nome in df_bolsistas['BOLSISTA'].dropna():
            nome_limpo = limpar_nome(padronizar_nome(str(nome).strip()))
            bolsistas_nomes.add(nome_limpo)
        
        bolsistas_avaliadores = set()
        for nome in df_processos['Nome completo do avaliador Ifes do processo CAR'].dropna():
            nome_padrao = padronizar_nome(str(nome).strip())
            nome_limpo = limpar_nome(nome_padrao)
            if nome_limpo in bolsistas_nomes:
                bolsistas_avaliadores.add(nome_padrao)
        
        print(f"Bolsistas identificados como avaliadores: {len(bolsistas_avaliadores)}\n")
        return bolsistas_avaliadores
        
    except Exception as e:
        print(f"Erro ao identificar bolsistas avaliadores: {e}")
        return set()

def complementar_orientadores_processos(caminho_arquivo: str, orientadores_existentes: Set[str], bolsistas_avaliadores: Set[str]) -> Set[str]:
    try:
        df = importar_csv(caminho_arquivo)
        contador = 0
        atualizados = 0
        erros = 0
        ignorados_bolsistas = 0
        
        for index, row in df.iterrows():
            try:
                nome = str(row.get('Nome completo do avaliador Ifes do processo CAR', '')).strip()
                campus_nome = str(row.get('Campus', '')).strip()
                
                if not nome or nome == 'nan':
                    continue
                
                nome = padronizar_nome(nome)
                
                if nome in bolsistas_avaliadores:
                    ignorados_bolsistas += 1
                    continue
                
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
        
        print(f"\nNovos orientadores: {contador}")
        print(f"Atualizados: {atualizados}")
        print(f"Ignorados (são bolsistas): {ignorados_bolsistas}")
        print(f"Erros: {erros}\n")
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

def importar_bolsistas(caminho_arquivo: str, usuarios_existentes: Set[str]) -> None:
    try:
        df = importar_csv(caminho_arquivo)
        
        df_car = df[df['CATEGORIA'].str.upper().str.strip() == 'CAR']
        
        print(f"Total de bolsistas CAR encontrados: {len(df_car)}\n")
        
        contador = 0
        erros = 0
        sem_orientador = 0
        
        for index, row in df_car.iterrows():
            try:
                nome_bolsista = str(row['BOLSISTA']).strip()
                email_bolsista = str(row.get('E-MAIL', '')).strip().lower()
                telefone_bolsista = str(row.get('TELEFONE', '')).strip()
                campus_nome = str(row.get('CAMPUS', '')).strip()
                nome_orientador = str(row.get('ORIENTADOR', '')).strip()
                
                if not nome_bolsista or nome_bolsista == 'nan' or len(nome_bolsista) < 3:
                    print(f"Bolsista inválido na linha {index + 2}: '{nome_bolsista}'")
                    continue
                
                nome_bolsista = padronizar_nome(nome_bolsista)
                nome_orientador = padronizar_nome(nome_orientador) if nome_orientador and nome_orientador != 'nan' else None
                
                if nome_bolsista in usuarios_existentes:
                    print(f"Bolsista '{nome_bolsista}' já existe, pulando...")
                    continue
                
                cod_campus = obter_cod_campus(campus_nome)
                
                cod_orientador = None
                if nome_orientador:
                    # Usar busca flexível
                    orientador = buscar_orientador(nome_orientador)
                    if orientador:
                        cod_orientador = orientador.cod_usuario
                        print(f"  -> Orientador encontrado: {orientador.nome_usuario}")
                    else:
                        sem_orientador += 1
                        print(f"  -> Orientador '{nome_orientador}' não encontrado")
                
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
                    print(f"{nome_bolsista} - ID: {cod}")
                else:
                    erros += 1
                    print(f"Erro ao inserir '{nome_bolsista}'")
                    
            except Exception as e:
                erros += 1
                print(f"Erro linha {index + 2}: {e}")
        
        print(f"\nInseridos: {contador}")
        print(f"Sem orientador: {sem_orientador}")
        print(f"Erros: {erros}\n")
        
    except Exception as e:
        print(f"Erro crítico: {e}")
        import traceback
        traceback.print_exc()

#Função principal
def importar_usuarios(orientadores_csv: str, processos_csv: str, bolsistas_csv: str) -> None:
    # Etapa 0: Identificar bolsistas que aparecem como avaliadores
    bolsistas_avaliadores = identificar_bolsistas_avaliadores(bolsistas_csv, processos_csv)

    # Etapa 1: Orientadores + email do arquivo orientadores.csv
    orientadores = importar_orientadores_csv(orientadores_csv)
    
    # Etapa 2: Complementar orientadores dos processos.csv
    todos_usuarios = complementar_orientadores_processos(processos_csv, orientadores, bolsistas_avaliadores)
    
    # Etapa 3: Consultores IDAF
    importar_consultores(processos_csv, todos_usuarios)

    # Etapa 4: Bolsistas CAR
    importar_bolsistas(bolsistas_csv, todos_usuarios)
