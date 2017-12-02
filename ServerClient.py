#coding = <utf-8>

import socket
import threading
import sys

global server

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    global users
    users = []
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

    def __init__(self):
        self.sock.bind(('0.0.0.0', 9999))
        # self.sock.bind(('0.0.0.0', 9998))
        self.sock.listen(1)

    def readUsersFile(self):
        fileUsers = open("users.txt", "r")
        self.users = fileUsers.readlines()
        fileUsers.close()

    def writeUsersFile(self):
        fileUsers = open("users.txt", "w")
        for user in users:
            fileUsers.write(user)
            fileUsers.write('\n')
        # fileUsers.writelines(users)
        fileUsers.close()

    def receiveSendMsg(self, c, name, conversa, cid):
        print(name + " listenig")
        while True:
            data = c.recv(1024)
            for user in conversa:
                if user != name:
                    for c, value in dic.iteritems():
                        if (value == user):
                            c.send(str(cid) + "-" + name + ": " + data)

    def conversa(self, conversa, cid):
        print("Creating conversation " + str(cid))
        for user in conversa:
            for c, value in dic.iteritems():
                if (value == user):
                    

    def handler(self, c, a):
        data = c.recv(1024)
        self.readUsersFile() # ve os users que existem
        if (data not in users):
            users.append(data) # adiciona aos users
            self.writeUsersFile() # escreve no ficheiro
        

        else:
            print("O nome de utilizador que quer inserir ja existe!")

        dicOnline[c] = data #adiciona ao dicionario
	principal = dicOnline[c]

        print("Users: ")
        print(users)
        print("Dicionario: ")
        print(dic);
        print("ArrayConversas: ")
        print(arrayConversas);

        while True:
            data = c.recv(1024)
            print(data)

	    if data in dicHold:
		c.send("Tem estas mensagens por ler:")
		for msg in dicHold[data]:
			c.send(msg)
		del dicHold[data]
		c.send("END")

	    else:
		c.send("END")

            if (data == "USERS"):
                print("Sending users to "+ principal)
                for user in users:
                    if(user != principal):
                        c.send(user)
                c.send("END")

            elif ("INIT" in data):
                msg = data.split(":")
                user = msg[1]
                print("Init conversation between "+ principal+" and "+user)
                self.conversaID += 1
		self.sock.send(str(self.conversaID))
		dicConversas[conversaID] = [principal, user]
				
		nomeFich = str(conversaID) +'_'+ principal + user + '.txt'
		arrayFiles.append(nomeFich)
		fich = open(nomeFich, 'a')

		#while para rececao de mensagens e envio pelo servidor
		while True:
			count = 0
			msg = c.recv(1024)
			fich.write(msg + '\n')
			for pessoa in dicConversas[conversaID]:
				if pessoa is not principal:
					for key, value in dicOnline.iterItems():
						if value == pessoa:
							count = 1
							key.send(msg)
					if count == 0:
						if pessoa in dicHold:
							dicHold[pessoa].append(msg)
						else:
							dicHold[pessoa] = [msg]
            if not data:
                print(str(a[0]) + ':' + str(a[1]) + " disconnected")
                self.connections.remove(c);
                c.close();
                break

    def run(self):
        #adiciona todas as conecoes realizadas entre clients e o servidor
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

    def recvMsg(self):
        while True:
            data = self.sock.recv(1024)
            print(data)
            if not data:
                break

    def menu(self):
        while True:
	    data = self.sock.recv(1024)
	    while (data != "END"):
		print(data)
		data = self.sock.recv(1024)
        
            print("O que deseja fazer?\n(1) Iniciar uma nova conversa\n(2) Listar as minhas conversas\n(3) Sair")
            opcao = raw_input('Opcao: ')
            if (opcao == '1'):
                self.sock.send("USERS")

                data = self.sock.recv(1024)
                if (data == "END"):
                    print("Nao ha utilizadores")
                    continue
                else:
                    print("Pessoas existentes: ")
                    while(data != "END"):
                        print(data)
                        data = self.sock.recv(1024)

                user2 = raw_input("Escolha: ")
                self.sock.send("INIT:"+user2)

                conversaID = self.sock.recv(1024)
		recvThread = threading.Thread(target=self.recvMsg)
		recvThread.daemon = True
		recvThread.start()
	
		while True:
			msg = raw_input('')
			self.sock.send(str(conversaID) + '- ' + self.name + ': '+ msg)
               
            elif (opcao == '2'):
                print("ola")

            elif (opcao == '3'):
                print("A sair...")
                sys.exit()

    def __init__(self, address, user):
        self.sock.connect((address, 9999))
        # self.sock.connect((address, 9998))
	
        self.name = user
        self.sock.send(self.name)

        self.menu()


if (len(sys.argv) == 1):
    global server
    server = Server()
    server.run()
else:
    user = raw_input("Introduza o seu nome de utilizador: ")
    client = Client(sys.argv[1], user)
