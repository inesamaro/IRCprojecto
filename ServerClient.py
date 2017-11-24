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
    fileUsers = open("users.txt", "w")
    global arrayFiles
    arrayFiles = []
    global user, user2
    global arrayConversas
    arrayConversas = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 9999))
        self.sock.listen(1)

    def handler(self, c, a):
        count = 0
        while True:
            data = c.recv(1024)
            if (count == 0):
                if (data not in users):
                    data = data.split(":")
                    user = data[0]
                    user2 = data[1]
                    arrayAtual = {user, user2}
                    arrayConversas.append([user, user2])
                    users.append(user, user2)  #adiciona o user a lista de users
                    fileUsers.write(user2)  #adiciona cada novo user a uma linha do users.txt
                    fileUsers.close()
                    dic[c] = user #porque esta coneccao que e feita corresponde ao user principal, o que correu o programa
                    fich = open(user+user2+'.txt', 'w')
                    arrayFiles.append(fich)
                    fich.close()
                else:
                    print("O nome de utilizador que quer inserir ja existe!")
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
    string = ""
    def sendMsg(self):
        while True:
            self.sock.send(self.user + ': '+ bytes(raw_input('')))

    def __init__(self, address, user, user2):
        self.sock.connect((address, 9999))

        string = user + ":" + user2
        self.sock.send(string)
        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            print(data)
            if not data:
                break

if (len(sys.argv) == 1):
    global server
    server = Server()
    server.run()
else:
    user = raw_input("Introduza o seu nome de utilizador: ")
    #for line in fich:
    #    if user == line:
    # ve se o utilizador ja existe no ficheiro de users
    print("O que deseja fazer?\n (1) Iniciar uma nova conversa\n (2) Listar as minhas conversas\n (3) Sair")
    opcao = raw_input('Opcao: ')
    if (opcao == '1'):
        print("Pessoas existentes: ")
        fich = open('users.txt', 'r')
        for line in fich:
            print(line)
        fich.close()
        user2 = raw_input("Com quem e que deseja comecar a conversa? ")
        client = Client(sys.argv[1], user, user2)

    if (opcao == '2'):
        print("ola")
        #for fich in arrayFiles:
        #    if user in fich.name:
        #        f = open(fich.name, 'r')
        #   percorre o arrayFiles ate encontrar ficheiros com o nome da pessoa, e depois imprime as conversas
    if (opcao == '3'):
        sys.exit()
