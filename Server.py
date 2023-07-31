import socket
import threading
import pickle
from Gruppenchat import network 


PORT = 5050
HEADER = 128
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = ('localhost', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []
networklist = []
network_s = []
count = 0

def Server_send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    
def handle_client(conn, addr):
    global count
    print(f'MESSAGE: {conn, addr}')
    print(f'NEW CONNECTION {addr} connected.\n')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length) 
            except ValueError:
                msg_length = len(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(msg)
            
            if msg == DISCONNECT_MESSAGE:
                    print(f'{conn} leaves chat')
                    Server_send('[SERVER]: YOU LEFT THIS SERVER!', conn)
                    if conn in clients:
                        conn_index  = clients.index(conn)
                        print(conn_index)
                        clients.remove(conn)
                        nicknames.remove(nicknames[conn_index])
                    connected = False
                    
            elif msg[:5] == '/tell':
                    parts = msg.split(':')
                    username1 = parts[1]
                    if username1 in nicknames:
                        message_prv = parts[2]
                        print(f'this is {username1}' )
                        index = nicknames.index(username1)
                        conn_index  = clients.index(conn)
                        clients[index].send(f'/PRVT:{nicknames[conn_index]}:{message_prv}'.encode(FORMAT))
                    else:
                        conn.send(f'The User is not on the Server \n'.encode(FORMAT))
                        
            elif msg[:4] == '/msg':
                    print('Private Email: ')
                    parts = msg.split('d8Q7#UMSShKY+u%@')
                    receiver = parts[2]
                    title = parts[1]
                    text = parts[3]
                    sender = parts[4]
                        
                    if type(receiver) == str:
                        index = nicknames.index(receiver)
                        # clients[index].send(f'/PRVTE:{title}:{receiver}:{text}:{sender}'.encode(FORMAT))
                        Server_send(f'/msgd8Q7#UMSShKY+u%@{title}d8Q7#UMSShKY+u%@{receiver}d8Q7#UMSShKY+u%@{text}d8Q7#UMSShKY+u%@{sender}', clients[index])

                    elif type(receiver) == int:
                        # clients[receiver].send(f'/PRVTE:{title}:{nicknames[receiver]}:{text}:{sender}'.encode(FORMAT))
                        Server_send(f'/msgd8Q7#UMSShKY+u%@{title}d8Q7#UMSShKY+u%@{nicknames[receiver]}d8Q7#UMSShKY+u%@{text}d8Q7#UMSShKY+u%@{sender}', clients[receiver])
                    
            elif msg.startswith('/setname'):
                    parts = msg.split(':')
                    nickname = parts[1]
                    if nickname not in nicknames:
                        clients.append(conn)
                        nicknames.append(nickname)
                        Server_send(f'Your Nickname is {nickname}\n', conn)
                        print(nicknames)
                    else: 
                        print('username is already taken')
                
            #create network
            elif msg.startswith('/NETW'):
                msg = (f'{msg}E!^nLBGs-S!4KM4^{count}')
                
                objectdata = conn.recv(4096)
                network = pickle.loads(objectdata)
                print('Received object:', network)
                network.NETW_id = int(count)
                networklist.append(network)
                count += 1
                network_s.append(objectdata)
                
                
                print(f'NETWORKLIST SERVER: {networklist}')
                O_broadcast(msg, objectdata)
                
            elif msg.startswith('/JOIN'):
                parts = msg.split('v+4t$gxG-+7M^?pj')
                name = parts[1]
                network_id = int(parts[2])
                networklist[network_id].userlist.append(name)
                network_s[network_id] = pickle.dumps(networklist[network_id])
                print('User added to networklist userlist')
                broadcastmsg(msg)
                
            #Group chat message
            elif msg.startswith('/G_BROADCAST'):
                parts = msg.split('kaCSLwgnF=b87-cU')
                try:
                    objectdata = conn.recv(4096)
                    network = pickle.loads(objectdata)
                    print('Received network object:', network)
                except (pickle.UnpicklingError, TypeError):
                    print('DESERIALIZATION FAILED')
                print(network.NETW_id, type(network.NETW_id))
                new_msg = (f'{parts[0]}kaCSLwgnF=b87-cU{parts[1]}kaCSLwgnF=b87-cU{parts[2]}kaCSLwgnF=b87-cU{network.NETW_id}')
                broadcast(new_msg, networklist[int(network.NETW_id)])
            
            #Ask for new information
            elif msg.startswith('/ping'):
                print('ping accepted')
                for i in range(len(networklist)):
                    
                    Server_send((f'/ping7&aJfqzmAb3xG+W#{i}'), conn)
                    conn.sendall(network_s[i])
                    print('Sucessfull network print')
                
            #check name
            elif msg.startswith('/checkname'):
                parts = msg.split('::')
                if parts[1] in nicknames:
                    Server_send('/CHECKED::F', conn)
                else:
                    Server_send('/CHECKED::P', conn)
            elif msg.startswith('/LEAVE'):
                parts = msg.split('eL#eWZ8%#kGa_JMm')
                name = parts[1]
                network_id = int(parts[2])
                if name in networklist[network_id].userlist:
                    networklist[network_id].userlist.remove(name)
                    network_s[network_id] = pickle.dumps(networklist[network_id])
                print('User removed from networklist userlist')
                broadcastmsg(msg)
                
            
        
            else:

              print(f'{addr}, {msg}')
              conn.send('SERVER: MSG received'.encode(FORMAT))


    conn.close()

def start():
    server.listen()
    print(f'SERVER IST LISTENING ON {SERVER}')
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target= handle_client, args= (conn, addr))
        thread.start()

        print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}\n')
        
def O_broadcast(message, network):
    
    for nickname in nicknames:
        conn_index = nicknames.index(nickname)
        Server_send(message, clients[conn_index])
        clients[conn_index].sendall(network)
        
def broadcastmsg(msg):
    for nickname in nicknames:
        conn_index = nicknames.index(nickname)
        Server_send(msg, clients[conn_index])

def broadcast(message, network):
    print(network.userlist)
    print(networklist)
    for nickname in network.userlist:
        if nickname in nicknames:
            conn_index = nicknames.index(nickname)
            print('send message')
            Server_send(message, clients[conn_index])
        else: 
            print('BROADCAST user is not in this server')

print('[STARTING] server is starting...')
start()
