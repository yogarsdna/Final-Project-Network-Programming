import socket
import threading
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from time import sleep

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
btn_connect = tk.Button(top_welcome_frame, text="Connect", foreground="blue", command=lambda : connect())
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

#Make a frame on the left for the client's name and opponents 
top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_your_name = tk.Label(top_left_frame, text="Name: " + your_name, font = "Helvetica 13 bold")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name)
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))

#Make a frame on the right for the timer 
top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Round (x) Starts In", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="red")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

#Middle frame consisting "GAME LOG" text 
middle_frame = tk.Frame(window_main)
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** GAME INFO ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

#Make a frame consisting of the game information 
round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(round_frame, text="You: " + "None", font = "Helvetica 13 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

#Make a final frame to separate the game information and rock, paper, and scissors buttons
final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

#Display the buttons
button_frame = tk.Frame(window_main)
photo_rock = PhotoImage(file=r"images/rock.gif")
photo_paper = PhotoImage(file = r"images/paper.gif")
photo_scissors = PhotoImage(file = r"images/scissors.gif")

#Make a frame for the buttons 
btn_rock = tk.Button(button_frame, text="Rock", command=lambda : choice("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(button_frame, text="Paper", command=lambda : choice("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(button_frame, text="Scissors", command=lambda : choice("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)

#Rock, paper, scissors logic
def game_logic(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    player0 = "you"
    player1 = "opponent"

    if you == opponent:
        winner = "draw"
    elif you == rock:
        if opponent == paper:
            winner = player1
        else:
            winner = player0
    elif you == scissors:
        if opponent == rock:
            winner = player1
        else:
            winner = player0
    elif you == paper:
        if opponent == scissors:
            winner = player1
        else:
            winner = player0
    return winner

#Make buttons
def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)

#Connect client's name
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "Name: " + your_name
        connect_to_server(your_name)

#Make count down function for the timer
def count_down(my_timer, nothing):
    global game_round
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1

    lbl_game_round["text"] = "Round " + str(game_round) + " Starts In"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("Timer: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(game_round)
    lbl_final_result["text"] = ""

#Make choice function to let the client's know which move they pick
def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "You: " + your_choice

    if client:
        str_data = "Game_Round"+str(game_round)+your_choice
        client.send(str_data.encode())
        enable_disable_buttons("disable")

#Connect to the server
def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) 

         #Disable widgets
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("disable")

        threading._start_new_thread(receive_message_from_server, (client, "m"))

    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

#Receive message from the server
def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score

    while True:
        from_server = sck.recv(4096).decode()

        if not from_server: 
            break

        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                lbl_welcome["text"] = ("Welcome " + your_name + "! Waiting for other player")
            elif from_server == "welcome2":
                lbl_welcome["text"] = ("Welcome " + your_name + "! Game will start soon")
            lbl_line_server.pack()

        elif from_server.startswith("opponent_name$"):
            opponent_name = from_server.replace("opponent_name$", "")
            lbl_opponent_name["text"] = "Opponent: " + opponent_name
            top_frame.pack()
            middle_frame.pack()

            #We know two users are connected so game is ready to start
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$opponent_choice"):
            #Get the opponent choice from the server
            opponent_choice = from_server.replace("$opponent_choice", "")

            #Figure out who wins in this round
            who_wins = game_logic(your_choice, opponent_choice)
            round_result = " "
            if who_wins == "you":
                your_score = your_score + 1
                round_result = "WIN"
                color = "green"
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "LOSS"
                color = "red"
            else:
                round_result = "DRAW"
                color = "brown"

            #Update GUI
            lbl_opponent_choice["text"] = "Opponent: " + opponent_choice
            lbl_result["text"] = "Result: " + round_result
            lbl_result.config(foreground=color)

            #Is this the last round e.g. Round 5?
            if game_round == TOTAL_NO_OF_ROUNDS:
                #Compute final result
                final_result = ""
                color = ""

                if your_score > opponent_score:
                    final_result = "(You Won!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "brown"

                lbl_final_result["text"] = "FINAL RESULT: " + str(your_score) + " - " + str(opponent_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0
                your_score = 0
                opponent_score = 0

            #Start the timer
            threading._start_new_thread(count_down, (game_timer, ""))

    sck.close()

window_main.mainloop()