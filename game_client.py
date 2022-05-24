import socket
import threading
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

#Initialize network client
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 9090

#Main Game Window 
window_main = tk.Tk()
window_main.title("Game Client")
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 3
your_score = 0
opponent_score = 0

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

#Connect client's name :
def connect():
    global your_name
    if len(your_name) < 1:
        pass