# 🌿 IntegraCAR

Sistema de Gestão de Análises de Processos Ambientais desenvolvido com FastAPI e Supabase.

## � Sobre o Projeto

O **IntegraCAR** é um sistema para gerenciamento de processos de análise ambiental, permitindo o controle de:
- Campus universitários
- Usuários e suas permissões
- Processos ambientais (EDOCS, processos florestais, empreendimentos)
- Status de análises
- Notificações
- Análises de processos com prazos e acompanhamento

---

## 🛠️ Stack Tecnológico

### **Backend**
- ![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white) **Python 3.12**
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?logo=fastapi&logoColor=white) **FastAPI 0.115.5** - Framework web moderno e rápido
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32.1-green) **Uvicorn 0.32.1** - Servidor ASGI
- **Jinja2 3.1.4** - Template engine para HTML

### **Banco de Dados**
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white) **PostgreSQL** (via Supabase)
- ![Supabase](https://img.shields.io/badge/Supabase-BaaS-3ECF8E?logo=supabase&logoColor=white) **Supabase** - Backend-as-a-Service
- **psycopg2-binary 2.9.11** - Driver PostgreSQL

### **Gerenciamento de Dados**
- **pandas 2.3.3** - Análise e manipulação de dados
- **numpy 2.3.4** - Computação numérica
- **python-dotenv 1.1.1** - Variáveis de ambiente

### **Utilitários**
- **python-dateutil 2.9.0** - Manipulação de datas
- **pytz 2025.2** - Suporte a timezones
- **python-multipart 0.0.18** - Upload de arquivos
- **itsdangerous 2.2.0** - Segurança de sessões

### **Padrões de Arquitetura**
- ✅ Repository Pattern
- ✅ MVC (Model-View-Controller)
- ✅ Data Classes para Models
- ✅ Context Managers
- ✅ Row Level Security (RLS)

---

## 📁 Estrutura do Projeto

```
integracar/
├── data/
│   ├── model/              # Models com dataclasses
│   │   ├── campus.py
│   │   ├── usuario.py
│   │   ├── processo.py
│   │   ├── status.py
│   │   ├── notificacao.py
│   │   └── analise_processos.py
│   ├── repo/               # Repositórios (acesso a dados)
│   │   ├── campus_repo.py
│   │   ├── usuario_repo.py
│   │   ├── processo_repo.py
│   │   ├── status_repo.py
│   │   ├── notificacao_repo.py
│   │   └── analise_processos_repo.py
│   └── sql/                # Queries SQL
│       ├── campus_sql.py
│       ├── usuario_sql.py
│       ├── processo_sql.py
│       ├── status_sql.py
│       ├── notificacao_sql.py
│       └── analise_processos_sql.py
├── routes/
│   └── publico/            # Rotas públicas da aplicação
│       └── publico_inicio.py
├── templates/
│   └── publico/            # Templates HTML
│       └── inicio.html
├── util/
│   └── database.py         # Utilitários de banco de dados
├── conexao_db.py           # Gerenciamento de conexão
├── main.py                 # Aplicação FastAPI principal
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Exemplo de variáveis de ambiente
└── .gitignore              # Arquivos ignorados pelo Git
```

---

## 🚀 Instalação e Configuração

### 1. **Clone o Repositório**

```bash
git clone https://github.com/IntegraCAR/integracar.git
cd integracar
```

### 2. **Criar Ambiente Virtual**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 4. **Configurar Variáveis de Ambiente**

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Supabase:

```env
DB_USER=postgres.seu_projeto_ref
DB_PASSWORD=sua_senha_aqui
DB_HOST=aws-1-us-east-1.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
```

**📌 Como obter as credenciais do Supabase:**

1. Acesse [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto
3. Vá em **Settings** → **Database**
4. Procure por **Connection Pooling** → **Session Mode**
5. Copie a connection string do pooler (IPv4)

### 5. **Criar Tabelas no Banco**

```bash
python criar_tabelas_repo.py
```

### 6. **Verificar Instalação**

```bash
python verificar_tabelas.py
```

---

## 🎮 Executando a Aplicação

### **Modo Desenvolvimento**

```bash
python main.py
```

Ou com uvicorn:

```bash
uvicorn main:app --reload
```

### **Acessar a Aplicação**

Abra o navegador em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **Documentação API (Swagger)**

Acesse: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📊 Estrutura do Banco de Dados

### **Tabelas Principais**

1. **Campus** - Cadastro dos campus universitários
   - `cod_campus` (PK)
   - `nome_campus`

2. **Usuario** - Usuários do sistema
   - `cod_usuario` (PK)
   - `cod_campus` (FK)
   - `nome_usuario`
   - `role_usuario`
   - `organizacao_usuario`

3. **Processo** - Processos ambientais
   - `cod_processo` (PK)
   - `codigo_edocs`
   - `numero_processo_florestal`
   - `codigo_empreendimento`

4. **Status** - Status das análises
   - `cod_status` (PK)
   - `tipo_status`
   - `data_hora_ultima_atualizacao`

5. **Notificacao** - Notificações do sistema
   - `cod_notificacao` (PK)
   - `motivo_notificacao`

6. **Analise_Processos** - Análises de processos
   - `cod_analise` (PK)
   - `data_hora_inicio_analise`
   - `data_previsao_fim_analise`
   - `cod_campus` (FK)
   - `cod_usuario` (FK)
   - `cod_status` (FK)
   - `cod_notificacao` (FK)
   - `cod_processo` (FK)

---

## � Exemplos de Uso

### **Listar Campus**

```python
from data.repo import campus_repo

campus_list = campus_repo.obter_todos()
for campus in campus_list:
    print(f"{campus.cod_campus} - {campus.nome_campus}")
```

### **Inserir Usuário**

```python
from data.repo import usuario_repo
from data.model.usuario import Usuario

usuario = Usuario(
    cod_usuario=0,
    cod_campus=1,
    nome_usuario="João Silva",
    role_usuario="Analista",
    organizacao_usuario="UFSC"
)

cod = usuario_repo.inserir(usuario)
print(f"Usuário inserido com ID: {cod}")
```

### **Buscar Análises por Campus**

```python
from data.repo import analise_processos_repo

analises = analise_processos_repo.obter_por_campus(1)
for analise in analises:
    print(f"Análise {analise.cod_analise} - Status: {analise.cod_status}")
```

---

## 🔐 Segurança

- ✅ Variáveis de ambiente para credenciais sensíveis
- ✅ Arquivo `.env` não versionado (`.gitignore`)
- ✅ Conexão SSL/TLS com Supabase
- ✅ Row Level Security (RLS) habilitado
- ✅ Session middleware para autenticação (preparado)

**⚠️ IMPORTANTE:** 
- Nunca commite o arquivo `.env`
- Use senhas fortes
- Em produção, use `https_only=True` no middleware

---

## 🧪 Scripts Utilitários

- **`criar_tabelas_repo.py`** - Cria todas as tabelas no banco
- **`verificar_tabelas.py`** - Verifica estrutura e dados das tabelas
- **`configurar_rls.py`** - Configura Row Level Security
- **`exemplo_models.py`** - Exemplos de uso dos models
- **`consultas_exemplo_v2.py`** - Exemplos de consultas SQL

---

## 📚 Documentação Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📧 Contato

**IntegraCAR Team**
- GitHub: [@IntegraCAR](https://github.com/IntegraCAR)
- Email: contato@integracar.com.br

---

## 🙏 Agradecimentos

- Equipe de desenvolvimento UFSC
- Comunidade FastAPI
- Supabase Team

---

<div align="center">
  
**Desenvolvido com ❤️ pela equipe IntegraCAR**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-BaaS-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)

</div>
    cursor.close()
    conn.close()
```

### Importar CSV

```python
from importar_csv import importar_csv

df = importar_csv('seu_arquivo.csv')
print(df.head())
```

### Exemplos Completos

Execute o arquivo de exemplos:

```bash
python exemplo_uso.py
```

## 📁 Estrutura do Projeto

```
integracar/
├── conexao_db.py       # Módulo de conexão com Supabase
├── importar_csv.py     # Módulo para importar arquivos CSV
├── exemplo_uso.py      # Exemplos de uso
├── .env                # Credenciais (não commitar!)
├── .env.example        # Template de configuração
└── README.md           # Este arquivo
```

## ⚠️ Segurança

- **NUNCA** commite o arquivo `.env` no Git
- Adicione `.env` ao `.gitignore`
- Use senhas fortes para o banco de dados

## 📚 Documentação

- [Supabase Database](https://supabase.com/docs/guides/database)
- [psycopg2](https://www.psycopg.org/docs/)
- [pandas](https://pandas.pydata.org/docs/)
