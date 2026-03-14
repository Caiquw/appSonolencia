# Sistema de Detecção de Sonolência

Sistema para detectar sonolência em funcionários usando visão computacional.

## Requisitos
- Python 3.10+
- PostgreSQL 17.9 instalado e rodando
- Webcam

## Instalação

1. Clone o repositório:
   git clone https://github.com/Caiquw/appSonolencia.git
   cd appSonolencia

2. Instale as dependências:
   pip install -r requirements.txt

3. Configure as variáveis de ambiente:
   - Renomeie o arquivo config.example.py para config.py
   - Crie um arquivo .env na raiz do projeto com:
     SENDGRID_API_KEY=SG.suachave
     DB_PASSWORD=sua_senha_postgres

4. Crie o banco de dados:
   python -c "
   import psycopg2
   conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='SUA_SENHA')
   conn.autocommit = True
   cur = conn.cursor()
   cur.execute('CREATE DATABASE sonolencia')
   print('Banco criado!')
   "

5. Crie a tabela:
   python -c "
   import psycopg2
   conn = psycopg2.connect(host='localhost', database='sonolencia', user='postgres', password='SUA_SENHA')
   cur = conn.cursor()
   cur.execute('''
       CREATE TABLE IF NOT EXISTS eventos_sonolencia (
           id           SERIAL PRIMARY KEY,
           funcionario  VARCHAR(100),
           inicio       TIMESTAMP,
           fim          TIMESTAMP,
           duracao_seg  FLOAT,
           ear_medio    FLOAT,
           camera_id    INT DEFAULT 0
       )
   ''')
   conn.commit()
   print('Tabela criada!')
   "

6. Execute o sistema:
   python main.py

## Como usar
- O sistema abre a webcam automaticamente
- Detecta se os olhos ficam fechados por muito tempo
- Dispara alarme sonoro ao detectar sonolência
- Ao pressionar Q, gera relatório e envia por e-mail ao supervisor
