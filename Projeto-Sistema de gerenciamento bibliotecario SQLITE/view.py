
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


import sqlite3

def connect():
    return sqlite3.connect("data.db")


# Função que conta quantos livros há no banco
def how_many_books():
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT COUNT(*) FROM livros")
        numero_de_linhas = cursor.fetchone()[0]  # Obtém o primeiro valor da primeira linha
        return numero_de_linhas
    except sqlite3.Error as e:
        return 0  
    finally:
        conectar.close()

# Função que conta quantos usuarios há no banco
def how_many_users():
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        numero_de_linhas = cursor.fetchone()[0]  # Obtém o primeiro valor da primeira linha
        return numero_de_linhas
    except sqlite3.Error as e:
        return 0  
    finally:
        conectar.close()

# Função que conta quantos empréstimos há no banco
def how_many_loans():
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE  data_devolucao IS NULL
        """)
        numero_de_linhas = cursor.fetchone()[0]  # Obtém o primeiro valor da primeira linha
        return numero_de_linhas
    except sqlite3.Error as e:
        return 0  
    finally:
        conectar.close()

# Função que insere livros na tabela
def insert_book(titulo, autor, editora, ano_publicacao, isbn):
    try:
        conectar = connect()
        conectar.execute("INSERT INTO livros(titulo, autor, editora, ano_publicacao, isbn)\
                          VALUES (?, ?, ?, ?, ?)", (titulo, autor, editora, ano_publicacao, isbn))
        conectar.commit()
    except Exception:
        return
    finally:
        conectar.close()

# Função que insere usuários
def insert_user(nome, sobrenome, bairro, rua, numero, email, telefone):
    try:
        conectar = connect()
        conectar.execute("INSERT INTO usuarios(nome, sobrenome, bairro, rua, numero, email, telefone)\
                         VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, sobrenome, bairro, rua, numero, email, telefone))
        conectar.commit()
    except Exception:
        return
    finally:
        conectar.close()

# Função que lista todos os usuários
def get_user():
    try:
        conectar = connect()
        c = conectar.cursor()
        c.execute("SELECT * FROM usuarios")
        users = c.fetchall()
        conectar.close()
        return users
    except Exception:
        return []

# Função que retorna todos os livros
def get_books():
    try:
        conectar = connect()
        c = conectar.cursor()
        c.execute("SELECT * FROM livros")
        books = c.fetchall()
        conectar.close()
        return books
    except Exception:
        return []

# Função que verifica se livro se encontra disponível
def verify_available_book(id_livro_test):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id_livro = ? AND data_devolucao IS NULL
        """, (id_livro_test,))
        emprestimos_pendentes = cursor.fetchone()[0]
        conectar.close()
        return emprestimos_pendentes == 0
    except Exception:
        return False

# Função que verifica se o livro existe pelo seu id
def verify_book_exist(id_livro_test):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM livros
            WHERE id = ?
        """, (id_livro_test,))
        livro_existente = cursor.fetchone()[0]
        conectar.close()
        return livro_existente > 0
    except Exception:
        return False

# Função que verifica se usuário existe pelo seu id
def verify_user_exist(id_usuario_test):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios
            WHERE id = ?
        """, (id_usuario_test,))
        usuario_existente = cursor.fetchone()[0]
        conectar.close()
        return usuario_existente > 0
    except Exception:
        return False

# Função que verifica se empréstimo existe pelo seu id
def verify_loan_exist(id_emprestimo_test):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id = ?
        """, (id_emprestimo_test,))
        emprestimo_existe = cursor.fetchone()[0]
        conectar.close()
        return emprestimo_existe > 0
    except Exception:
        return False

# Função que define se o empréstimo de um livro é válido pelo seu id 
#e se o campo data_devolucao ainda está como NULL
#caso retorne como falsom não será validado

def verify_available_loan(id_emprestimo):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emprestimos
            WHERE id = ? AND data_devolucao IS NULL
        """, (id_emprestimo,))
        emprestimos_pendentes = cursor.fetchone()[0]
        conectar.close()
        return emprestimos_pendentes == 1
    except Exception:
        return False

# Função que realiza empréstimo
def insert_loan(id_livro, id_usuario, data_emprestimo, data_devolucao):
    try:
        conectar = connect()
        conectar.execute("INSERT INTO emprestimos(id_livro, id_usuario, data_emprestimo, data_devolucao)\
                         VALUES(?, ?, ?, ?)", (id_livro, id_usuario, data_emprestimo, data_devolucao))
        conectar.commit()
    except Exception:
        return
    finally:
        conectar.close()

# Função que retorna um empréstimo pelo seu id
def return_loan(id_emprestimo, data_devolucao):
    try:
        conectar = connect()
        conectar.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (data_devolucao, id_emprestimo))
        conectar.commit()
    except Exception:
        return
    finally:
        conectar.close()

# Função que mostra os empréstimos que já foram devolvidos
def get_loans_with_return_date():
    try:
        conectar = connect()
        cursor = conectar.cursor()
        
        # Seleciona ID do empréstimo, nome do livro, nome do usuário e as datas
        cursor.execute("""
            SELECT emprestimos.id, livros.titulo, usuarios.nome, emprestimos.data_emprestimo, emprestimos.data_devolucao
            FROM emprestimos
            INNER JOIN livros ON emprestimos.id_livro = livros.id
            INNER JOIN usuarios ON emprestimos.id_usuario = usuarios.id
            WHERE emprestimos.data_devolucao IS NOT NULL
        """)
        
        loans_with_return_date = cursor.fetchall()
        conectar.close()
        return loans_with_return_date
    except Exception:
        return []



# Função que mostra todos os empréstimos
def get_books_on_loan():
    try:
        conectar = connect()
        result = conectar.execute(
            "SELECT livros.titulo, usuarios.nome, emprestimos.id, emprestimos.data_emprestimo, emprestimos.data_devolucao \
             FROM livros \
             INNER JOIN emprestimos ON livros.id = emprestimos.id_livro \
             INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario \
             WHERE emprestimos.data_devolucao IS NULL").fetchall()
        conectar.close()
        return result
    except Exception:
        return []

# Função que deleta usuário pelo seu id
def delete_user(id_user):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (id_user,))
        result = cursor.fetchone()
        if result is None:
            return False
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_user,))
        conectar.commit()
        return True
    except Exception:
        return False
    finally:
        conectar.close()

# Função que deleta livro pelo seu id
def delete_book(id_book):
    try:
        conectar = connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT id FROM livros WHERE id = ?", (id_book,))
        result = cursor.fetchone()
        if result is None:
            return False
        cursor.execute("DELETE FROM livros WHERE id = ?", (id_book,))
        conectar.commit()
        return True
    except Exception:
        return False
    finally:
        conectar.close()


