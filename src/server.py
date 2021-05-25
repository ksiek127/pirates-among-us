import socket
from _thread import *
import pickle
import random
from objects.player import Player
from datetime import timedelta

# server = "192.168.1.94"  # Asia
server = "192.168.1.61"  # K
# server = "192.168.1.102" # K2
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)  # wypisanie bledu

s.listen(10)
print("connecting")

display_width = 1200
display_height = 1200

already_set_roles = False

players = [Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=0),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=1),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=2),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=3),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=4),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=5),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=6),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=7),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=8),
           Player(screen_pos=[display_width // 2, display_height // 2], position=[800, 300],
                  role="crewmate", cooldown=-1, kill_distance=-1, id=9)
           ]


def set_roles():
    if connected_players >= 7:
        impostors_number = 2
    else:
        impostors_number = 1

    while impostors_number > 0:
        index = random.randint(0, connected_players-1)
        if players[index].role != "impostor":
            set_impostor(index)
            impostors_number -= 1


def set_impostor(index):
    players[index].role = "impostor"
    players[index].kill_cooldown = timedelta(seconds=2)
    players[index].kill_distance = 100


def threaded_client(conn, player_idx):
    conn.send(pickle.dumps(players[player_idx]))

    global already_set_roles

    while True:  # klient wysyla swoja pozycje na serwer
        try:
            data = pickle.loads(conn.recv(100000))

            if players[player_idx].role == "impostor" and data.role == "crewmate":
                players[player_idx] = data
                set_impostor(player_idx)
            else:
                players[player_idx] = data

            if not data:
                print("disconnected")
                break
            else:

                if data.in_game and not already_set_roles:
                    set_roles()
                    already_set_roles = True

                reply = players

            conn.sendall(pickle.dumps(reply))
        except socket.error as e:
            print(e)

    print("lost connection")
    conn.close()


connected_players = 0


while True:
    conn, address = s.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (conn, connected_players))
    connected_players += 1
