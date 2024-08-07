import hashlib
import socket
import sqlite3
import threading
from datetime import datetime
import time

SERVER_IP = "192.168.1.42"
SERVER_PORT = 3333

global timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect("server/userdata.db", check_same_thread=False)
cur = conn.cursor()

onlineUsers = {}

def send(client_socket, message):
    client_socket.send(message.encode("utf-8"))

def log(log, client_address_for_log):
    with open("server/log.txt", "a") as log_file:
        log_file.write(f"{client_address_for_log} - {log}\n")
    print(log)

def onlineUsersSender():
    for username, client_socket in onlineUsers.items():
        send(client_socket, f"Online Users: {', '.join(onlineUsers.keys())}")
    print(f"Online Users: {', '.join(onlineUsers.keys())}")

def broadcast(broadcast_message,client_address):
    for username, client_socket in onlineUsers.items():
        send(client_socket, broadcast_message)
    log(broadcast_message, client_address)

def handle_client(client_socket, client_address, username):

    send(client_socket, f"Welcome to chat room, {username}!\n")
    time.sleep(0.3)

    onlineUsers[username] = client_socket

    onlineUsersSender()
    time.sleep(0.3)
    
    broadcast(f"[{timestamp}] {username} has joined the room.", client_address)
 
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            formatted_message = f"[{timestamp}] {username} --> {message}"
            
            if message == ".exit":

                client_socket.close()
                del onlineUsers[username]
                
                broadcast(f"[{timestamp}] {username} left the room.", client_address)
                time.sleep(0.3) 
                onlineUsersSender() 

                threading.Thread(target=handle_client, args=(client_socket, username,)).join()
                
            if message.startswith("@"):
                target_user = message.split(" ")[0][1:]
                private_message = " ".join(message.split(" ")[1:])

                if target_user in onlineUsers:  
                    send(onlineUsers[target_user], f"[{timestamp}] Private message ({username} has sent message to you): {message}")
                
                else:
                    send(client_socket, f"[{timestamp}] {target_user} is not online now.")
                    
                log(f"[{timestamp}] Private message ({username} -> {target_user}): {private_message}", client_address)

            if not message:
                break

            else:
                broadcast(formatted_message, client_address)

        except:
            break
    client_socket.close()

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    log(f"[{timestamp}] Server has started",f"<('{SERVER_IP}', {SERVER_PORT})>")    
    print(f"Server is on.\nListening {SERVER_IP}:{SERVER_PORT} ...")

    def handle_input():

        while True:

            admin_input= input("Server:")

            if admin_input.startswith(".run"):

                try:
                    code = admin_input.split(" ", 2)
                    run_arg = code[0]
                    target = code[1]
                    executed = code[2]
                    sended = f"{run_arg} {executed}"
                    target_user = target

                except Exception:
                    print("Invalid input")

                try:
                    send(onlineUsers[target_user], sended)

                except KeyError:
                    print(f"User not found: {target_user}")

            elif admin_input.startswith(".kick"):
    
                try:
                    code = admin_input.split(" ", 1)
                    username_K = code[1]

                    cur.execute("UPDATE userdata SET status = 1 WHERE username = ?", (username_K))
                    conn.commit()
                    
                    broadcast(f"[{timestamp}] {username_K} has been kicked.", client_address)
                    
                    if username_K in onlineUsers:
                        send(onlineUsers[username_K],".kick")
                        time.sleep(2)
                        client_socket.close()

                        del onlineUsers[username_K]
                        onlineUsersSender() 

                    else:
                        print(f"User not found: {username_K}")

                except Exception as e:
                    print(e)

            elif admin_input.startswith(".unkick"):

                try:
                    code = admin_input.split(" ", 1)
                    username_U = code[1]

                    if username_U in onlineUsers:
                        cur.execute("UPDATE userdata SET status = 0 WHERE username = ?", (username_U))
                        conn.commit()  

                        broadcast(f"[{timestamp}] {username_U} has been granted access.", client_address)

                    else:
                        print(f"User not found: {username_U}")

                except Exception as e:
                    print(e)

            elif admin_input.startswith(".mute"):

                try:
                    code = admin_input.split(" ", 1)
                    username_M = code[1]

                    if username_M in result[0]:
                        cur.execute("UPDATE userdata SET status = 2 WHERE username = ?", (username_M))
                        conn.commit()
                        
                        broadcast(f"[{timestamp}] {username_M} has been muted.", client_address)

                    if username_M in onlineUsers:
                        send(onlineUsers[username_M], ".mute")
                    
                    else:
                        print(f"User not found: {username_M}")

                except Exception as e:
                    print(e)

            elif admin_input.startswith(".unmute"):

                try:
                    code = admin_input.split(" ", 1)
                    username_UM = code[1]

                    if username_UM in result[0]:
                        cur.execute("UPDATE userdata SET status = 0 WHERE username = ?", (username_UM))
                        conn.commit()

                        broadcast(f"[{timestamp}] {username_UM} has been unmuted.", client_address)

                    if username_UM in onlineUsers:
                        send(onlineUsers[username_UM], ".unmute")

                    else:
                        print(f"User not found: {username_UM}")

                except Exception as e:
                    print(e)

            elif admin_input.startswith(".not"):

                try:
                    code = admin_input.split(" ", 2)
                    run_arg = code[0]
                    username_N = code[1]

                    if username_N in onlineUsers:
                        send(onlineUsers[username_N], admin_input)

                    else:
                        print(f"[{timestamp}] {username_N} is offline. Attempt to send notification failed")

                except KeyError:
                    print(f"User not found: {username_N}")
            
            elif admin_input.startswith(".ann"):
 
                try:
                    broadcast(admin_input, client_address)

                except Exception as e:
                    print(e)

            elif admin_input.startswith(".exit"):
                code = admin_input.split(" ", 1)
                username_E = code[1]
                if username_E in onlineUsers:

                    client_socket.close()
                    del onlineUsers[username_E]
                    
                    broadcast(f"[{timestamp}] {username_E} has been disconnected by server.", client_address)
                    time.sleep(0.3) 
                    onlineUsersSender() 

                    threading.Thread(target=handle_client, args=(client_socket, username_E,)).join

            else:
                broadcast(f"{timestamp} Server: " + admin_input, client_address)

    threading.Thread(target=handle_input,).start()

    while True:

        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")

        loginorregister = client_socket.recv(1024).decode("utf-8")

        if loginorregister == "login":

            username = client_socket.recv(1024).decode("utf-8")
            password = client_socket.recv(1024)
            password = hashlib.sha256(password).hexdigest()
        
            cur.execute("SELECT username, password, status FROM userdata WHERE username = ? AND password = ?", (username, password))
            result = cur.fetchone()
            
            status = result[2]
            
            if not result:
                send(client_socket, "Failed not authorize")
                client_socket.close()
            
            if username in onlineUsers:
                send(client_socket, "You have already logged in")

            if status == 1:
                send(client_socket, "You have been kicked")
                client_socket.close()

            elif status == 0 or 2:
                send(client_socket, "success")
                threading.Thread(target=handle_client, args=(client_socket, client_address, username)).start()
                onlineUsers[username] = client_socket

            else:
                send(client_socket, "Failed: Unvalid status")
                client_socket.close()
                
        elif loginorregister == "register":

            username = client_socket.recv(1024).decode("utf-8")
            password = client_socket.recv(1024)
            password = hashlib.sha256(password).hexdigest()

            cur.execute("SELECT username FROM userdata WHERE username = ?", (username,))

            result = cur.fetchone()

            if not result:
                cur.execute("INSERT INTO userdata (username, password, status) VALUES (?, ?, ?)",(username, password, 0))
                conn.commit()

                send(client_socket, "success")

                threading.Thread(target=handle_client, args=(client_socket, username)).start()

                onlineUsers[username] = client_socket                

            else:
                send(client_socket, "Username has already been taken")
                client_socket.close()
                onlineUsers[username] = client_socket

        else:
            send(client_socket, "Failed: Wrong label")
            client_socket.close()

if __name__ == "__main__":
    main()