# Frontend IntegraCAR - Next.js

Tela de login do sistema IntegraCAR desenvolvida com Next.js, TypeScript, Tailwind CSS e Shadcn/UI.

## 🚀 Tecnologias

- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Shadcn/UI** - Componentes UI
- **Lucide React** - Ícones

## 📦 Instalação

1. Navegue até a pasta frontend:
```powershell
cd frontend
```

2. Instale as dependências:
```powershell
npm install
```

## ⚙️ Configuração

1. O arquivo `.env.local` já está configurado com a URL padrão do backend:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

2. Certifique-se de que o backend FastAPI está rodando na porta 8000.

## 🎨 Logo

A logo do projeto deve estar em `frontend/public/logo_login.jpg`. Copie a logo da pasta `static/img/logo_login.jpg` para a pasta `public`:

```powershell
# Crie a pasta public se não existir
mkdir public

# Copie a logo
copy ..\static\img\logo_login.jpg public\logo_login.jpg
```

## 🏃‍♂️ Executar

Inicie o servidor de desenvolvimento:

```powershell
npm run dev
```

O aplicativo estará disponível em: **http://localhost:3000**

## 🔗 Integração com Backend

A tela de login faz uma requisição POST para `http://127.0.0.1:8000/login` com os seguintes dados:
- `email` - Email do usuário
- `senha` - Senha do usuário

O backend FastAPI deve retornar um redirect para a página apropriada baseado no `role_usuario`.

## 📝 Scripts Disponíveis

- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Cria a versão de produção
- `npm start` - Inicia o servidor de produção
- `npm run lint` - Executa o linter

## 🎨 Design

A tela de login replica o design fornecido com:
- Layout responsivo dividido em duas colunas
- Lado esquerdo: Logo e call-to-action para criar conta
- Lado direito: Formulário de login com gradiente azul
- Campos de email e senha com validação
- Botão de mostrar/ocultar senha
- Checkbox "Permanecer conectado"
- Link "Esqueceu sua senha?"
- Mensagens de erro integradas

## 🔒 Segurança

- Senhas são ocultadas por padrão com opção de visualização
- Validação de campos obrigatórios
- Tratamento de erros de autenticação
- Cookies de sessão gerenciados pelo backend
