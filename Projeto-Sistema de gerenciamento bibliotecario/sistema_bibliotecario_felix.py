from tkinter.ttk import *
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
from dados import *
from view import *
from datetime import datetime
import os
import sys

# Variáveis de tema e personalização
cor_branca = "#feffff"
cor_primaria = "#4F4F4F"
cor_secundaria_segunda_camada = "#808080"
cor_navajo_white = "#A9A9A9"
cor_primaria_segunda_janela = "#7c7c7f"
credentials = None


# Função que define ícone de todas as janelas
def definir_icone(janela):
    icon_path = os.path.join(os.path.dirname(__file__), "main_ico.ico")
    janela.iconbitmap(icon_path)


class Login:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x150")
        self.root.title("Login")
        self.root.resizable(False, False)

        # Label para a senha
        self.label_text1 = Label(self.root, text="PostgreSQL Password", font='Arial 15')
        self.label_text1.pack(pady=10)

        # Campo de entrada para a senha
        self.entry_credential = Entry(self.root, show="*")
        self.entry_credential.pack(pady=5)

        # Botão de login
        self.login_button = Button(self.root, text="Login", command=self.get_password)
        self.login_button.pack(pady=20)

        # Vincula a tecla "Enter" ao método get_password
        self.root.bind('<Return>', self.enter_key_pressed)

        definir_icone(self.root)

        # Configurações do banco de dados
        self.dbname = "postgres"
        self.user = "postgres"
        self.host = "localhost"

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Intercepta o evento de fechamento da janela

        self.root.mainloop()

    def on_close(self):
        # Pergunta ao usuário se ele quer sair
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.root.destroy()  # Fecha a janela
            sys.exit()  # Fecha a aplicação

    def enter_key_pressed(self, event):
        # Método para lidar com o evento de tecla "Enter" pressionada
        self.get_password()

    def get_password(self):
        # Obtem a senha inserida no campo de entrada
        self.admin_password = self.entry_credential.get()

        if not self.admin_password:
            messagebox.showerror("Erro", "Você deve digitar uma senha!")
            return

        # Tenta autenticar no banco de dados
        try:
            if self.authenticate():
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.root.destroy()  # Fecha a janela de login
                global credentials
                credentials = self.admin_password
                # Continue com a lógica da aplicação
        except:
            messagebox.showerror("Erro", "Senha incorreta! Acesso negado.")
            self.entry_credential.delete(0, END)  # Limpa o campo de entrada

    def authenticate(self):
        try:
            # Tenta conectar ao banco de dados com a senha fornecida
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.admin_password,
                host=self.host
            )
            connection.close()  # Fecha a conexão se for bem-sucedida
            return True
        except psycopg2.OperationalError:
            return False


class TelaInicial:

    def __init__(self, master):

        # Cria a janela mestre da aplicação
        self.master = master
        self.master.title("")

        # Geometria da aplicação
        self.master.geometry("800x400")
        self.master.resizable(width=False, height=False)

        # Menus
        self.barra_menu = Menu(self.master)

        # Menu Arquivo
        self.menu_arquivo = Menu(self.barra_menu, tearoff=0)
        self.menu_arquivo.add_command(label="Sair", command=self.sair)
        

        # Menu Gerenciar
        self.menu_gerenciar = Menu(self.barra_menu, tearoff=0)
        self.menu_gerenciar.add_command(label="Novo Usuário", command=self.abrir_novo_usuario)
        self.menu_gerenciar.add_command(label="Novo Livro", command=self.abrir_novo_livro)

        # Menu Listar
        self.menu_listar = Menu(self.barra_menu, tearoff=0)
        self.menu_listar.add_command(label="Listar Usuários", command=self.abrir_listar_usuarios)
        self.menu_listar.add_command(label="Listar Livros", command=self.abrir_listar_livros)
        self.menu_listar.add_command(label="Livros Emprestados", command=self.abrir_livros_emprestados)
        self.menu_listar.add_command(label="Livros Devolvidos", command=self.abrir_livros_devolvidos)


        # Menu Empretimos
        self.menu_emprestimo = Menu(self.barra_menu, tearoff=0)
        self.menu_emprestimo.add_command(label="Realizar Empréstimo", command=self.abrir_novo_emprestimo)
        self.menu_emprestimo.add_command(label="Realizar Devolução", command=self.abrir_retornar_emprestimo)


        # Menu Remover
        self.menu_remover = Menu(self.barra_menu, tearoff=0)
        self.menu_remover.add_command(label="Remover Usuários", command=self.abrir_remover_user)
        self.menu_remover.add_command(label="Remover Livros", command=self.abrir_remover_livros)

        # Menu Ajuda
        self.menu_ajuda = Menu(self.barra_menu, tearoff=0)
        self.menu_ajuda.add_command(label="Sobre", command=self.abrir_ajuda)

        # Adicionando os menus à barra de menu principal
        self.barra_menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.barra_menu.add_cascade(label="Gerenciar", menu=self.menu_gerenciar)
        self.barra_menu.add_cascade(label="Listar", menu=self.menu_listar)
        self.barra_menu.add_cascade(label="Emprestimos", menu=self.menu_emprestimo)
        self.barra_menu.add_cascade(label="Remover", menu=self.menu_remover)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)


        # Configurar a barra de menu na janela principal
        self.master.config(menu=self.barra_menu)

        # Cores
        self.master.configure(background=cor_primaria)

        style = Style()
        style.theme_use("clam")

        # Frames
        self.frame_superior = Frame(self.master, bg=cor_secundaria_segunda_camada)
        self.frame_superior.grid(row=0, column=0)

        self.frame_inferior = Frame(self.master)
        self.frame_inferior.grid(row=1, column=2, pady=75)

        self.frame_status = Frame(self.master, relief='sunken', borderwidth=3, padx=2, pady=1)
        self.frame_status.grid(row=2, column=2, sticky="ew", pady=20)

        # Path para o ícone
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/logo.png")

        # Ícone [PNG]   
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.frame_superior, image=self.logo_photo, bg=cor_secundaria_segunda_camada)
        self.logo_app.grid(row=0, column=0, padx=10, pady=10)

        # Define o ícone da aplicação  
        definir_icone(self.master)

        self.logo_text_name = Label(self.frame_superior, text="SISTEMA BIBLIOTECÁRIO FELIX")
        self.logo_text_name.grid(row=2, column=0, padx=10, pady=10)

        self.welcome_text = Label(self.master, text="SEJA MUITO BEM VINDO!", font="Cascadia 34 bold")
        self.welcome_text.grid(row=0, column=2, padx=10, pady=10)

        self.explanation_text = Label(self.frame_inferior, text='''"Conheça o sistema de gerenciamento eficiente para informações\n de livros e empréstimos, powered by PostgreSQL!"'''
                                      , font=("Times New Roman", 16))
        self.explanation_text.grid(row=0, column=0, padx=10)

        self.status_msg1 = Label(self.frame_status, text=f"LIVROS [{how_many_books(credentials)}]")
        self.status_msg1.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.status_msg2 = Label(self.frame_status, text=f"USUÁRIOS [{how_many_users(credentials)}]")
        self.status_msg2.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.status_msg3 = Label(self.frame_status, text=f"EMPRÉSTIMOS [{how_many_loans(credentials)}]")
        self.status_msg3.grid(row=0, column=2, sticky="ew", padx=10, pady=5)

        self.atualizar_status()

    def atualizar_status(self):
        # Atualiza os labels com os valores mais recentes
        self.status_msg1.config(text=f"LIVROS [{how_many_books(credentials)}]")
        self.status_msg2.config(text=f"USUÁRIOS [{how_many_users(credentials)}]")
        self.status_msg3.config(text=f"EMPRÉSTIMOS [{how_many_loans(credentials)}]")

        # Agendar a próxima atualização em 10000 ms (10 segundos)
        self.master.after(3000, self.atualizar_status)


    def sair(self):
        self.master.quit()

    # Função para abrir interface de cadastro de usuário
    def abrir_novo_usuario(self):
        NewUserWindow(self.master)

    # Função para abrir interface de cadastro de livro
    def abrir_novo_livro(self):
        NewBookWindow(self.master)

    # Função para abrir interface de listar usuários
    def abrir_listar_usuarios(self):
        listUsersWindow(self.master)

    # Função para abrir interface de listar livros
    def abrir_listar_livros(self):
        listBooksWindow(self.master)

    # Função para abrir interface de listar livros emprestados
    def abrir_livros_emprestados(self):
        listbooksInLoan(self.master)

    #Função para mostrar livros devolvidos
    def abrir_livros_devolvidos(self):
        listCompletedReturns(self.master)

    # Função para abrir interface de realizar emprestimo
    def abrir_novo_emprestimo(self):
        insertLoan(self.master)

    # Função para abrir interface de retornar emprestimo
    def abrir_retornar_emprestimo(self):
        returnLoan(self.master)
    
    # Função para abrir interface de deletar usuários
    def abrir_remover_user(self):
        deleteUser(self.master)

    # Função para abrir interface de deletar livros
    def abrir_remover_livros(self):
        deleteBook(self.master)
    
    def abrir_ajuda(self):
        sobreSistema(self.master)




class NewUserWindow:

    def sair_new_win(self):
        self.new_user_window.destroy()

    def add_user(self):

        self.nome_get = self.texto_nome.get()
        self.sobrenome_get = self.texto_sobrenome.get()
        self.bairro_get = self.texto_bairro.get()
        self.rua_get = self.texto_rua.get()
        self.numero_get = self.texto_numero.get()
        self.email_get = self.texto_email.get()
        self.telefone_get = self.texto_telefone.get()

        self.lista_de_dados = [self.nome_get, self.sobrenome_get, self.bairro_get, self.rua_get, self.numero_get, self.email_get, self.telefone_get]
        
        # Verifica se existe campos vazios
        for i in self.lista_de_dados:
            if i == '':
                messagebox.showerror("Erro", "Um ou mais campos encontra-se vazios")
                return
        
        # Insere dados nos bancos de dados
        insert_user(credentials, self.nome_get, self.sobrenome_get, self.bairro_get,\
                     self.rua_get , self.numero_get, self.email_get, self.telefone_get)
        
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso")

        # Limpa dos dados inseridos na interface
        self.texto_nome.delete(0, END)
        self.texto_sobrenome.delete(0, END)
        self.texto_bairro.delete(0, END)
        self.texto_rua.delete(0, END)
        self.texto_numero.delete(0, END)
        self.texto_email.delete(0, END)
        self.texto_telefone.delete(0, END)

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_user_window = Toplevel()
        self.new_user_window.configure(background=cor_primaria_segunda_janela)
        self.new_user_window.title("")

        # Trava na nova janela
        self.new_user_window.transient(self.main_window)
        self.new_user_window.grab_set()

        self.new_user_window.geometry("900x400")
        self.new_user_window.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_user_window)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_user_window, text="INSIRA UM NOVO USUÁRIO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/user.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_user_window, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_user_window)

        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_user_window)
        self.frame_esquerdo.grid(row=1, column=0)

        ##Frame Direito
        self.frame_direito = Frame(self.new_user_window)
        self.frame_direito.grid(row=1, column=3)

        #nome
        self.label_nome = Label(self.frame_direito, text="Primeiro Nome")
        self.label_nome.grid(row=0, column=1, padx=5,pady=5)
        self.texto_nome = Entry(self.frame_direito, width=50)
        self.texto_nome.grid(row=0, column=2, padx=5,pady=5)

        #Sobrenome
        self.label_sobrenome = Label(self.frame_direito, text="Sobrenome")
        self.label_sobrenome.grid(row=1, column=1,padx=5,pady=5)
        self.texto_sobrenome = Entry(self.frame_direito, width=50)
        self.texto_sobrenome.grid(row=1, column=2,padx=5,pady=5)

        #bairro
        self.label_bairro = Label(self.frame_direito, text="Bairro")
        self.label_bairro.grid(row=2, column=1,padx=5,pady=5)
        self.texto_bairro = Entry(self.frame_direito, width=50)
        self.texto_bairro.grid(row=2, column=2,padx=5,pady=5)

        #Rua
        self.label_rua = Label(self.frame_direito, text="Rua")
        self.label_rua.grid(row=3, column=1,padx=5,pady=5)
        self.texto_rua = Entry(self.frame_direito, width=50)
        self.texto_rua.grid(row=3, column=2,padx=5,pady=5)

        #Número
        self.label_numero = Label(self.frame_direito, text="Número")
        self.label_numero.grid(row=4, column=1,padx=5,pady=5)
        self.texto_numero = Entry(self.frame_direito, width=50)
        self.texto_numero.grid(row=4, column=2,padx=5,pady=5)

        #Email
        self.label_email = Label(self.frame_direito, text="Email")
        self.label_email.grid(row=5, column=1,padx=5,pady=5)
        self.texto_email = Entry(self.frame_direito, width=50)
        self.texto_email.grid(row=5, column=2,padx=5,pady=5)

        #Telefone
        self.label_telefone = Label(self.frame_direito, text="Telefone")
        self.label_telefone.grid(row=6, column=1,padx=5,pady=5)
        self.texto_telefone = Entry(self.frame_direito, width=50)
        self.texto_telefone.grid(row=6, column=2,padx=5,pady=5)

        #Botões
        self.botao_salvar = Button(self.frame_direito, width=20, text="Salvar",background=cor_primaria_segunda_janela, command=self.add_user)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_new_win)

        self.botao_salvar.grid(row=7,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=7,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class NewBookWindow:

    def sair_new_book(self):
        self.new_book_window.destroy()

    def add_book(self):

        self.titulo_get = self.texto_titulo.get()
        self.autor_get = self.texto_autor.get()
        self.editora_get = self.texto_editora.get()
        self.ano_publicacao_get = self.texto_ano_publicacao.get()
        self.isbn_get = self.texto_isbn.get()

        self.lista_de_dados = [self.titulo_get, self.autor_get, self.editora_get, self.ano_publicacao_get, self.isbn_get]
        
        # Verifica se existe campos vazios
        for i in self.lista_de_dados:
            if i == '':
                messagebox.showerror("Erro", "Um ou mais campos encontra-se vazios")
                return
        
        # Insere dados nos bancos de dados
        insert_book(credentials, self.titulo_get, self.autor_get, self.editora_get,\
                     self.ano_publicacao_get, self.isbn_get)
        
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso")

        # Limpa dos dados inseridos na interface
        self.texto_titulo.delete(0, END)
        self.texto_autor.delete(0, END)
        self.texto_editora.delete(0, END)
        self.texto_ano_publicacao.delete(0, END)
        self.texto_isbn.delete(0, END)

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_book_window = Toplevel()
        self.new_book_window.configure(background=cor_primaria_segunda_janela)
        self.new_book_window.title("")

        # Trava na nova janela
        self.new_book_window.transient(self.main_window)
        self.new_book_window.grab_set()

        self.new_book_window.geometry("730x350")
        self.new_book_window.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_book_window)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_book_window, text="INSIRA UM LIVRO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/book.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_book_window, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_book_window)

        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_book_window)
        self.frame_esquerdo.grid(row=1, column=0)

        ##Frame Direito
        self.frame_direito = Frame(self.new_book_window)
        self.frame_direito.grid(row=1, column=3)

        #titulo
        self.label_titulo = Label(self.frame_direito, text="Título")
        self.label_titulo.grid(row=0, column=1)
        self.texto_titulo = Entry(self.frame_direito, width=50)
        self.texto_titulo.grid(row=0, column=2)

        #Autor
        self.label_autor = Label(self.frame_direito, text="Autor")
        self.label_autor.grid(row=1, column=1,padx=5,pady=5)
        self.texto_autor = Entry(self.frame_direito, width=50)
        self.texto_autor.grid(row=1, column=2,padx=5,pady=5)

        #Editora
        self.label_editora = Label(self.frame_direito, text="Editora")
        self.label_editora.grid(row=2, column=1,padx=5,pady=5)
        self.texto_editora = Entry(self.frame_direito, width=50)
        self.texto_editora.grid(row=2, column=2,padx=5,pady=5)

        #Ano de publicação
        self.label_ano_publicacao = Label(self.frame_direito, text="Ano de Publicação")
        self.label_ano_publicacao.grid(row=3, column=1,padx=5,pady=5)
        self.texto_ano_publicacao = Entry(self.frame_direito, width=50)
        self.texto_ano_publicacao.grid(row=3, column=2,padx=5,pady=5)

        #ISBN
        self.label_isbn = Label(self.frame_direito, text="ISBN")
        self.label_isbn.grid(row=4, column=1,padx=5,pady=5)
        self.texto_isbn = Entry(self.frame_direito, width=50)
        self.texto_isbn.grid(row=4, column=2,padx=5,pady=5)

        #Botões
        self.botao_salvar = Button(self.frame_direito, width=20, text="Salvar",background=cor_primaria_segunda_janela, command=self.add_book)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_new_book)

        self.botao_salvar.grid(row=5,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=5,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class listUsersWindow:

    def sair_new_book(self):
        self.new_list_user_window.destroy()

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_list_user_window = Toplevel()
        self.new_list_user_window.configure(background=cor_primaria_segunda_janela)
        self.new_list_user_window.title("")

        # Trava na nova janela
        self.new_list_user_window.transient(self.main_window)
        self.new_list_user_window.grab_set()

        self.new_list_user_window.geometry("1250x400")
        self.new_list_user_window.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_list_user_window)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_list_user_window, text="  TODOS OS USUÁRIOS", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/list_users.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_list_user_window, image=self.logo_photo, bg=cor_navajo_white, background=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_list_user_window)

        ##Frame Direito
        self.frame_direito = Frame(self.new_list_user_window)
        self.frame_direito.grid(row=1, column=3)

        self.list_header = ['ID','Nome','Sobrenome','Bairro','Rua','Número','Email','Telefone']
        
        global tree

        self.tree = Treeview(self.frame_direito, selectmode="extended",
                            columns=self.list_header, show="headings")

        self.vsb = Scrollbar(self.frame_direito, orient="vertical", command=self.tree.yview)


        self.hsb = Scrollbar(self.frame_direito, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(column=0, row=2, sticky='nsew')
        self.vsb.grid(column=1, row=2, sticky='ns')
        self.hsb.grid(column=0, row=3, sticky='ew')
        self.frame_direito.grid_rowconfigure(0, weight=12)

        self.hd=["nw","nw","nw","nw","nw","nw","nw","nw"]
        self.h=[25,80,140,160,160,80,180,170]
        self.n=0

        for col in self.list_header:
            self.tree.heading(col, text=col, anchor='nw')
            self.tree.column(col, width=self.h[self.n],anchor=self.hd[self.n])
            
            self.n+=1

        self.dados = get_user(credentials)

        for item in self.dados:
            self.tree.insert('', 'end', values=item)


        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)


class listBooksWindow:

    def sair_new_book(self):
        self.new_list_all_books.destroy()

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_list_all_books = Toplevel()
        self.new_list_all_books.configure(background=cor_primaria_segunda_janela)
        self.new_list_all_books.title("")

        # Trava na nova janela
        self.new_list_all_books.transient(self.main_window)
        self.new_list_all_books.grab_set()

        self.new_list_all_books.geometry("900x400")
        self.new_list_all_books.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_list_all_books)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_list_all_books, text="  TODOS OS LIVROS", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/list_books.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_list_all_books, image=self.logo_photo, bg=cor_navajo_white, background=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_list_all_books)

        ##Frame Direito
        self.frame_direito = Frame(self.new_list_all_books)
        self.frame_direito.grid(row=1, column=3)

        self.list_header = ['ID','Titulo','Autor','Editora','Ano Publicação','ISBN']
        
        global tree

        self.tree = Treeview(self.frame_direito, selectmode="extended",
                            columns=self.list_header, show="headings")

        self.vsb = Scrollbar(self.frame_direito, orient="vertical", command=self.tree.yview)


        self.hsb = Scrollbar(self.frame_direito, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(column=0, row=2, sticky='nsew')
        self.vsb.grid(column=1, row=2, sticky='ns')
        self.hsb.grid(column=0, row=3, sticky='ew')
        self.frame_direito.grid_rowconfigure(0, weight=12)

        self.hd=["nw","nw","nw","nw","nw","nw"]
        self.h=[25,140,140,160,100,130]
        self.n=0

        for col in self.list_header:
            self.tree.heading(col, text=col, anchor='nw')
            self.tree.column(col, width=self.h[self.n],anchor=self.hd[self.n])
            
            self.n+=1

        self.dados = get_books(credentials)


        for item in self.dados:
            self.tree.insert('', 'end', values=item)


        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class listbooksInLoan:

    def sair_new_de(self):
        self.new_window_books_in_loan.destroy()

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_books_in_loan = Toplevel()
        self.new_window_books_in_loan.configure(background=cor_primaria_segunda_janela)
        self.new_window_books_in_loan.title("")

        # Trava na nova janela
        self.new_window_books_in_loan.transient(self.main_window)
        self.new_window_books_in_loan.grab_set()

        self.new_window_books_in_loan.geometry("900x400")
        self.new_window_books_in_loan.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_books_in_loan)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_books_in_loan, text="LIVROS EMPRESTADOS", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/books_in_loan.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_books_in_loan, image=self.logo_photo, bg=cor_navajo_white, background=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_books_in_loan)

        ##Frame Direito
        self.frame_direito = Frame(self.new_window_books_in_loan)
        self.frame_direito.grid(row=1, column=3)


        self.list_header = ['Título','Nome do usuário','Id. Emprestimo','Dia do emprestimo']
        
        global tree

        self.tree = Treeview(self.frame_direito, selectmode="extended",
                            columns=self.list_header, show="headings")

        self.vsb = Scrollbar(self.frame_direito, orient="vertical", command=self.tree.yview)


        self.hsb = Scrollbar(self.frame_direito, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(column=0, row=2, sticky='nsew')
        self.vsb.grid(column=1, row=2, sticky='ns')
        self.hsb.grid(column=0, row=3, sticky='ew')
        self.frame_direito.grid_rowconfigure(0, weight=12)

        self.hd=["nw","nw","nw","nw","nw","nw"]
        self.h=[250,130,120,160,100]
        self.n=0

        for col in self.list_header:
            self.tree.heading(col, text=col, anchor='nw')
            self.tree.column(col, width=self.h[self.n],anchor=self.hd[self.n])
            
            self.n+=1

        self.dados = get_books_on_loan(credentials)


        for self.book in self.dados:
            self.dado = [f"{self.book[0]}", f"{self.book[1]}", f"{self.book[2]}", f"{self.book[3]}", f"{self.book[4]}"]

        for item in self.dados:
            self.tree.insert('', 'end', values=item)


        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class listCompletedReturns:

    def sair_new_book(self):
        self.new_window_completed_returns.destroy()

    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_completed_returns = Toplevel()
        self.new_window_completed_returns.configure(background=cor_primaria_segunda_janela)
        self.new_window_completed_returns.title("")

        # Trava na nova janela
        self.new_window_completed_returns.transient(self.main_window)
        self.new_window_completed_returns.grab_set()

        self.new_window_completed_returns.geometry("850x400")
        self.new_window_completed_returns.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_completed_returns)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_completed_returns, text="TODAS DEVOLUÇÕES", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/books_returned.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_completed_returns, image=self.logo_photo, bg=cor_navajo_white, background=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_completed_returns)

        ##Frame Direito
        self.frame_direito = Frame(self.new_window_completed_returns)
        self.frame_direito.grid(row=1, column=3)

        self.list_header = ['ID empréstimo','Livro','Usuário','Data do empréstismo','Data devolução']
        
        global tree

        self.tree = Treeview(self.frame_direito, selectmode="extended",
                            columns=self.list_header, show="headings")

        self.vsb = Scrollbar(self.frame_direito, orient="vertical", command=self.tree.yview)


        self.hsb = Scrollbar(self.frame_direito, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(column=0, row=2, sticky='nsew')
        self.vsb.grid(column=1, row=2, sticky='ns')
        self.hsb.grid(column=0, row=3, sticky='ew')
        self.frame_direito.grid_rowconfigure(0, weight=12)

        self.hd=["nw","nw","nw","nw","nw"]
        self.h=[25,140,140,160,100]
        self.n=0

        for col in self.list_header:
            self.tree.heading(col, text=col, anchor='nw')
            self.tree.column(col, width=self.h[self.n],anchor=self.hd[self.n])
            
            self.n+=1

        self.dados = get_loans_with_return_date(credentials)

        for item in self.dados:
            self.tree.insert('', 'end', values=item)


        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)


class insertLoan:

    def sair_new_win(self):
        self.new_window_insert_loan.destroy()

    def add_loan(self):

        self.id_livro_get = self.texto_id_livro.get()
        self.id_usuario_get = self.texto_id_usuario.get()

        self.lista_de_dados = [self.id_usuario_get, self.id_livro_get]
        
        # Verifica se existe campos vazios
        for i in self.lista_de_dados:
            if i == '':
                messagebox.showerror("Erro", "Um ou mais campos estão vazios.")
                return
            
        # Verifica se o usuário existe
        self.test_usuario_existe = verify_user_exist(credentials,self.id_usuario_get)  # Corrigir o parâmetro
        if not self.test_usuario_existe:
            messagebox.showerror("Erro", "O usuário não está cadastrado")
            return

        # Verifica se o livro existe
        self.test_livro_existe = verify_book_exist(credentials, self.id_livro_get)
        if not self.test_livro_existe:
            messagebox.showerror("Erro", "O Id. do livro não consta no sistema")
            return
            
        # Verifica se o livro já se encontra emprestado
        self.test_disponivel = verify_available_book(credentials, self.id_livro_get)
        if not self.test_disponivel:
            messagebox.showerror("Erro", "O livro está em posse de outro usuário")
            return


        # Pega data atual
        self.date_now = datetime.now().strftime('%Y-%m-%d')

        # Insere dados nos bancos de dados
        if self.test_disponivel == True:
            insert_loan(credentials, self.id_livro_get,  self.id_usuario_get, self.date_now, None)
        
        messagebox.showinfo("Sucesso", "Empréstimo realizado com êxito")

        # Limpa dos dados inseridos na interface
        self.texto_id_livro.delete(0, END)
        self.texto_id_usuario.delete(0, END)


    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_insert_loan = Toplevel()
        self.new_window_insert_loan.configure(background=cor_primaria_segunda_janela)
        self.new_window_insert_loan.title("")

        # Trava na nova janela
        self.new_window_insert_loan.transient(self.main_window)
        self.new_window_insert_loan.grab_set()

        self.new_window_insert_loan.geometry("800x250")
        self.new_window_insert_loan.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_insert_loan)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_insert_loan, text="REALIZAR EMPRÉSTIMO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/plus.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_insert_loan, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_insert_loan)

        
        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_window_insert_loan)
        self.frame_esquerdo.grid(row=1, column=0)


        ##Frame Direito
        self.frame_direito = Frame(self.new_window_insert_loan)
        self.frame_direito.grid(row=1, column=3)

        #Id_usuário
        self.label_id_usuario = Label(self.frame_direito, text="Id. Usuario")
        self.label_id_usuario.grid(row=0, column=1)
        self.texto_id_usuario = Entry(self.frame_direito, width=50)
        self.texto_id_usuario.grid(row=0, column=2)

        #Id_livro
        self.label_id_livro = Label(self.frame_direito, text="Id. Livro")
        self.label_id_livro.grid(row=1, column=1,padx=5,pady=5)
        self.texto_id_livro = Entry(self.frame_direito, width=50)
        self.texto_id_livro.grid(row=1, column=2,padx=5,pady=5)

        #Texto explicação
        self.label_id_explicação = Label(self.frame_direito, text="(A data do empréstimo será inserida automaticamente.)", fg="blue")
        self.label_id_explicação.grid(row=2, column=2,padx=5,pady=5)


        #Botões
        self.botao_salvar = Button(self.frame_direito, width=20, text="Salvar",background=cor_primaria_segunda_janela, command=self.add_loan)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_new_win)

        self.botao_salvar.grid(row=5,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=5,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class returnLoan:

    def sair_new_win(self):
        self.new_window_return_loan.destroy()

    def return_book_in_loan(self):

        self.data_id_emprestimo_get = self.texto_id_emprestimo.get()

        self.lista_de_dados = [self.data_id_emprestimo_get]

        # Verifica se existe emprestimo com esse id
        self.test_verifica_possivel = verify_loan_exist(credentials, self.data_id_emprestimo_get)
        if not self.test_verifica_possivel:
            messagebox.showerror("Erro", "Empréstimo não existe")
            return

        
        # Verifica se o empréstimo não está mais ativo
        self.test_verifica_emprestimo = verify_available_loan(credentials, self.data_id_emprestimo_get)
        if not self.test_verifica_emprestimo:
            messagebox.showerror("Erro", "A devolução já foi realizada")
            return

        # Verifica se existe campos vazios
        for i in self.lista_de_dados:
            if i == '':
                messagebox.showerror("Erro", "Um ou mais campos estão vazios.")
                return
        
        # Pega data atual
        self.date_now = datetime.now().strftime('%Y-%m-%d')

        # Insere dados nos bancos de dados
        return_loan(credentials, self.data_id_emprestimo_get, self.date_now)
        
        messagebox.showinfo("Sucesso", "Devolução realizada com êxito")

        # Limpa dos dados inseridos na interface
        self.texto_id_emprestimo.delete(0, END)


    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_return_loan = Toplevel()
        self.new_window_return_loan.configure(background=cor_primaria_segunda_janela)
        self.new_window_return_loan.title("")

        # Trava na nova janela
        self.new_window_return_loan.transient(self.main_window)
        self.new_window_return_loan.grab_set()

        self.new_window_return_loan.geometry("800x230")
        self.new_window_return_loan.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_return_loan)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_return_loan, text="REALIZAR DEVOLUÇÃO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/hands.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_return_loan, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_return_loan)
    
        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_window_return_loan)
        self.frame_esquerdo.grid(row=1, column=0)

        ##Frame Direito
        self.frame_direito = Frame(self.new_window_return_loan)
        self.frame_direito.grid(row=1, column=3)

        #Id_livro
        self.label_id_emprestimo = Label(self.frame_direito, text="Id. Emprestimo")
        self.label_id_emprestimo.grid(row=0, column=1)
        self.texto_id_emprestimo = Entry(self.frame_direito, width=50)
        self.texto_id_emprestimo.grid(row=0, column=2)

        #Texto explicação
        self.label_id_explicação = Label(self.frame_direito, text="(A data da devolução será inserida automaticamente.)", fg="blue")
        self.label_id_explicação.grid(row=1, column=2,padx=5,pady=5)

        # Botões
        self.botao_salvar = Button(self.frame_direito, width=20, text="Salvar",background=cor_primaria_segunda_janela, command=self.return_book_in_loan)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_new_win)

        self.botao_salvar.grid(row=5,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=5,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

        
class deleteUser:

    def sair_delete_user(self):
        self.new_window_delete_user.destroy()

    def remove_user(self):

        self.data_id_usuario_get = self.texto_id_usuario.get()

        self.lista_de_dados = [self.data_id_usuario_get]
        
        # Verifica se existe campos vazios
        if not self.data_id_usuario_get:
            messagebox.showerror("Erro", "O campo está vazio")
            return
        
        # Insere dados nos bancos de dados
        self.delete_test = delete_user(credentials, self.data_id_usuario_get)
        
        if self.delete_test: 
            messagebox.showinfo("Sucesso", "A remoção de usuário foi realizada com êxito")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado")


        # Limpa dos dados inseridos na interface
        self.texto_id_usuario.delete(0, END)


    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_delete_user = Toplevel()
        self.new_window_delete_user.configure(background=cor_primaria_segunda_janela)
        self.new_window_delete_user.title("")

        # Trava na nova janela
        self.new_window_delete_user.transient(self.main_window)
        self.new_window_delete_user.grab_set()

        self.new_window_delete_user.geometry("770x220")
        self.new_window_delete_user.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_delete_user)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_delete_user, text="DELETAR USUÁRIO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/delete_user.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_delete_user, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_delete_user)
    
        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_window_delete_user)
        self.frame_esquerdo.grid(row=1, column=0)

        ##Frame Direito
        self.frame_direito = Frame(self.new_window_delete_user)
        self.frame_direito.grid(row=1, column=3)

        #Id_Usuário
        self.label_id_usuario = Label(self.frame_direito, text="Id. Usuário")
        self.label_id_usuario.grid(row=0, column=1)
        self.texto_id_usuario = Entry(self.frame_direito, width=60)
        self.texto_id_usuario.grid(row=0, column=2)

        #Texto explicação
        self.label_id_explicação = Label(self.frame_direito, text="(CUIDADO: O usuário será completamente removido do sistema)",fg="red")
        self.label_id_explicação.grid(row=2, column=2,padx=5,pady=5)

        # Botões
        self.botao_confirmar = Button(self.frame_direito, width=20, text="Confirmar",background=cor_primaria_segunda_janela, command=self.remove_user)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_delete_user)

        self.botao_confirmar.grid(row=5,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=5,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class deleteBook:

    def sair_delete_book(self):
        self.new_window_delete_book.destroy()

    def remove_book(self):

        self.data_id_book_get = self.texto_id_book.get()

        self.lista_de_dados = [self.data_id_book_get]
        
        # Verifica se existe campos vazios
        if not self.data_id_book_get:
            messagebox.showerror("Erro", "O campo está vazio")
            return
        
        # Insere dados nos bancos de dados
        self.delete_test = delete_book(credentials, self.data_id_book_get)
        
        if self.delete_test: 
            messagebox.showinfo("Sucesso", "A remoção do livro foi realizada com êxito")
        else:
            messagebox.showerror("Erro", "Livro não encontrado")


        # Limpa dos dados inseridos na interface
        self.texto_id_book.delete(0, END)


    def __init__(self, main_window):
        self.main_window = main_window

        # Configurações da nova Janela
        self.new_window_delete_book = Toplevel()
        self.new_window_delete_book.configure(background=cor_primaria_segunda_janela)
        self.new_window_delete_book.title("")

        # Trava na nova janela
        self.new_window_delete_book.transient(self.main_window)
        self.new_window_delete_book.grab_set()

        self.new_window_delete_book.geometry("720x220")
        self.new_window_delete_book.resizable(width=False, height=False)

        ######Frame superior
        self.frame_superior = Frame(self.new_window_delete_book)
        self.frame_superior.grid(row=0, column=0)
        self.logo_text_name = Label(self.new_window_delete_book, text="DELETAR LIVRO", font="Cascadia 30 bold")

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/delete_book.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.new_window_delete_book, image=self.logo_photo, bg=cor_navajo_white)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_delete_book)

    
        ######Frame Esquerdo
        self.frame_esquerdo = Frame(self.new_window_delete_book)
        self.frame_esquerdo.grid(row=1, column=0)

        ##Frame Direito
        self.frame_direito = Frame(self.new_window_delete_book)
        self.frame_direito.grid(row=1, column=3)

        #Id_Usuário
        self.label_id_book = Label(self.frame_direito, text="Id. Livro")
        self.label_id_book.grid(row=0, column=1)
        self.texto_id_book = Entry(self.frame_direito, width=60)
        self.texto_id_book.grid(row=0, column=2)

        #Texto explicação
        self.label_id_explicação = Label(self.frame_direito, text="(CUIDADO: O livro será completamente removido do sistema)", fg="red")
        self.label_id_explicação.grid(row=2, column=2,padx=5,pady=5)

        # Botões
        self.botao_salvar = Button(self.frame_direito, width=20, text="Salvar",background=cor_primaria_segunda_janela, command=self.remove_book)
        self.botao_sair = Button(self.frame_direito, width=20, text="Sair", background=cor_primaria_segunda_janela, command=self.sair_delete_book)

        self.botao_salvar.grid(row=5,column=1,padx=5, pady=5)
        self.botao_sair.grid(row=5,column=2,padx=5, pady=5)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        # Grids Necessarios
        self.logo_app.grid(row=0, column=0, padx=0, pady=0)
        self.logo_text_name.grid(row=0, column=3, padx=100, pady=20)

class sobreSistema:

    def __init__(self, main_window):

        # Criação e configuração da janela da aplicação
        self.main_window = main_window

        self.new_window_about = Toplevel()
        self.new_window_about.configure(background=cor_secundaria_segunda_camada)
        self.new_window_about.title("")
        
        self.new_window_about.transient(self.main_window)
        self.new_window_about.grab_set()

        self.new_window_about.geometry("230x200")
        self.new_window_about.resizable(width=False, height=False)

        #Frame superior

        self.frame_superior = Frame(self.new_window_about)
        self.frame_superior.grid(pady=10)

        # Frame Central
        self.frame_centro = Frame(self.new_window_about)
        self.frame_centro.grid(padx=25, pady=30)

        self.credits1 = Label(self.frame_centro, text="Sistema bibliotecario Felix")
        self.credits1.grid()
        self.credits2 = Label(self.frame_centro, text="Feito por Yago Azevedo Cruz",fg="blue")
        self.credits2.grid()
        self.credits3 = Label(self.frame_centro, text="yagoazevedocruz@hotmail.com", fg="green")
        self.credits3.grid()

        # Ícones
        icon_path = os.path.join(os.path.dirname(__file__), "Icons/about.png")
        self.logo_img = Image.open(icon_path)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_app = Label(self.frame_superior, image=self.logo_photo, bg=cor_secundaria_segunda_camada)

        # Define o ícone da aplicação  
        definir_icone(self.new_window_about)

        # Manter uma referência à imagem
        self.logo_app.image = self.logo_photo

        self.logo_app.grid()



if __name__ == "__main__":

    logintk = Login() 
    root = Tk()
    app = TelaInicial(root)


    #Cria a base de dados caso não exista
    dados_create(credentials)
    root.mainloop()

