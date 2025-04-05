# Teste Técnico - ANS

Este repositório contém a solução para um conjunto de desafios técnicos envolvendo web scraping, transformação de dados, banco de dados e desenvolvimento de uma API com interface frontend.

---

## 🧪 Estrutura dos Testes

### 1. Teste de Web Scraping (Python)

- Acesso automatizado ao site da ANS:  
  [ANS - Atualização do Rol](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos)

- Download automático dos anexos I e II (PDF)
- Compactação dos dois arquivos em `.zip`

📄 Código: `teste1_WebScraping.py`  
📦 Resultado: `anexos_compactados.zip`
📦 Resultado: `/downloads`

---

### 2. Teste de Transformação de Dados (Python)

- Extração de todas as tabelas do PDF dos Anexos
- Conversão para `.csv`
- Substituição de abreviações ("OD", "AMB", etc.) por descrições completas
- Compactação em `Teste_CaioMontenegro.zip`

📄 Código: `teste2_TranformacaoDados.py`  
📄 Arquivo gerado: `rol_procedimentos.csv`

---

### 3. Teste de Banco de Dados (PostgreSQL)

- Download dos demonstrativos contábeis (últimos 2 anos) e dos dados cadastrais de operadoras
- Criação de tabelas via SQL
- Importação dos dados CSV
- Queries analíticas:

  - Top 10 operadoras com maiores despesas em eventos médicos hospitalares no último trimestre
  - Top 10 no último ano

📂 Pasta: `scripts/`  
📄 Arquivos:  
- `create_table.sql`  
- `import_data.py`  
- `consulta1.sql`
- `consulta2.sql`

---

### 4. Teste de API + Frontend (Vue.js + Flask)

#### 🔁 Backend

- API Flask com endpoint `/busca`
- Permite busca textual por nome da operadora (razao_social ou nome_fantasia)

📄 Código: `BACKEND/app.py`  
📄 Requisitos: `BACKEND/requirements.txt`  
🌐 Exemplo de uso: `GET /busca?q=Unimed`

#### 🖼️ Frontend

- Interface web com Vue.js
- Campo de pesquisa + exibição dos resultados da API

📁 Código: `FRONTEND/src`  
📄 Configuração: `FRONTEND/.env`

#### 📬 Postman

Coleção com requisição à API para testes e demonstrações.

📁 Arquivo: `api-teste.postman_collection.json`

---

## ▶️ Como Rodar o Projeto

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+
- Git
- Postman

---

### 🔧 Clonar o repositório

git clone https://github.com/seu-usuario/projeto-teste.git
cd projeto-teste

### 🐍 Rodar o Backend (Flask + Python)

cd BACKEND
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
cp .env_sample .env
python app.py

### 🌐 Rodar o Frontend (Vue.js)

cd FRONTEND
npm install
npm run dev
