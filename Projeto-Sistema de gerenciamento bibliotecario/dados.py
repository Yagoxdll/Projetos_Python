import psycopg2

def dados_create(passwd):
    # Conecta ao banco de dados PostgreSQL
    conectar = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=passwd,
        host="localhost",
        port="5432"
    )

    # Defina a codificação do cliente como UTF-8
    cursor = conectar.cursor()
    cursor.execute("SET client_encoding TO 'UTF8';")

    # Cria as tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            sobrenome TEXT,
            bairro TEXT,
            rua TEXT,
            numero TEXT,
            email TEXT UNIQUE,
            telefone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id SERIAL PRIMARY KEY,
            id_livro INTEGER REFERENCES livros(id),
            id_usuario INTEGER REFERENCES usuarios(id),
            data_emprestimo DATE,
            data_devolucao DATE
        )
    ''')

    # Fecha o cursor e a conexão com o banco de dados
    conectar.commit()
    cursor.close()
    conectar.close()

