import tkinter as tk
import socket
import threading

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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, " "))

#Stop server function
def stop_server():
    global server

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

    if len(clients) >= num_players:

        #Send opponent name
        opponent_name = "opponent_name$" + clients_names[1]
        clients[0].send(opponent_name.encode())
        opponent_name = "opponent_name$" + clients_names[0]
        clients[1].send(opponent_name.encode())