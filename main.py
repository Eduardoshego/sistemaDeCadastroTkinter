from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

root = Tk()

class Functions():
    #FUNÇÃO DO BOTÃO LIMPAR (LIMPA O TEXTO EM TODAS AS ENTRYS)
    def clean_entrys(self):
        self.entry_codigo.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_cidade.delete(0, END)
    
    #FUNÇÃO DO BANCO DE DADOS
    def conecta_bd(self):
        self.connection = sqlite3.connect('database.db')# -> CRIA O BANCO DE DADOS database.db e abre a conexão
        self.cursor = self.connection.cursor() #variavel que simplifica o uso de comandos do SQLITE3
    def close_connection(self):
        self.connection.close()
    def cria_tables(self):
        try:
            self.conecta_bd() 
            #comandos do sqlite3 para criaçaõ da tabela.
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes         
                                 (codigo INTEGER PRIMARY KEY,
                                    nome CHAR(40) NOT NULL,
                                    telefone CHAR(10),
                                    cidade CHAR(10) )'''
                                )
            self.connection.commit() #-> Confirma as mudanças no banco de daddos.
            self.close_connection()
        except sqlite3.Error as erro:
            print(erro) #-> retorna o resultado do erro se houver.

    def save_data(self):
        self.codigo = self.entry_codigo.get() # ->Pega o valor da entry_codigo.
        self.nome = self.entry_nome.get()
        self.telefone = self.entry_telefone.get()
        self.cidade = self.entry_cidade.get()
        try:
            self.conecta_bd()
            self.cursor.execute('INSERT INTO clientes (nome, telefone, cidade) VALUES (?,?,?)',
                                (self.nome, self.telefone, self.cidade))
            self.connection.commit()
            self.close_connection()
            self.select_all_for_TreeView()
            messagebox.showinfo('Sucesso', 'Dados salvos com sucesso!')
            self.clean_entrys()
        except sqlite3.Error as erro:
            print(erro)
            messagebox.showerror('Erro', 'Erro ao salvar os dados!')

    def select_all_for_TreeView(self):
        try:
            self.conecta_bd()
            self.cursor.execute('SELECT * FROM clientes ORDER BY nome ASC')
            self.result = self.cursor.fetchall()
            self.close_connection()
            self.lista_clientes.delete(*self.lista_clientes.get_children())
            for row in self.result:
                self.lista_clientes.insert('', END, values=row)
        except sqlite3.Error as erro:
            print(erro)
class Application(Functions):

    def __init__(self):
        self.root = root #->variável que recebe todos os paramentros do tkinter
        self.tela() #-> Chama a tela principal.
        self.frames_da_tela() #-> Chama os frames da tela
        self.widgets_frame_1()# -> Chama os widgets do frame 1
        self.list_frame2() # -> Chama os widgets do frame 2
        self.cria_tables() # -> Inicia a criação do banco de dados.
        self.select_all_for_TreeView() # -> Chama a função para selecionar todos os registros.
        root.mainloop()# mantem a tela em looping loop necessário pois sem ele a tela fecha.

    def tela(self):
        #Configuration of screen

        self.root.title('Cadastro de equipamentos')
        self.root.configure(background='#9800FA')
        self.root.geometry("980x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=800)
        self.root.minsize(width=400, height=200)

    def frames_da_tela(self):
        
        #Inicia o frame 1 com seus parâmetros
        self.frame1 = Frame(self.root, # Define onde será inserido o frame nesse caso na tela principal (root) <- seu PAI.
                            bd=4, # Define o tipo de bordas do frame.
                            bg='#7A4DFA', # Define sua cor de fundo.
                            highlightbackground='#759feb',  #define a cor da linha das bordas
                            highlightthickness=2) # define o tamanho da linha das bordas
        
        #Posiciona o frame dentro da janela.
        self.frame1.place(relx=0.05, # -> posiçao em relaçao ao eixo x em porcentagem (0.05) representa 5%
                          rely=0.02, # -> posição em relação ao eixo y em porcentagem (0.02) representa 2%
                          relwidth=0.9,   # -> define seu tamanho em largura em proporção ao seu elelmento Pai
                          relheight=0.46) # -> define seu tamanho em altura em proporção ao seu elelmento Pai.
        
        self.frame2 = Frame(self.root,
                            bd=4,
                            bg='#7A4DFA',
                            highlightbackground='#759feb',
                            highlightthickness=2)
        
        self.frame2.place(relx=0.05,
                          rely=0.5,
                          relwidth=0.9,
                          relheight=0.46)
        
    def widgets_frame_1(self):

        #definição dos buttons e estilização dos buttons

        self.botao_limpar = Button(self.frame1, # Define onde se inicia o button nesse caso dentro do frame1 seu Pai
                                   text='Limpar', # texto que será exibido no botão.
                                   bd=2, # Define o tipe de borda do botão
                                   bg= '#D330FA', # Define a cor de fundo do botão
                                   fg='black', # Define a cor do texto do botão
                                   font=('verdana', 8,  'bold'), # Define o estilo da fonte do texto exibido no botão
                                   command=self.clean_entrys) # Define qual funçao sera chamada ao clicar no botão.
        
        self.botao_buscar = Button(self.frame1,
                                    text='Buscar',
                                    bd=2,
                                    bg= '#D330FA',
                                    fg='black',
                                    font=('verdana', 8,  'bold'))

        self.botao_novo = Button(self.frame1,
                                 text='Salvar',
                                 bd=2,
                                 bg= '#D330FA',
                                 fg='black',
                                 font=('verdana', 8,  'bold'),
                                 command=self.save_data
                                 )
        
        
        self.botao_alterar = Button(self.frame1,
                                    text='Alterar',
                                    bd=2,
                                    bg= '#D330FA',
                                    fg='black',
                                    font=('verdana', 8,  'bold'))
        
        self.botao_deletar = Button(self.frame1,
                                    text='Deletar',
                                    bd=2,
                                    bg= '#D330FA',
                                    fg='black',
                                    font=('verdana', 8,  'bold'))
        
        # posições dos botões

        self.botao_limpar.place(relx=0.20, #Define a posiçao do eixo X do botão em relaçao ao seu elemento Pai em porcentagem.
                                rely=0.11, #Define a posição do eixo Y do botão em relação ao seu elemento Pai em porcentagem.
                                relwidth=0.1, #Define sua largura.
                                relheight=0.15) #Define sua altura.
        
        self.botao_buscar.place(relx=0.31,
                                rely=0.11,
                                relwidth=0.1,
                                relheight=0.15)
        
        self.botao_novo.place(relx=0.63,
                              rely=0.11,
                              relwidth=0.1,
                              relheight=0.15)
        
        self.botao_alterar.place(relx=0.74,
                                 rely=0.11,
                                 relwidth=0.1,
                                 relheight=0.15)
        
        self.botao_deletar.place(relx=0.85,
                                 rely=0.11,
                                 relwidth=0.1,
                                 relheight=0.15)
        
        #Create the label as inputs

        self.label_codigo = Label(self.frame1, # Define onde será inserido a label.
                                text='Código', # Define o texto que será exibido na label.
                                bg='#7A4DFA') #Define a cor de fundo da label.
        
        self.entry_codigo = Entry(self.frame1, # Define onde será inserido a entry.
                                  bg='#E6ED55') # Define a cor de fungo da entry.

        self.label_nome = Label(self.frame1,
                                text='Nome',
                                bg='#7A4DFA')
        self.entry_nome = Entry(self.frame1,
                                bg='#E6ED55')

        self.label_telefone = Label(self.frame1,
                                    text='Telefone',
                                    bg='#7A4DFA')
        self.entry_telefone = Entry(self.frame1,
                                    bg='#E6ED55')

        self.label_cidade = Label(self.frame1,
                                  text='Cidade',
                                  bg='#7A4DFA')
        self.entry_cidade = Entry(self.frame1,
                                  bg='#E6ED55')

        #configure the position of the entry and the label.

        self.label_codigo.place(relx=0.05,# Define a posiçao da label no eixo X em relação ao seu elemento Pai.
                                rely= 0.05 # Define a posição da label no eixo Y em relação ao seu elemento Pai.
                                )
        
        self.entry_codigo.place(relx=0.05, # Define a posião da entry no eixo X em relação ao seu elemento Pai.
                                rely=0.12, # Define a posião da entry no eixo Y em relação ao su elemento Pai.
                                relwidth= 0.09 # Define o tamanho da entry em largura.
                                )  

        
        self.label_nome.place(relx=0.05,rely= 0.36)        
        self.entry_nome.place(relx=0.05, rely=0.43, relwidth= 0.9 )

        
        self.label_telefone.place(relx=0.05,rely= 0.66)        
        self.entry_telefone.place(relx=0.05, rely=0.73, relwidth= 0.44)

        
        self.label_cidade.place(relx=0.51 ,rely= 0.66)        
        self.entry_cidade.place(relx=0.51, rely=0.73, relwidth= 0.44 )

    #Criação de uma arvore de visualização par criar lista.
    def list_frame2(self):
        self.lista_clientes = ttk.Treeview(self.frame2, #Define onde sera inserida a Treeview em seu elemento Pai.
                                           height= 3, #Define a altura da Treeview em seu elemento Pai.
                                        columns=('column1', 'column2', 'column3','column4')) # Define as colunas da Treeview.
        self.lista_clientes.heading('#0', text='') # Define o texto a ser exibido na primeia colunas.
        self.lista_clientes.heading('#1', text='Código') # Define o texto a ser exibido na segunda coluna.
        self.lista_clientes.heading('#2', text='Nome') # Define o texto a ser exibido na tercira coluna.
        self.lista_clientes.heading('#3', text='Telefone') # Define o texto a ser exibido na quarta coluna.
        self.lista_clientes.heading('#4', text='Cidade') # Define o texto a ser exibido na quinta coluna.
                                                                            
        self.lista_clientes.column('#0', width=0) 
        self.lista_clientes.column('#1', width=50)
        self.lista_clientes.column('#2', width=200) #define o tamanho das colunas em porcentagem( levar em consideração 100% = 500)
        self.lista_clientes.column('#3', width=125)
        self.lista_clientes.column('#4', width=125)                                                                    
        
        self.lista_clientes.place(relx=0.01, # Define a posição da Treeview em relação ao eixo X considerando as dimensões do seu elemento Pai.
                                  rely=0.01, # Define a posição da Treeview em relação ao eico Y considerando as dimensões do seu elemento Pai.
                                  relwidth=0.95, # Define o tamanho em largura da Treeview.
                                  relheight=0.99 # Define o tamanho em altura da Treeview.
                                  )
        #Definição da barra de rolagem para a Treeview.
        self.scroll_client = Scrollbar(self.frame2, # Define onde será inserida a barra de rolagem.
                                       orient='vertical' # Define a posição da barra de rolagem.
                                       )
        self.lista_clientes.configure(yscroll = self.scroll_client.set) # Relaciona a barra de rolagem com a Treeview.

        self.scroll_client.place(relx=0.96, # Define a posição da barra de rolagem em relação ao eixo X considerando as dimensões do seu elemento Pai.
                                 rely=0.01, # Define a posição da barra de rolagem em relação ao eixo Y considerando as dimensões do seu elemento Pai.
                                 relwidth= 0.04, # Define sua largura em porcentagem.
                                 relheight= 0.99 # Define sua altura em porcentagem.
                                 )

def test():
    print('Testing')


Application()