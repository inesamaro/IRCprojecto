#coding = <utf-8>

import socket
import threading
import sys

global server

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    global users
    #users = []
    global dicOnline, dicConversas, dicHold
    dicOnline = {}
    dicConversas = {}
    dicHold = {}
    global portos
    portos = []
    global ficheiros
    ficheiros = []
    global fileUsers
    global arrayFiles
    arrayFiles = []
    global arrayConversas
    arrayConversas = []
    conversaID = 0
    conversaIDstr = ""
    global nomeFich

    def __init__(self):
        # self.sock.bind(('0.0.0.0', 9999))
        self.sock.bind(('0.0.0.0', 9969))
        self.sock.listen(1)
        self.run()

    def readUsersFile(self):
	self.users = []
        fileUsers = open("users.txt", "r")
        for line in fileUsers:
		print("line")
		print(line)
		comp = len(line)
		line2 = line[0:comp-1]
		self.users.append(line2)
	fileUsers.close()

    def writeUsersFile(self):
        fileUsers = open("users.txt", "w")
        for user in users:
            fileUsers.write(user)
            fileUsers.write('\n')
        fileUsers.close()


    def handler(self, c, a):
        data = c.recv(1024)
        self.readUsersFile() # ve os users que existem

	print("Users depois da funcao de ler")
	print(self.users)

        if data not in self.users:
            self.users.append(data) # adiciona aos users
            self.writeUsersFile() # escreve no ficheiro
        else:
            print("O nome de utilizador que quer inserir ja existe!")

        c.send("HOLD") # avisar o cliente que vai receber as mensagens por ler
        c.send(":")
	if data in dicHold:
            for msg in dicHold[data]:
                c.send(msg)
		c.send(":")
            del dicHold[data]
            c.send("END")

        else:
            c.send("END")

        dicOnline[c] = data #adiciona ao dicionario
        principal = dicOnline[c]

       
        print("DicOnline: ")
        print(dicOnline);
        print("ArrayConversas: ")
        print(arrayConversas);

        data = c.recv(1024)
	print("Recebi do utilizador: ")
        print(data)

	if (data == "USERS"):
		print("Sending users to " + principal)
		c.send("USERS") # avisar o cliente que vai receber os users
		c.send(":")
		#self.readUsersFile()
		for user in self.users:
		    if(user != principal):
		        c.send(user)
			c.send(":")
		c.send("END")

	data = c.recv(1024)
       	if ("INIT" in data):
		verificar = 0
                msg = data.split(":")
                user = msg[1]
		for fich in arrayFiles:
			if (user in fich) and (principal in fich):
				verificar = 1
				cid = fich.split("_")
				self.conversaIDstr = cid[0] #atribuimos a conversa o id da convrsa que ja exitia antes entre estas duas pessoas
				c.send("CID:" + self.conversaIDstr)
		if verificar == 0:
		        print("Init conversation between " + principal + " and " + user)
		        self.conversaID += 1
			self.conversaIDstr = str(self.conversaID)
		        c.send("CID:" + self.conversaIDstr)
		        dicConversas[self.conversaIDstr] = [principal, user]
		        self.nomeFich = self.conversaIDstr +'_'+ principal + user + '.txt'
		        arrayFiles.append(self.nomeFich)
		        fich = open(self.nomeFich, 'a')

	print("dicOnline")
	print(dicOnline)

	print("dicConversas")
	print(dicConversas)

        #while para rececao de mensagens e envio pelo servidor
        while True:
	    print("dicHold")
	    print(dicHold)
            count = 0
	    fich = open(self.nomeFich, 'a')
            msg = c.recv(1024)
	    separado = msg.split('-')
 	    #nomes = separado[1].split(':')
	    #principal = nomes[0] 
            fich.write(msg + '\n')
	    print("dicConversas")
	    print(dicConversas)

	    print("principal")
	    print(principal)
            for pessoa in dicConversas[separado[0]]:
                if pessoa != principal:
                    for key, value in dicOnline.iteritems(): #percorre o dicOnline para ver se a pessoa para quem quer mandar a mensagem esta online
                        if value == pessoa:
                            count = 1
                            key.send(msg)
                    if count == 0:
			print(pessoa + "nao esta on")
                        if pessoa in dicHold:
                            dicHold[pessoa].append(msg)
                        else:
                            dicHold[pessoa] = [msg]
            if not msg:
                print(str(a[0]) + ':' + str(a[1]) + " disconnected")
                self.connections.remove(c);
                c.close();
                break


    def run(self):
        #adiciona todas as conecoes realizadas entre clients e o servidor
        self.readUsersFile()
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            portos.append(a[1])
            print(str(a[0]) + ':' + str(a[1]) + " connected")

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global name
    name = ""
    global users
    users = []
    global conversaID

    def recvMsg(self):
        # os prints podem aparecer sobrepostos com os prints do menu
        # deve haver uma maneira de resolver isso 
        while True:
            data = self.sock.recv(1024)
	    #print("Data pura: \n ---->")
	    #print(data)

            #if "USERS" in data:
		#print("Recebi um USERS")
                #data = self.sock.recv(1024)
                #print("Pessoas existentes: ")
                #while(data != "END"):
                #    print(data + '\n')
                #    data = self.sock.recv(1024)
		#user2 = raw_input("Escolha: ")
                #self.sock.send("INIT:" + user2)

            if "USERS" in data:
		users = data.split(":")
		print("Pessoas existentes para conversar: ")		
		for user in users:
			if (user != "END"):
				print(user)
		print("Escolha com quem quer falar escrevendo: INIT:<nomeDaPessoa>")

            #elif "HOLD" in data:
		#print("Recebi um HOLD")
                #data = self.sock.recv(1024)
                #print("Mensagens por ler: ")
                #while (data != "END"):
                #    print(data)
                #    data = self.sock.recv(1024)
	
	    elif "HOLD" in data:
		print("Recebi um HOLD")
		holds = data.split(":")
		for hold in holds:
			if (hold != "END"):
				print(hold)

            elif "CID" in data:
		print("Recebi um CID")
                array = data.split(":")
                self.conversaID = int(array[1])
	    
	    else:
		print(data)

            if not data:
                break

    def menu(self):
        while True:
            # recebe as mensagens por ler na thread recv

            print("O que deseja fazer?\n(1) Iniciar uma nova conversa\n(2) Listar as minhas conversas\n(3) Sair")
            opcao = raw_input('Opcao: ')
            if (opcao == '1'):
                self.sock.send("USERS")

                # pensei numa ideia para a thread nao bloquear
                # sempre que o servidor envia alguma coisa ao cliente envia uma palavra chave 
                # primeiro e assim a thread ja sabe o que esta a receber

                # recebe os users na thread recv
		
		recvThread = threading.Thread(target=self.recvMsg)
        	recvThread.daemon = True
        	recvThread.start()

                while True:
                    msg = raw_input('')
		    if "INIT" in msg:
			self.sock.send(msg)
		    else:
                    	self.sock.send(str(self.conversaID) + '-' + self.name +': '+ msg)

            elif (opcao == '2'):	
                print("ola")

            elif (opcao == '3'):
                print("A sair...")
                sys.exit()

    def __init__(self, address):
        # self.sock.connect((address, 9999))
        self.sock.connect((address, 9969))
        self.name = raw_input("Introduza o seu nome de utilizador: ")
        self.sock.send(self.name)

        self.menu()


if (len(sys.argv) == 1):
    global server
    server = Server()
else:
    client = Client(sys.argv[1])
