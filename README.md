# Group-Chat
First Python Project: Programming Group-Chat with TCP/IP Sockets

## Client.py

### class network:
This is the client socket. The network class represents the group rooms and has properties for how many clients can use them and how many subnets, i.e. subgroup rooms, it has (I didn't take the subnets into account in the socket programming because this is unnecessary for my learning experience and just more work might). There are other classes, such as Message, Groupchat. These are important to save the messages and display them on the GUI. (Their also might be some useless code...)

# class Client and User:

The Client class contains socket information and the specific functions for sending private messages, sending information about the connected network and about the messages in the groupchat. Each client has a groupchat_log. When a client sends a message to another client, it can read that message by looking in the file menu and clicking _"Receive Message"_ (looking up the groupchat_log). I created the User class to store the information about ID, username, and which groupchat the client is currently in.
(I guess I could have put this information in the Client class and deleted the User class, but this project was my first Python project and when I started it, I had no idea about sockets, so I programmed a "network" just for fun, but later I found out that I could use sockets to achieve my goal. But after writing a lot of code for the User class, I didn't want to delete everything).


### class: GUI

I used tkinter to create the GUI. 
In order to use the GUI efficiently, you need to create a username. After this you get a user-id, your username is login and a filemenu which contains the function to send private message to another user if you know his user-id or username and the function to reload the gui in order to see new created groupchats).
On the right side, You can create a network (group chat) with any number of allowed users by clicking on the GUI and entering an integer.
The buttons to enter the network should spawn under the label "Join Network" after refreshing the GUI by clicking the function "Update Network" in the filemenu.
I also added a search Function to check if a certain network exist by giving his id.

If you enter a network, you can write with other people in the groupchat. (I adjust the load of messages in the group chat to 3 seconds which results in delayed messages, but to change this, one can change the code in line 777 in Gruppenchat.py from _time.sleep(5)_ to _time.sleep(0.25)_.)

I used tkinter to create the GUI. 
To use the GUI efficiently you have to create a username. After that you get a user id, the username and a file menu which contains the function to send a private message to another user if you know his _user id_ or _username_ and the function to reload the _GUI_ to see newly created group chats).
On the right side, you can create a network (group chat) with any number of allowed users by clicking on the _button : "Create Network"_ and entering an integer.
The buttons to join the network should appear under the label "Join Network" after you update the GUI by clicking  _"Update Network"_ function on the file menu.
I also added a search function to check if a particular network exists by entering its ID.

When you join a network, you can write with other people in your groupchat. (I have set message loading in group chat to 5 seconds, which results in delayed messages, but to change this you can change the code in line 777 in groupchat.py from _time.sleep(5)_ to _time.sleep(0.25)_).

## Server.py

This is the server socket. Depending on the command, it receives and sends messages to users (privately or in group chat(network)). I've used a randomly generated sequence of numbers for certain commands like Broadcast or Private Message to distinguish specific uses. (Maybe there are some methods that are actually useless, but I'm afraid to delete those because they might break my whole code

