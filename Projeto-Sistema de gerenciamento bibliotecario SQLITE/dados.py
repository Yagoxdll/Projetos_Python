import sqlite3

def dados_create():
    # Conecta ao banco de dados
    conectar = sqlite3.connect("data.db")

    # Cria uma tabela de livros, se não existir
    conectar.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            isbn TEXT UNIQUE
        )
    ''')

    # Cria tabela de usuários, se não existir
    conectar.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT,
            bairro TEXT,
            rua TEXT,
            numero TEXT,
            email TEXT UNIQUE,
            telefone TEXT
        )
    ''')

    # Cria tabela de empréstimos de livros, se não existir
    conectar.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER,
            id_usuario INTEGER,
            data_emprestimo DATE,
            data_devolucao DATE,
            FOREIGN KEY (id_livro) REFERENCES livros(id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
    ''')

    # Fecha a conexão com o banco de dados
    conectar.commit()
    conectar.close()
