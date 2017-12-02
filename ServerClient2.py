
'''def chat(c, conversa):
while True:
    data = c.recv(1024)
    principal = conversa[0]
    for pessoa in conversa:   #percorre todas as pessoas da conversa
        if (pessoa is not principal):   #para garantir que nao envia a mensagem para ela propria
            for key, value in dic.iteritems():  #percorre o dic para encontrar o 'c' de cada uma das pessoas para as quais quer enviar
                if (value == pessoa):
                    key.send(dic[c] + ':' + data)      #quando encontra a pessoa envia a mensagem'''
import socket
import threading
import sys
import random

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    global dicOnline, dicConversas, dicHold
    dicOnline = {}
    dicConversas = {}
    dicHold = {}
    global fileUsers
    global arrayFiles, users
    arrayFiles = []
    users = []
    global user, user2

    def __init__(self):
        self.sock.bind(('0.0.0.0', 9988))
        self.sock.listen(1)

    def readUsersFile(self):
        fileUsers = open("users.txt", "r")
	for line in fileUsers:
		print("Numa linha")
		comp = len(line)
		line2 = line[0:comp-1]
		if line2 not in users:
			users.append(line2)
	fileUsers.close()	

    def writeUsersFile(self):
        fileUsers = open("users.txt", "w")
        for user in users:
            fileUsers.write(user)
            fileUsers.write('\n')
        fileUsers.close()

    def handler(self, c, a):
        print("Na funcao handler")
        #quando a funcao handler e chamada e logo adicionado o utilizador a lista de users
        data = c.recv(1024)
        self.readUsersFile() #ve os users que existem
        conversa = data.split(':')
	dicConversas[conversa[0]] = [conversa[1], conversa[2]]
	print("DicConversa:")
	print(dicConversas)

        #verifica se o nome de utilizador do primeiro ainda nao existe
	if conversa[1] not in users:
        	self.users.append(conversa[1]) #adiciona aos users (so precisa de adicionar quem adicionou a conversa, porque a segunda foi escolhido das pessoas ja existentes no ficheiro)
        self.writeUsersFile() #escreve no ficheiro
        dicOnline[c] = conversa[1] #adiciona ao dicionario, juntamente com o 'c'. Porque e mais uma pessoa que ficou online

       # chatThread = threading.Thread(target=self.chat, args=(c, conversa))

	print("Dicionario: ")
        print(dicOnline);

        while True:
	    count = 0
            data = c.recv(1024)
            principal = conversa[1]
	    for pessoa in dicConversa[conversa[0]]:	#vai buscar todas as pessoas associado a conversa de numero x
            	if pessoa is not principal:		#para nao enviar mensagem para ela propria
			for key, value in dicOnline.iteritems():  	#percorre o dic para encontrar o 'c' de cada uma das pessoas para as quais quer enviar
                        	if (value == pessoa):
					count = 1
                            		key.send(dicOnline[c] + ':' + data)      #quando encontra a pessoa envia a mensagem
			if (count == 0): 		#caso a pessoa nao esteja online
				if pessoa in dicHold:
					dic[pessoa].append(data)	#caso ja tenha sido mandada alguma mensagem enquanto a pessoa esteve off faz-se append ao array da nossa msg
				else:
					dic[pessoa] = [data]	#caso seja a primeira vez que se esteja a tentar mandar msg enquanto off, iniciamos um array de msgs associado a pessoa
					hold = open('hold.txt', 'w')	#insere o nome da pessoa no ficheiro de pessoas que tem msgs on hold
					hold.write(pessoa)
					hold.write('\n')

	    if not data:
		print(str(a[0]) + ':' + str(a[1]) + " disconnected")
		del dicOnline[c]
		self.connections.remove(c);
		c.close();
		break

    def run(self):
        #adiciona todas as conecoes realizadas entre clients e o servidor
        while True:
            c, a = self.sock.accept()
            #sempre que um novo cliente e adicionado e criada uma nova thread handler
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + " connected")

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	global name
	name = ""
	global num
	global users, holds
	users = []
	holds = []
	global user

	def __init__(self, address):
		self.sock.connect((address, 9988))
		#thread responsavel pelo envio de mensagens
		sendThread = threading.Thread(target=self.recvMsg)
		sendThread.daemon = True
		sendThread.start()
	
		self.menu()

	def readUsersFile(self):
		#Le o ficheiro de users e guarda cada um deles no array "users"
		fileUsers = open("users.txt", "r")
		for line in fileUsers:
			print("Numa linha")
			comp = len(line)
			line2 = line[0:comp-1]
			users.append(line2)
		fileUsers.close()
	
	def readHoldFile(self):
		fileHold = open("hold.txt", "r")
		for line in fileHold:
			print("Numa linha")
			comp = len(line)
			line2 = line[0:comp-1]
			holds.append(line2)
		fileHold.close()

	def recvMsg(self):
		while True:
			data = self.sock.recv(1024)
			print(data)
			if not data:
				break

	def menu(self):
		name = raw_input("Introduza o seu nome de utilizador: ")
		self.readHoldsFile()
		if name in holds:	
			print('Tem mensages por ler:')
			#vai printar todas as mensagens associadas ao utilizador que nao esta online. so que esse dicHold esta no server. como fazemos?
		print("O que deseja fazer?\n(1) Iniciar uma nova conversa\n(2) Listar as minhas conversas\n(3) Sair")
		opcao = raw_input('Opcao: ')
		if (opcao == '1'):
			print("Pessoas existentes para conversar: ")
			self.readUsersFile()
			for user in users:
				if user != name:
					print(user)

			name2 = raw_input("Escolha com quem quer falar: ")
			num = random.randint(0, 100) #escolhe um numero para identificar a conversa
			string = str(num) + ':' + name + ':' + name2
			self.sock.send(string)
			
			#funcao que corre infinitamente
			#fica a espera que o client escreva algo, e depois envia-o para o server
			while True:
				string = raw_input('')
				self.sock.send(str(num) + ": " + name + ': '+ string)

if (len(sys.argv) == 1):
    global server
    server = Server()
    server.run()

else:
    client = Client(sys.argv[1])
