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

def send_receive_client_message():
    pass