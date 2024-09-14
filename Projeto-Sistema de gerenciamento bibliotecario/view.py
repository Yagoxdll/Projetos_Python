# CRUD é um conceito central em desenvolvimento de software que descreve as quatro operações essenciais para manipulação de dados em um sistema. 
# Ele engloba a criação de novos registros, a leitura de dados existentes, a atualização de informações e a exclusão de registros 
# que não são mais necessários. 
# Essas operações formam a base de interações com bancos de dados e são fundamentais para o funcionamento de aplicações que lidam com dados 
# persistentes.

# A ideia por trás do CRUD é fornecer uma estrutura clara e organizada para manipular dados de forma eficiente e segura. 
#  Ao utilizar esses quatro pilares, desenvolvedores podem criar sistemas que permitem aos usuários gerenciar informações 
# de maneira intuitiva e confiável. 
# Além disso, o CRUD serve como uma base sólida sobre a qual funcionalidades mais complexas podem ser construídas, garantindo 
# que as operações básicas de manipulação de dados sejam tratadas de forma consistente e robusta.

import psycopg2


def connect(passwd):
    try:
        conectar = psycopg2.connect(
            dbname="postgres",
            user="postgres",  # ou o usuário que você estiver usando
            password=passwd,  # Substitua pela sua senha
            host="localhost",
            port="5432"
        )
        return conectar
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

# Teste de Conexão
def test_connection(passwd):
    conectar = connect(passwd)
    if conectar:
        print("Conexão bem-sucedida!")
        conectar.close()
    else:
        print("Falha na conexão.")


def how_many_books(passwd):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("SELECT COUNT(*) FROM livros")
        numero_de_linhas = cursor.fetchone()[0]
        return numero_de_linhas
    except psycopg2.Error as e:
        return f"Erro ao contar livros: {e}"
    finally:
        if conectar:
            conectar.close()

def how_many_users(passwd):
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        numero_de_linhas = cursor.fetchone()[0]
        return numero_de_linhas
    except psycopg2.Error as e:
        return f"Erro ao contar usuários: {e}"
    finally:
        if conectar:
            conectar.close()

def how_many_loans(passwd):
    conectar = None
    try:
        conectar = connect(passwd,)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE data_devolucao IS NULL
        """)
        numero_de_linhas = cursor.fetchone()[0]
        return numero_de_linhas
    except psycopg2.Error as e:
        return f"Erro ao contar empréstimos: {e}"
    finally:
        if conectar:
            conectar.close()

def insert_book(passwd, titulo, autor, editora, ano_publicacao, isbn):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn) VALUES (%s, %s, %s, %s, %s)", 
                       (titulo, autor, editora, ano_publicacao, isbn))
        conectar.commit()
        return "Livro inserido com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao inserir livro: {e}"
    finally:
        if conectar:
            conectar.close()

def insert_user(passwd, nome, sobrenome, bairro, rua, numero, email, telefone):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("INSERT INTO usuarios(nome, sobrenome, bairro, rua, numero, email, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (nome, sobrenome, bairro, rua, numero, email, telefone))
        conectar.commit()
        return "Usuário inserido com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao inserir usuário: {e}"
    finally:
        if conectar:
            conectar.close()

def get_user(passwd):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        return users
    except psycopg2.Error as e:
        return f"Erro ao buscar usuários: {e}"
    finally:
        if conectar:
            conectar.close()

def get_books(passwd):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor(passwd)
        cursor.execute("SELECT * FROM livros")
        books = cursor.fetchall()
        return books
    except psycopg2.Error as e:
        return f"Erro ao buscar livros: {e}"
    finally:
        if conectar:
            conectar.close()

def verify_available_book(passwd, id_livro_test):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id_livro = %s AND data_devolucao IS NULL
        """, (id_livro_test,))
        emprestimos_pendentes = cursor.fetchone()[0]
        return emprestimos_pendentes == 0
    except psycopg2.Error as e:
        return f"Erro ao verificar disponibilidade do livro: {e}"
    finally:
        if conectar:
            conectar.close()

def verify_book_exist(passwd, id_livro_test):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM livros
            WHERE id = %s
        """, (id_livro_test,))
        livro_existente = cursor.fetchone()[0]
        return livro_existente > 0
    except psycopg2.Error as e:
        return f"Erro ao verificar existência do livro: {e}"
    finally:
        if conectar:
            conectar.close()

def verify_user_exist(passwd, id_usuario_test):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios
            WHERE id = %s
        """, (id_usuario_test,))
        usuario_existente = cursor.fetchone()[0]
        return usuario_existente > 0
    except psycopg2.Error as e:
        return f"Erro ao verificar existência do usuário: {e}"
    finally:
        if conectar:
            conectar.close()

def verify_loan_exist(passwd, id_emprestimo_test):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id = %s
        """, (id_emprestimo_test,))
        emprestimo_existe = cursor.fetchone()[0]
        return emprestimo_existe > 0
    except psycopg2.Error as e:
        return f"Erro ao verificar existência do empréstimo: {e}"
    finally:
        if conectar:
            conectar.close()

def verify_available_loan(passwd, id_emprestimo):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id = %s AND data_devolucao IS NULL
        """, (id_emprestimo,))
        emprestimos_pendentes = cursor.fetchone()[0]
        return emprestimos_pendentes == 1
    except psycopg2.Error as e:
        return f"Erro ao verificar empréstimo disponível: {e}"
    finally:
        if conectar:
            conectar.close()

def insert_loan(passwd, id_livro, id_usuario, data_emprestimo, data_devolucao):
    conectar = None
    try:
        conectar = connect(passwd )
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("INSERT INTO emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao) VALUES (%s, %s, %s, %s)", 
                       (id_livro, id_usuario, data_emprestimo, data_devolucao))
        conectar.commit()
        return "Empréstimo registrado com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao registrar empréstimo: {e}"
    finally:
        if conectar:
            conectar.close()

def return_loan(passwd, id_emprestimo, data_devolucao):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("UPDATE emprestimos SET data_devolucao = %s WHERE id = %s", 
                       (data_devolucao, id_emprestimo))
        conectar.commit()
        return "Empréstimo devolvido com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao registrar devolução: {e}"
    finally:
        if conectar:
            conectar.close()

def get_loans_with_return_date(passwd):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT emprestimos.id, livros.titulo, usuarios.nome, emprestimos.data_emprestimo, emprestimos.data_devolucao
            FROM emprestimos
            INNER JOIN livros ON emprestimos.id_livro = livros.id
            INNER JOIN usuarios ON emprestimos.id_usuario = usuarios.id
            WHERE emprestimos.data_devolucao IS NOT NULL
        """)
        loans_with_return_date = cursor.fetchall()
        return loans_with_return_date
    except psycopg2.Error as e:
        return f"Erro ao buscar empréstimos com data de devolução: {e}"
    finally:
        if conectar:
            conectar.close()

def get_books_on_loan(passwd):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT livros.titulo, usuarios.nome, emprestimos.id, emprestimos.data_emprestimo, emprestimos.data_devolucao
            FROM livros
            INNER JOIN emprestimos ON livros.id = emprestimos.id_livro
            INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario
            WHERE emprestimos.data_devolucao IS NULL
        """)
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        return f"Erro ao buscar livros emprestados: {e}"
    finally:
        if conectar:
            conectar.close()

def delete_user(passwd, id_user):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id_user,))
        result = cursor.fetchone()
        if result is None:
            return "Usuário não encontrado."
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_user,))
        conectar.commit()
        return "Usuário deletado com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao deletar usuário: {e}"
    finally:
        if conectar:
            conectar.close()

def delete_book(passwd, id_book):
    conectar = None
    try:
        conectar = connect(passwd)
        if conectar is None:
            raise Exception("Conexão falhou.")
        cursor = conectar.cursor()
        cursor.execute("SELECT id FROM livros WHERE id = %s", (id_book,))
        result = cursor.fetchone()
        if result is None:
            return "Livro não encontrado."
        cursor.execute("DELETE FROM livros WHERE id = %s", (id_book,))
        conectar.commit()
        return "Livro deletado com sucesso!"
    except psycopg2.Error as e:
        return f"Erro ao deletar livro: {e}"
    finally:
        if conectar:
            conectar.close()


