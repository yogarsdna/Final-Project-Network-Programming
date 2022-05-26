import tkinter as tk
import socket
import threading
from time import sleep

#Initialize server
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 9090

#Initialize variables that will be used
client_name = " "
clients = []
clients_names = []
player_data = []
num_players = 2

#initialize frame
window = tk.Tk()
window.title("Server")

#Top frame
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", foreground="grey", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStart.configure(fg="grey")
btnStop = tk.Button(topFrame, text="Stop", foreground="grey", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

#Middle frame
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

#The client frame
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

#Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT 
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)

#Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    server.close()

#Accept client requests
def accept_clients(the_server, y):
    while True:
        if len(clients) < num_players:
            client, addr = the_server.accept()
            clients.append(client)

            #Use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    #Send welcome message to client
    client_name = client_connection.recv(4096).decode()
    if len(clients) == 1:
        client_connection.send(b"1")
    elif len(clients) == 2:
        client_connection.send(b"2")

    clients_names.append(client_name)
    update_client_names_display(clients_names) 

    if len(clients) >= num_players:
        sleep(1)

        #Send opponent name
        opponent_name = "opponent_name$" + clients_names[1]
        clients[0].send(opponent_name.encode())
        opponent_name = "opponent_name$" + clients_names[0]
        clients[1].send(opponent_name.encode())
    
    while True:
        data = client_connection.recv(4096).decode()
        if not data: break

        #Get the player choice from received data
        player_choice = data[11:len(data)]

        msg = {
            "choice": player_choice,
            "socket": client_connection
        }

        if len(player_data) < num_players:
            player_data.append(msg)

        if len(player_data) == num_players:
            #Send player 1 choice to player 2 and vice versa
            opponent_choice = "1:" + player_data[1].get("choice")
            player_data[0].get("socket").send(opponent_choice.encode())

            opponent_choice = "0:" + player_data[0].get("choice")
            player_data[1].get("socket").send(opponent_choice.encode())
        

            player_data = []

    #Find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  

def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx

def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)

window.mainloop()