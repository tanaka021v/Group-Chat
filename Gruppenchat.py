import tkinter as tk
from tkinter import messagebox
import socket
import threading
import pickle
import time

from tkinter import font
from tkinter import simpledialog
from tkinter import DISABLED    
from tkinter import messagebox
from tkinter import ttk

import json

class network():
    networklist = []
    netw_id = 0
    SUB_id = 0
    location = {}

    def __init__(self,  ntwsize : int, sub_id = -1):
        self.userlist = []
        self.networkcreator = None
        self.NETW_id = None
        
        self.NETW_size = ntwsize
        if(sub_id != -1): 
            self.SUB_id = network.SUB_id
            network.SUB_id += 1
        else:
            self.SUB_id = sub_id
            # self.networklist.append((self, self.NETW_id, sub_id))
        self.subnetwork = []

        print('Initialize Network... | ID: ' + str(self.NETW_id) + ' | ' + str(self))
         
    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if(self.index > len(self.userlist)-1):
            raise StopIteration
        else:
            user_element = self.userlist[self.index]
            self.index += 1
            return user_element


   
    def searchNetwork_path(self, Sub_id, route=None):
        if route is None:
            route = []
        route.append( (self, self.SUB_id))
        if self.SUB_id == Sub_id:
            
            return route
        shortest_route = None
        for i in range(len(self.subnetwork)):
            result = self.subnetwork[i][0].searchNetwork_path(Sub_id, route.copy())
            if result is not None:
                sub_route = result
                if shortest_route is None or len(sub_route) < len(shortest_route):
                    shortest_route = sub_route
        
        return shortest_route

      
    def searchNetwork_SUB(self, Sub_id):
        
        if self.SUB_id == Sub_id:
            print(f'Network was found | Information NETW_ID: {self.NETW_id}, SUB_id: {self.SUB_id }')
            return self
        for i in range(len(self.subnetwork)):
            result = self.subnetwork[i][0].searchNetwork_SUB(Sub_id)
            if result is not None:
                
                return result
            
        return None
    
    def __SearchinOwnNETW(self, NETW_id):
            if self.NETW_id == NETW_id:
                print(f'Network was found | Information -> NETW_ID: {self.NETW_id}, SUB_id: {self.SUB_id }')
                return self
            for i in range(len(self.subnetwork)):
                result = self.subnetwork[i][0].__SearchinOwnNETW(NETW_id)
                if result is not None:
                    return result
            return None
        
    def searchNetwork_NETW(self, NETW_id):
        print('--------------------------------------------------------------------------------------------------------------------------')
        print(f'Searching Network-id: {NETW_id}')
        temp = self.__SearchinOwnNETW(NETW_id)
        if temp is None:
            print('No Result in own Network! Connecting to network list, traversing through every network')
            result = None
            for i in range(len(network.networklist)):
               if(self.networklist[i][0] !=self ):
                print(f'Search in Root network: {network.networklist[i][0].NETW_id}')
                result = network.networklist[i][0].__SearchinOwnNETW(NETW_id)
               
               if result is not None:
                    return result
            return None
        else:
            return temp
        
    
    def print_Network(self):
        liste = [self.SUB_id]
  
        print(f'Information -> Network ID: {self.NETW_id} | Subnet ID: {self.SUB_id}')
        for i in range(len(self.subnetwork)):
            
            liste.append(self.subnetwork[i][0].print_Network())
        return liste

class groupchat(network):
    def __init__(self):
        self.groupchat_log = {
        
        }
        
    
class message():
    message_id = 0
    def __init__(self, title : str, receiver, text : str, sender ):
        notifications = []
        self.message = {
            'title': title,
            'receiver': receiver,
            'text': text,
            'sender': sender
        }
        self.message_id = message.message_id
        message.message_id += 1
        
class cache(groupchat, message):
    
    def __init__(self, network):

        self.user_information = {}  
        self.network = []
        self.notifications = []
        self.message_log = {}    
class client(cache):
    DISCONNECT_MESSAGE = '!DISCONNECT'
    
    def __init__(self):
        #socket
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.ADDR = (self.SERVER, self.PORT)
        self.network_addr = ('5.tcp.eu.ngrok.io', 13992)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.count = 0
        
        self.client_cache = cache(None)
        self.client_groupchat = groupchat()
        self.user_start()
        
        
    def send_private_message(self,nickname, message):
        print(f'Send PRIVATE MESSAGE to {nickname}')
        complete_msg = f'/PRVT:{nickname}:{message}'

        message_length = len(complete_msg.encode(self.FORMAT))
        send_length = str(message_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))

        self.client.send(send_length)
        self.client.send(complete_msg.encode(self.FORMAT))
        
    def user_start(self):
        thread = threading.Thread(target = self.handle_server)
        thread.start()
        
    def handle_server(self):
        while True:
            msg_length =  self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                try:
                    msg_length = int(msg_length)
                except ValueError:
                    msg_length = len(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                print(msg)
                #send private message
                if msg.startswith('/msg'):
                    print('Private Message receive')
                    parts = msg.split('d8Q7#UMSShKY+u%@')
                    receiver = parts[2]
                    title = parts[1]
                    text = parts[3]
                    sender = parts[4]
                    
                    message_var = message(title, receiver, text, sender )
                   
                    self.client_cache.message_log.update({f'{message.message_id} : {sender}' :message_var.message})
                    self.client_cache.notifications.append(f'{message.message_id} : {sender}' )
                #send group message
                elif msg[:12] == '/G_BROADCAST':                            
                    parts = msg.split('kaCSLwgnF=b87-cU')
                    message1 = (f'[{parts[1]}]: {parts[2]}')
                    self.client_groupchat.groupchat_log[f'{parts[3]}'].add(message1)
             

                #Create Network
                elif msg[:5] == '/NETW': 
                    try:
                        parts = msg.split('E!^nLBGs-S!4KM4^')
                        
                        objectdata = self.client.recv(4096)   #Aendern?
                        network1 = pickle.loads(objectdata)
                        
                        print('Received network object:', network1)
                        
                        if network1 not in network.networklist:
                                network1.NETW_id = parts[1]
                                network.networklist.append(network1)
                                print('ADDED NETWORK TO NETWORKLIST')
                                print(network.networklist)
                        else:
                                print('network already exist')
                    except (pickle.UnpicklingError, TypeError):
                        print('DESERIALIZATION FAILED')
                        
                elif msg.startswith('/JOIN'):
                    parts = msg.split('v+4t$gxG-+7M^?pj')
                    name = parts[1]
                    network_id = int(parts[2])
                    if name not in network.networklist[network_id]:
                        network.networklist[network_id].userlist.append(name)
                   
                    print('User added to networklist userlist')
                    
                
                #Ask for new information 
                elif msg[:5] == '/ping':
                    print('ping accepted')
                    parts = msg.split('7&aJfqzmAb3xG+W#')
                    objectdata = self.client.recv(4096)
                    network1 = pickle.loads(objectdata)
                    
                    if network1 not in network.networklist:
                        network1.NETW_id = parts[1]
                        network.networklist.append(network1)
                elif msg[:6] == '/LEAVE':
                    parts = msg.split('eL#eWZ8%#kGa_JMm')
                    name = parts[1]
                    network_id = int(parts[2])
                    if name in network.networklist[network_id]:
                        network.networklist[network_id].userlist.remove(name)
                   
                    print('User remove from networklist userlist')
               
                            
                #username check
                elif msg.startswith('/CHECKED'):
                    parts = msg.split('::')
                    if parts[1] == 'F':
                        self.name_check = False
                    elif parts[1] == 'P':
                        self.name_check = True
                time.sleep(0.25)
                
    
    def client_leave_network(self, network_id, name):
        self.send_(f'/LEAVEeL#eWZ8%#kGa_JMm{name}eL#eWZ8%#kGa_JMm{network_id}')
    
    
    def client_join_network(self, network_id,name):
        self.send_(f'/JOINv+4t$gxG-+7M^?pj{name}v+4t$gxG-+7M^?pj{network_id}')
       
    
    def groupchat_sync(self, network):
        self.send_(f'/NETW')
        self.USER_send_object(network)
        
    def ping_for_network(self):
        self.send_(f'/ping')
                
    def send_(self,msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        
    def send_private_emessage(self, title, receiver, text, sender):
        print(f'Send PRIVATE MESSAGE to {receiver}')
        complete_msg = (f'/msgd8Q7#UMSShKY+u%@{title}d8Q7#UMSShKY+u%@{receiver}d8Q7#UMSShKY+u%@{text}d8Q7#UMSShKY+u%@{sender}')
        self.send_(complete_msg)
    
    def broadcastG(self,name, message, network):
        message = (f'/G_BROADCASTkaCSLwgnF=b87-cU{name}kaCSLwgnF=b87-cU{message}')
        self.send_(message)
        self.USER_send_object(network)

    def USER_send_object(self, object1):
        serialized_object = pickle.dumps(object1)
        self.client.sendall(serialized_object)
    
        
class user(client): 
    
    
    user_id = 0
    name_list = []
    
    def __contains__(self, name1_list):
        return name1_list in user.name_list
    
    def __init__(self, name, status = None):

        self.client1 = client()
    
        if name not in user.name_list:
            self.name = name
            self.client1.send_(f'/setname:{self.name}')
        else:
            name_input = input('Name is already taken, choose another: ')
            self.__init__(str(name_input),status)
            return

        self.status = status
        self.USER_id = user.user_id
        user.user_id += 1
        
        self.user_cache = cache(None)
        self.user_cache.user_information[f'{self.USER_id}'] = {
                'user_id' : self.USER_id,
                'username': self.name,
                'network' : [],
                'sub_network' : []
        }
        
        print('Create User: '+ str(name) + ' - ' + str(self.USER_id) + '  --> SUCCESS')
        print('--------------------------------------------------------------------------------------------------------------------------')
        
                
    def Connect_USER_to_NETW(self, network):
        
        print('     Connecting User: ' + str(self.USER_id) + ' | Attempt Network: ' + str(network.NETW_id) )
        if(len(network.userlist) < network.NETW_size):
            print('User: ' + str(self.USER_id) + ' ----> connected to network | ID: ' + str(network.NETW_id) )
            print()
            network.userlist.append(self.name)
            self.user_cache.user_information[f'{self.USER_id}']['network'].append((network, network.NETW_id))
            self.user_cache.user_information[f'{self.USER_id}']['sub_network'].append([])
            self.user_cache.network.append(network)
               
            
        else:
            print('Network ' + str(network.NETW_id) + ' has no storage for more users')
            templist = self.networklist
            if (network, network.NETW_id) in templist:
                 templist.remove((network, network.NETW_id))

            print('Here are other avaible networks: ')
            second_elements = [str(element[1]) for element in self.networklist]  # Zweite Elemente als Zeichenketten sammeln
            joined_elements = ', '.join(second_elements)                         # Zeichenketten mit einem Komma und Leerzeichen trennen
            print(joined_elements)
            del templist
            inputs = input(str(self.USER_id) +': Choose a new Network: ')
            if(int(inputs) <= len(self.networklist)-1):
                self.Connect_USER_to_NETW(self.networklist[int(inputs)-1][0])
        
                
        print('---------------------------------------------------FINISHED CONNECTION---------------------------------------------------')
         
    def USER_leaveNetwork(self, network):
      
            if self.name in network.userlist:
              
                if network.SUB_id == -1:
                    for elements in self.user_cache.user_information[f'{self.USER_id}']['sub_network'][self.user_cache.network.index(network)]:
                        if elements is not None:
                            temp =  network.searchNetwork_SUB(elements[1])
                            temp.userlist.remove(self.name)
                            print(f'Leaving Sub network: {temp.NETW_id, temp.SUB_id}')
                    if self.name in network.userlist:
                        network.userlist.remove(self.name)
                    
                    self.user_cache.user_information[f'{self.USER_id}']['sub_network'].remove(self.user_cache.user_information[f'{self.USER_id}']['sub_network'][self.user_cache.network.index(network)])
                    self.user_cache.user_information[f'{self.USER_id}']['network'].remove( (network, network.NETW_id))
                    self.user_cache.network.remove(network)
                    print(f'{self.name} is leaving network id: {network.NETW_id}')
                    return
            else:
                print('User is not in this network')
            
    def USER_requestEnteringNetwork(self, NETW_id, Sub_id = None, currentnet = None):
        print('--------------------------------------------------------------------------------------------------------------------------')
        network_avaible = False
        for elements in network.networklist:
            if NETW_id in elements:
                print(f'Network ID: {elements[1]} is available')
                network_avaible =  True
                root_network = elements[0]
                break
            
        if network_avaible:    
            sub_network = root_network.searchNetwork_SUB(Sub_id)
            
            if sub_network is not None :
                if( (self.name, self.USER_id, self) not in root_network.userlist):    
                    if(len(root_network.userlist) <= root_network.NETW_size):
                        self.user_cache.user_information[f'{self.USER_id}']['sub_network'].append([])
                        # self.user_cache.network.userlist.remove((self.name, self.USER_id, self))
                        root_network.userlist.append(self.name)
                        self.user_cache.user_information[f'{self.USER_id}']['network'].append( (root_network, root_network.NETW_id) )
                        self.user_cache.network.append( root_network)
                        print(f'User_name : {self.name}, User_id: {self.USER_id} connected to network {root_network, root_network.NETW_id} ')     
                    else:
                        print(f'The Network , you are trying to enter, has reached max capacity | ID: {root_network.NETW_id}')
                else:
                    print(f'User {self.name, self.USER_id} is already in this (root) network')
                    
                if Sub_id is not None:
                            if ( self.name not in sub_network.userlist):   
                                print()
                                if(sub_network.NETW_size >= len(sub_network.userlist) ):
                                    path = root_network.searchNetwork_path(Sub_id) 
                                    
                                    for elements in path[1:]:
                                        elements[0].userlist.append(self.name)      
                                    self.user_cache.user_information[f'{self.USER_id}']['sub_network'][self.user_cache.network.index(root_network)] = path[1:]
                                    
                                    temp = self.user_cache.user_information[f'{self.USER_id}']['sub_network'][-1][-1]
                                    print(f'User_name : {self.name}, User_id: {self.USER_id} connected to network {root_network, root_network.NETW_id} and subnetwork {temp}')
                                    print(self.user_cache.user_information[f'{self.USER_id}']['sub_network'])
                                else:
                                    print(f'The Subnetwork with the SubID: {sub_network.SUB_id} has reached max capacity')
                            else:
                                print(f'User {self.name, self.USER_id} is already in this (sub) network')  
            else:
                        print(f'Subnetwork {Sub_id} does not exist in this network!')
                        print('Please Try again')
        else:
                print(f'No Root Network found with the NETW_id: {NETW_id}')
                print('Please Try again')
        
        print('--------------------------------------------------------------------------------------------------------------------------')

    def USER_findLocation(self):
        print()
        print(f'User {self.name, self.USER_id} location is')
        print(f'Network:                                              last Sub_Network:')
        if self.user_cache.user_information[f'{self.USER_id}']['network'] is not None:
            if len(self.user_cache.user_information[f'{self.USER_id}']['sub_network']) > 0:
                return self.user_cache.user_information[f'{self.USER_id}']['network'], self.user_cache.user_information[f'{self.USER_id}']['sub_network'][-1][-1]
            else: 
              return self.user_cache.user_information[f'{self.USER_id}']['network']
 
            
    def USER_receive_MESSAGE(self):
        print('--------------------------------------------------------------------------------------------------------------------------')
        print('Your Message View')
        print()
        for i in range (len(self.client1.client_cache.message_log)):
            print(f"title: {self.client1.client_cache.message_log[self.user_cache.notifications[i]]['title']}")
            print(f"receiver: You")
            print(f"message: {self.client1.client_cache.message_log[self.user_cache.notifications[i]]['text']}")
            print(f"sender: {self.client1.client_cache.message_log[self.user_cache.notifications[i]]['sender']}")
            print('--------------------------------------------------------------------------------------------------------------------------')
            print(self.client1.client_cache.message_log)


class GUI(tk.Tk,user):
    a = 0
    def GUI_createUser(self):
        self.dialogfenster = tk.Toplevel(self.window)
        self.dialogfenster.geometry("600x150")
        label = tk.Label(self.dialogfenster, text='Type your username: ', font = ('Arial', 18))
        label.pack(anchor = tk.NW, padx = 10, pady = 10)
        
        self.textbox = tk.Text(self.dialogfenster, height=1, width=100, font=('Arial', 25))
        self.textbox.bind('<KeyPress>', lambda event: self.on_keypress(event))
        self.textbox.pack(padx=10, pady=10)   
        
        
    def on_keypress(self, event):
       
        if event.keysym == 'Return':
            self.textbox.delete('end - 1c')
            self.username = self.textbox.get('1.0', tk.END).strip()
            self.textbox.delete('1.0', tk.END)
            self.dialogfenster.destroy()
            self.user = user(self.username)
            self.user.client1.ping_for_network()
            self.create_user_button.destroy()  # Entferne den Button
        
        # Erstelle das neue Label an derselben Position wie der Button
            # self.username_label = tk.Label(self.button_frame, text=f'USERNAME: [{self.username}]\nID: [{self.user.USER_id}]', font= ('Montserrat',12, 'bold'))
            # self.username_label.pack(side=tk.LEFT, anchor=tk.NW, padx=15, pady=20)
            self.new_textboxt = tk.Text(self.button_frame, width=30, height=4, font= ('Montserrat',12, 'bold'), bg = f'{self.window.winfo_toplevel().cget("background")}' )
            self.new_textboxt.insert(0.0, f'USERNAME: [{self.username}]\nID: [{self.user.USER_id}]\nNetwork:[{None}]\nSub Network:[{None}]')
            self.new_textboxt['state'] = DISABLED
            self.new_textboxt.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
            
            menubar= tk.Menu(self.window, bg = self.window.winfo_toplevel().cget('background'))
            filemenu = tk.Menu(menubar, tearoff = 0,  bg = self.window.winfo_toplevel().cget('background'))
            filemenu.add_command(label = 'send private Message', command = self.PRVT_send_messages)
            filemenu.add_command(label ='receive Message', command =  self.receive_message)
            actionmenu = tk.Menu(menubar, tearoff= 0)
            actionmenu.add_command(label = 'Update Networks', command = self.network_buttons)
            menubar.add_cascade(menu = filemenu, label = 'Add ons')
            menubar.add_cascade(menu = actionmenu, label = 'Networks')
       
            
            
            self.window.config(menu = menubar)
            
            
        
    def PRVT_send_messages(self):
       
        message_window = tk.Toplevel(self.window)
        message_window.geometry('1000x800')
        message_frame = tk.Frame(message_window)
        message_frame.place(x=0, y=0, relheight=0.9, relwidth=1)

        title_frame  = tk.Frame(message_frame)
        title_frame.place(x=0,y=20, relheight= 0.1, relwidth = 1.0)
        title_label = tk.Label(title_frame, text='Title: ', font=('Arial', 18, 'bold'))
        title_label.pack(side = tk.LEFT, anchor = tk.NW, padx = 10, pady = 10)
        title_box = tk.Text(title_frame, font=('Arial', 18), width=60)
        title_box.pack(padx=10, pady=10)
        
        receiver_frame = tk.Frame(message_frame)
        receiver_frame.place(x= 0, y = 70, relheight= 0.1, relwidth = 1.0)
        receiver_label = tk.Label(receiver_frame, text='Receiver ID: ', font=('Arial', 18, 'bold'))
        receiver_label.pack(side = tk.LEFT, anchor = tk.NW, padx = 10, pady = 10)
        receiver_box = tk.Text(receiver_frame, font=('Arial', 18), width=60)
        receiver_box.pack(padx=10, pady=10)
        
        text_frame = tk.Frame(message_frame)
        text_frame.place(x= 0, y = 150, relheight= 0.6, relwidth = 1.0)
        text_label = tk.Label(text_frame, text='Message: ', font=('Arial', 18, 'bold'))
        text_label.pack(side = tk.LEFT, anchor = tk.NW, padx = 10, pady = 10)
        text_box = tk.Text(text_frame, font=('Arial', 18), width=60, height = 30)
        text_box.pack(side = tk.LEFT, anchor = tk.NW,padx=10, pady=10)
        
        send_button = tk.Button(message_frame, text = 'Send Message', font = ('Arial', 18), command =  lambda : self.PRVT_messagebox_enter(receiver_box, text_box, title_box))
        send_button.pack(side = tk.LEFT, anchor = tk.SW, padx = 60, pady = 60)
        
    def receive_message(self):
        self.rcvwindow = tk.Toplevel(self.window)
        self.rcvwindow.geometry('1000x800')
        
        _frame = tk.Frame(self.rcvwindow)
        _frame.pack(fill=tk.X, side = tk.TOP)
        
        text = tk.Label(_frame, text='RECEIVED MESSAGE', font=('Arial', 16, ' bold'))
        text.pack(pady=5, anchor=tk.NW)
        
        length = len(self.user.client1.client_cache.notifications)
        
        if length == 0:
            notext = tk.Label(_frame, text='NO MESSAGE RECEIVED', font=('Arial',14,'bold'))
            notext.pack(side = tk.LEFT, pady=5)
        else:
            notext = tk.Label(_frame, text=f'{length} MESSAGE(S) RECEIVED', font=('Arial', 14, 'bold'))
            notext.pack(padx=20, pady=20)
        
        s_frame = tk.Frame(self.rcvwindow)
        s_frame.pack(fill=tk.BOTH, expand=True, side = tk.LEFT, anchor = tk.NW)
        

        canvas = tk.Canvas(s_frame)
        canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        scrollbar = ttk.Scrollbar(s_frame, orient = 'vertical', command = canvas.yview)
        scrollbar.pack(side =  tk.RIGHT, fill = tk.Y)
        
        
          
        
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.bind('<Configure>', lambda event : canvas.configure(scrollregion = canvas.bbox('all')))

        scroll_frame =ttk.Frame(canvas)
        for i in range(length):
            button = tk.Button(scroll_frame, text=self.user.client1.client_cache.notifications[i], width = 50, height = 5, font=('Arial', 12), command=lambda i=i: self.openMESSAGE(self.user.client1.client_cache.notifications[i]))
            button.grid(row=i, column=0, sticky=tk.W, padx=10, pady=10)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))  
        canvas.create_window((0,0), window = scroll_frame, anchor = tk.NW)
        canvas.bind_all('<MouseWheel>', lambda event : canvas.yview_scroll(int(-1 * (event.delta/120)), 'units'))
        
      
 
        

        
    def openMESSAGE(self, noti):
        msgbutton = tk.Toplevel(self.rcvwindow)
        msgbutton.geometry('800x500')
        msgbox = tk.Text(msgbutton, font= ('Arial', 16, 'bold'))
        
        title = (f"title: {self.user.client1.client_cache.message_log[noti]['title']}")
        message = (f"message: {self.user.client1.client_cache.message_log[noti]['text']}")
        sender =  (f"sender: {self.user.client1.client_cache.message_log[noti]['sender']}")
        string = title + '\n' + message + '\n'+ sender 
        msgbox.insert(tk.END, string)

        msgbox['state'] = DISABLED
        msgbox.pack(pady = 10, padx = 10)
        
    def PRVT_messagebox_enter(self, receiver_box, text_box, title_box):
        title = title_box.get('1.0', tk.END).strip()
        receiver = receiver_box.get('1.0', tk.END).strip()
        text = text_box.get('1.0', tk.END).strip()
        self.user.client1.send_private_emessage(title ,receiver,text, self.user.name)
      
            
        title_box.delete('1.0', tk.END)
        receiver_box.delete('1.0', tk.END)
        text_box.delete('1.0', tk.END)
        
        
    def GUI_createNetwork(self):
        if self.new_window is None:
            self.__GUI_createNetwork()
        else:
            if self.new_window.winfo_exists():
                # Bringen Sie das Fenster in den Vordergrund
                self.new_window.lift()
            else:
                # Wenn das Fenster nicht mehr existiert, öffnen Sie ein neues 
                self.__GUI_createNetwork()
                
    def __GUI_createNetwork(self):
            self.new_window  = tk.Toplevel(self.button_frame)
            self.new_window.geometry('600x150')
            label1 = tk.Label(self.new_window, text = 'Network size? ', font = ('Arial', 18))
            label1.pack(anchor = tk.NW, padx = 10, pady = 10)
            self.network_textbox = tk.Text(self.new_window, height = 1, width = 100, font=('Arial', 25))
            self.new_window.protocol('WM_DELETE_WINDOW', self.close_networkbutton)
            self.network_textbox.bind('<KeyPress>', lambda event: self.network_keypress(event))
            self.network_textbox.pack(padx=10, pady=10)
    def close_networkbutton(self):
        self.new_window.destroy()
        self.new_window = None
        return
        
        # network1 = network()
        
    def network_keypress(self, event):
        if event.keysym == 'Return':
            if self.user is not None:
                self.network_textbox.delete('end - 1c')
                size = self.network_textbox.get('1.0', tk.END).strip()
                
                try:
                        self.network_textbox.delete('1.0', tk.END)
                        self.new_window.destroy()
                        new_size = int(size)
                        create_network = network(new_size)
                        create_network.networkcreator = self.user.name
                        self.user.client1.groupchat_sync(create_network)
                        
                        self.network_buttons()
                        # Aktualisierung der Scrollregion
                        self.canvas.update_idletasks()
                        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
                        
                        return
                except ValueError:
                        # Wenn die Konvertierung zu einem Integer fehlschlägt
                        # oder new_size kein ganzzahliger Wert ist
                        messagebox.showinfo('Information', 'Invalid network size, enter a whole number')
                        print("Invalid network size")
            else:
                messagebox.showinfo('Information', 'You do not have an user account')
                return
    def network_buttons(self):
        button_list = []  # Liste für Buttons erstellen
        length = 0
        for button in button_list:
            button.destroy()
        if len(network.networklist) != 0:
            for length in range(len(network.networklist)):
                button = tk.Button(self.scroll_frame, text=f'Network ID: {network.networklist[length].NETW_id} | Network Size: {len(network.networklist[length].userlist)}/{network.networklist[length].NETW_size} | from User: {network.networklist[length].networkcreator}', font=('Arial', 18, 'bold'), width=50, height=2,command=lambda length=length: self.join_Network(network.networklist[length], button))
                button.grid(row=length, column=0)
                button_list.append(button)  # Button zur Liste hinzufügen

            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

                
            

    def join_Network(self, network, button):
        
        if network.NETW_size > len(network.userlist):
            if self.user.name not in network.userlist:
                self.NETconnection = True
                # self.user.Connect_USER_to_NETW(network)
                self.user.client1.client_join_network(name = self.user.name, network_id = network.NETW_id)
                self.user.client1.client_groupchat.groupchat_log[f'{network.NETW_id}'] = set()

                network_window = tk.Toplevel()
                network_window.geometry('1200x720')
                
                self.new_textboxt = tk.Text(network_window, width=30, height=4, font= ('Montserrat',12, 'bold'), bg = f'{network_window.winfo_toplevel().cget("background")}' )
                self.new_textboxt.insert(0.0, f'USERNAME: [{self.user.name}]\nID: [{self.user.USER_id}]\nNetwork:[{network.NETW_id}]\nSub Network:[{None}]')
                self.new_textboxt['state'] = DISABLED
                self.new_textboxt.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

                new_frame = ttk.Frame(network_window)
                new_frame.place(x=0, y=100, relwidth=1, relheight=0.7)
                
                message_canvas = tk.Canvas(new_frame)
                message_canvas.pack(fill=tk.BOTH, expand=True)

                message_box = tk.Text(message_canvas, width=100, height=50, font=('Montserrat', 12, 'bold'))
                message_box.pack(padx=10, pady=10, anchor=tk.NW)
                message_box['state'] = DISABLED
                
                scrollbar = ttk.Scrollbar(new_frame, orient='vertical', command=message_canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                message_canvas.configure(yscrollcommand=scrollbar.set)
                message_canvas.bind('<Configure>', lambda event: message_canvas.configure(scrollregion=message_canvas.bbox('all')))

                scroll_frame = ttk.Frame(message_canvas)
                message_canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)
                
                # Nachdem Sie das Fenster mit create_window erstellt haben,
                # aktualisieren Sie die scrollregion noch einmal
                # scrollbar.bind('<MouseWheel>', lambda event: self.message_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units'))

                message_box1 = tk.Text(network_window, width=100, height=5, font=('Montserrat', 12, 'bold'))
                message_box1.place(x=10, y=600)
                message_box1.bind('<KeyPress>', lambda event: self.GUI_send_message(event, message_box1, message_box, network))
                
                message_canvas.update_idletasks()
                message_canvas.configure(scrollregion=message_canvas.bbox('all'))
                
                
                # self.button = tk.Button(self.scroll_frame, text=f'Network ID: {network.NETW_id} | Network Size: {len(network.userlist)}/{network.NETW_size} | from User: {self.user.name}', font=('Arial', 18, 'bold'), width=50, height=2, command = lambda:  self.join_Network(network)) 
                button.configure(text=f'Network ID: {network.NETW_id} | Network Size: {len(network.userlist)}/{network.NETW_size} | from User: {network.networkcreator}')
                thread = threading.Thread(target = self.updateForum, args = (message_box,message_canvas,network))
                thread.start()
                
                network_window.protocol('WM_DELETE_WINDOW', lambda: self.on_close(network, network_window) )
            else:
                messagebox.showinfo('Information', 'The User is already in this network')
        else:
            messagebox.showinfo('Information', 'Network size is already full')
            
    def on_close(self, network,  network_window):
        self.NETconnection = False
        
        self.user.client1.client_leave_network(network_id = network.NETW_id, name = self.user.name)
        self.network_buttons()
        network_window.destroy()
  
    def GUI_send_message(self, event, message_box1, message_box, network):
        if event.keysym == 'Return':
            message = message_box1.get('1.0', tk.END).strip()
            self.user.client1.broadcastG(self.user.name, message, network)
            message_box1.delete('1.0', tk.END)
            message_box['state'] = 'disabled'
            
    def updateForum(self, message_box, message_canvas, network):
        while self.NETconnection:
            print((f'{network.NETW_id}'))
            time.sleep(5)
            if self.user.client1.client_groupchat.groupchat_log[f'{network.NETW_id}'] != set():
                print('Yes Yes Yers')
                try:
                    message_box['state'] = 'normal'
                    for value in self.user.client1.client_groupchat.groupchat_log[f'{network.NETW_id}']:
                        message_box.insert(tk.END, f'{value}\n')
                        print(value)
                        print('Inserting')
                except Exception as e:
                    print(f"Error updating message box: {e}")
                finally:
                    message_box['state'] = 'disabled'
                message_canvas.update_idletasks()
                message_canvas.configure(scrollregion= message_canvas.bbox('all'))
                self.user.client1.client_groupchat.groupchat_log[f'{network.NETW_id}'] = set()
            
        
        
    def entryreturn(self, event):
        if self.user is not None:
            if (len(network.networklist) != 0):
                entry_text = self.entry.get().strip()
                
                try:
                    networkid = int(entry_text)
                    if networkid < len(network.networklist):
                        print(networkid)
                        print(len(network.networklist))
                        
                        self.entrybutton = tk.Button(self.button_frame, text=f'Network ID: {network.networklist[networkid].NETW_id} | Network Size: {len(network.networklist[networkid].userlist)}/{network.networklist[networkid].NETW_size} | from User: {network.networklist[networkid].networkcreator}', font=('Arial', 18, 'bold'), width=50, height=1, command = lambda:  self.join_Network(network.networklist[networkid], self.entrybutton))
                        self.entrybutton.place(x = 5, y = 180)
                    else:
                        messagebox.showinfo('information', 'Network with this ID does not exist')
                    
                except ValueError:
                    messagebox.showinfo('Information', 'Invalid Network ID')
            else:
                messagebox.showinfo('Information','There are no networks')
        else:
            messagebox.showinfo('Information', 'First, create a User Account')
        
    def close_window(self):
        if self.user is not None:
            self.NETconnection = False
            self.window_connected =  False
            if self.user.name in user.name_list:
                user.name_list.remove(self.user.name)
            if self.user.user_cache.user_information[f'{self.user.USER_id}']['network'] != set():
                for elements in self.user.user_cache.user_information[f'{self.user.USER_id}']['network']:
                    if self.user.name in elements[0].userlist:
                        elements[0].userlist.remove(self.user.name)
                        print('deleting user from root network')
            if self.user.user_cache.user_information[f'{self.user.USER_id}']['sub_network'] != set():
                for elements in self.user.user_cache.user_information[f'{self.user.USER_id}']['sub_network']:
                    for another in elements:
                        if self.user.name in another.userlist:
                            another.userlist.remove(self.user.name)
                            print('deleting user from subnetwork')
            self.user.client1.send_(client.DISCONNECT_MESSAGE)
            del self.user.client1
            del self.user
            
        self.window.destroy()
    def __init__(self):
        #Haupt Menü
        self.user = None
        self.window = tk.Tk()
        
        self.window.geometry('1200x720')
        self.window.title('Andito')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        # self.window.resizable(False,False)
        self.label1 = tk.Label(self.window, text='Andito', font = ('Roboto', 18))
        self.label1.pack(padx= 10, pady = 10)
        
        #Frame mit Network und User Button
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(padx = 10, pady  = 10, fill = tk.BOTH, expand = True)
        self.new_window = None
        
        
        self.create_user_button = tk.Button(self.button_frame, text='Create User', font = ('Arial', 10, 'bold'), width=30, height=4, command = self.GUI_createUser)
        self.create_user_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        self.create_network_button = tk.Button(self.button_frame, text='Create Network',font = ('Arial', 10, 'bold'), width=30, height=4, command = self.GUI_createNetwork)
        self.create_network_button.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)
        
        label = tk.Label(self.button_frame, text ='Search Network ID: ', font = ('Arial', 14, 'bold'))
        label.place(x = 5, y = 100)
        self.entry = tk.Entry(self.button_frame, width = 15, font = ('Arial', 14, 'bold'))
        self.entry.place(x = 5, y = 140)
        self.entry.bind('<Return>', self.entryreturn)
        
        #Network Frame
        self.network_frame  = ttk.Frame(self.window)
        self.network_frame.place(x = 0, y = 360, relwidth = 1, relheight= 0.5)
        label1 = tk.Label(self.network_frame, text= 'Join Network: ', font = ('Arial', 16, 'bold'))
        label1.pack(side = tk.LEFT, anchor = tk.NW)

        self.canvas = tk.Canvas(self.network_frame)
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        scrollbar = ttk.Scrollbar(self.network_frame, orient = 'vertical', command = self.canvas.yview)
        scrollbar.pack(side =  tk.RIGHT, fill = tk.Y)
        
        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.canvas.bind('<Configure>', lambda event : self.canvas.configure(scrollregion = self.canvas.bbox('all')))

        self.scroll_frame =ttk.Frame(self.canvas)

        self.canvas.create_window((0,0), window = self.scroll_frame, anchor = tk.NW)
        self.canvas.bind_all('<MouseWheel>', lambda event : self.canvas.yview_scroll(int(-1 * (event.delta/120)), 'units'))
        self.network_frame.pack_propagate(False)
        self.window.after(0, self.window.mainloop) 
        

if __name__ == '__main__':

    gui = GUI()
    tk.mainloop()
    
