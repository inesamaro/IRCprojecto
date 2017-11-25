import socket
import threading
import sys

global server

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    global users
    users = []
    global dic
    dic = {}
    global portos
    portos = []
    global ficheiros
    ficheiros = []
    global fileUsers
    global arrayFiles
    arrayFiles = []
    global user, user2
    global arrayConversas
    arrayConversas = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 9999))
        self.sock.listen(1)

    def readUsersFile(self):
        fileUsers = open("users.txt", "r")
        users = fileUsers.readlines()
        fileUsers.close()

    def writeUsersFile(self):
        fileUsers = open("users.txt", "w")
        fileUsers.writelines(users)
        fileUsers.close()

    def handler(self, c, a):
        count = 0
        while True:
            data = c.recv(1024)
            if (count == 0):
                self.readUsersFile() # ve os users que existem
                if (data not in users):
                    users.append(data) # adiciona aos users
                    self.writeUsersFile() # escreve no ficheiro
                    dic[c] = data #adiciona ao dicionario
                else:
                    print("O nome de utilizador que quer inserir ja existe!")

                print("Users: ")
                print(users)
                print("Dicionario: ")
                print(dic);
            else:
                for key, value in self.dic.iteritems():
                    if (value is not user): #para garantir que nao mandamos a mensagem para a propria pessoa
                        if value in arrayAtual:
                            key.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]) + " disconnected")
                self.connections.remove(c);
                c.close();
                break
            count = count+1

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
    name = ""

    def sendMsg(self):
        while True:
            string = raw_input('')
            self.sock.send(self.name + ': '+ string)

    def recvMsg(self):
        while True:
            data = self.sock.recv(1024)
            print(data)
            if not data:
                break            

    def menu(self):
        while True:        
            print("O que deseja fazer?\n(1) Iniciar uma nova conversa\n(2) Listar as minhas conversas\n(3) Sair")
            opcao = raw_input('Opcao: ')
            if (opcao == '1'):
                print("Enviar mensagem")
                self.sendMsg()
                # print("Pessoas existentes: ")
                # fich = open('users.txt', 'r')
                # for line in fich:
                #     print(line)
                # fich.close()
                # user2 = raw_input("Com quem e que deseja comecar a conversa? ")
                # client = Client(sys.argv[1], user, user2)
            elif (opcao == '2'):
                print("ola")
                #for fich in arrayFiles:
                #    if user in fich.name:
                #        f = open(fich.name, 'r')
                #   percorre o arrayFiles ate encontrar ficheiros com o nome da pessoa, e depois imprime as conversas
            elif (opcao == '3'):
                sys.exit()

    def __init__(self, address, user):
        self.sock.connect((address, 9999))

        name = user
        self.sock.send(name)
        sendThread = threading.Thread(target=self.sendMsg)
        sendThread.daemon = True
        sendThread.start()
        recvThread = threading.Thread(target=self.recvMsg)
        recvThread.daemon = True
        recvThread.start()

        self.menu()


if (len(sys.argv) == 1):
    global server
    server = Server()
    server.run()
else:
    user = raw_input("Introduza o seu nome de utilizador: ")
    client = Client(sys.argv[1], user)
