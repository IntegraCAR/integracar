#CUIDADO AO UTILIZAR ESSE SCRIPTS!!!
#O objetivo desse arquivo é reinserir as tabelas com os novos ajustes no banco
#SEM GUARDAR AS INFORMAÇÕES PRESENTES NO BANCO ANTERIORMENTE
from util.database import get_connection

#Deletando as tabelas antigas
try:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        DROP TABLE IF EXISTS AnaliseProcessos CASCADE;
                        DROP TABLE IF EXISTS Usuario CASCADE;
                        DROP TABLE IF EXISTS Processo CASCADE;
                        DROP TABLE IF EXISTS Notificacao CASCADE;
                        DROP TABLE IF EXISTS Campus CASCADE;
                        DROP TABLE IF EXISTS Status CASCADE;
                        """)
        conn.commit()
        cursor.close()
except Exception as e:
    print(f"Erro ao deletar tabela: {e}")

#Recriando as tabelas
from data.repo import usuario_repo
from data.repo import status_repo
from data.repo import campus_repo
from data.repo import notificacao_repo
from data.repo import processo_repo
from data.repo import analise_processos_repo

campus_repo.criar_tabela()
status_repo.criar_tabela()
processo_repo.criar_tabela()
notificacao_repo.criar_tabela()
usuario_repo.criar_tabela()
analise_processos_repo.criar_tabela()

#Reinserir dados dos campus
from seeders.importar_campus import importar_campus
#importar_campus("processos.csv")