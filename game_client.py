import socket
import threading
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

#Main Game Window 
window_main = tk.Tk()
window_main.title("Game Client")

#Initialize network client
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 9090

#Initialize variables that will be used
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 3
your_score = 0
opponent_score = 0

#Top frame consisting of label name and a button widget 
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

#Make a line to separate top frame and middle frame 
top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)

#Connect client's name
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        connect_to_server(your_name)

#Connect to the server
def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) 

        threading._start_new_thread(receive_message_from_server, (client, "m"))

    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

#Receive message from the server
def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score

    while True:
        from_server = sck.recv(4096).decode()

        if not from_server: break

        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Waiting for player 2"
            elif from_server == "welcome2":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Game will start soon"
            lbl_line_server.pack()
        