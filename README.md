##Group-Chat: My First Python Project with TCP/IP Sockets
##Client.py
Network Class:
The Network class handles the client socket. It represents group rooms and includes properties for the number of clients it can accommodate and the number of subnets (subgroup rooms), although subnet functionality isn't implemented. Other classes like Message and Groupchat help save messages and display them on the GUI.

##Client and User Classes:
The Client class manages socket information and functions for sending private messages, sharing network information, and managing group chat messages. Each client maintains a group chat log, allowing them to review messages sent to them. Additionally, the User class stores client information such as ID, username, and current group chat. Originally, I created the User class without knowing about sockets, intending to manage users within a "network." While this approach may not be optimal, I kept it due to the significant code investment.

##GUI Class:
I utilized tkinter to create the GUI. Upon launching, users are prompted to create a username. Once set, they receive a user ID and can access a file menu offering options to send private messages to other users and refresh the GUI to view new group chats. On the right side of the GUI, users can create group chats with any number of participants by clicking the "Create Network" button and entering the desired number. After updating the GUI with the "Update Network" function, buttons to join these networks appear under the "Join Network" label. Additionally, I implemented a search function allowing users to check if a specific network exists by entering its ID. Within group chats, messages load every 5 seconds, although this delay can be adjusted by modifying the code in groupchat.py.

##Server.py
The Server module manages the server socket. Depending on received commands, it dispatches messages to users privately or within group chats (networks). Commands like Broadcast or Private Message are distinguished using randomly generated sequence numbers. While some methods may seem redundant, I hesitate to remove them fearing potential disruptions to the code's functionality.
