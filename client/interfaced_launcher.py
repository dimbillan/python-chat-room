import threading
from utilities import *
from tkinter import Listbox, Tk, Canvas, Entry, Button
from datetime import datetime

def main():
    window = Tk()

    window.geometry("750x475")
    window.configure(bg = "#151515")
    window.title("Login Window")

    canvas = Canvas(
        window,
        bg = "#151515",
        height = 475,
        width = 750,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    login_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 15,),
        text="Giriş Yap",
        command=lambda: login(server_ip_entry.get(), username_entry.get(), password_entry.get(),chat_window_func,window),
        relief="flat"
    )
    login_button.place(
        x=25.0,
        y=400.0,
        width=313.0,
        height=50.0
    )

    register_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 15,),
        text="Kayıt Ol",
        command=lambda: register_user(server_ip_entry.get(), username_entry.get(), password_entry.get(),chat_window_func,window),
        relief="flat"
    )
    register_button.place(
        x=412.0,
        y=400.0,
        width=313.0,
        height=50.0
    )

    server_ip_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 15,),
    )
    server_ip_entry.place(
        x=25.0,
        y=75.0,
        width=700.0,
        height=50.0
    )

    username_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 15,),
    )
    username_entry.place(
        x=25.0,
        y=200.0,
        width=700.0,
        height=50.0
    )

    password_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 15,),
        show="*",
    )
    password_entry.place(
        x=25.0,
        y=325.0,
        width=700.0,
        height=50.0
    )

    canvas.create_text(
        30.0,
        25.0,
        anchor="nw",
        text="Server IP:",
        fill="#D9D9D9",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        30.0,
        150.0,
        anchor="nw",
        text="Kullanıcı Adı:",
        fill="#D9D9D9",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        30.0,
        275.0,
        anchor="nw",
        text="Şifre:",
        fill="#D9D9D9",
        font=("Inter", 15 * -1)
    )

    def update():
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d.%m.%Y")
        canvas.delete("time")
        canvas.delete("date")
        canvas.create_text(720, 25.0, anchor="ne", text= time, fill="#D9D9D9", font=("Inter", 15 * -1), tags = "time")
        canvas.create_text(720, 45.0, anchor="ne", text= date, fill="#D9D9D9", font=("Inter", 15 * -1), tags = "date") 
        window.after(1000, update)

    update()

    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.resizable(False, False)
    window.mainloop()

def chat_window_func():
    chat_window = Tk()

    chat_window.geometry("750x475")
    chat_window.configure(bg = "#151515")
    chat_window.title("Chat Room")

    canvas = Canvas(
        chat_window,
        bg = "#151515",
        height = 475,
        width = 750,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    chat_box_entry = tk.Text(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 13 * -1),
    )
    chat_box_entry.place(
        x=25.0,
        y=75.0,
        width=500.0,
        height=300.0
    )

    online_users_entry = Listbox(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 13 * -1),
    )
    online_users_entry.place(
        x=550.0,
        y=75.0,
        width=175.0,
        height=223.0
    )

    message_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        font=("", 13,),
    )
    message_entry.place(
        x=25.0,
        y=400.0,
        width=500.0,
        height=48.0
    )

    toggle_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        text="Koyu/Açık\nTema",
        font=("",12 * -1),
        command=lambda: print("tema toggle clicked"),
        relief="flat"
    )
    toggle_button.place(
        x=550.0,
        y=325.0,
        width=75.0,
        height=50.0
    )

    exit_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        text="Çıkış",
        font=("",15 * -1),
        command=lambda: on_closing(chat_window, receive_thread),
        relief="flat"
    )
    exit_button.place(
        x=650.0,
        y=325.0,
        width=75.0,
        height=50.0
    )

    clear_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        text="Temizle",
        font=("",15 * -1),
        command=lambda: chat_box_entry.delete(0, tk.END),
        relief="flat"
    )
    clear_button.place(
        x=650.0,
        y=400.0,
        width=75.0,
        height=50.0
    )

    send_button = Button(
        borderwidth=0,
        bg="#D9D9D9",
        fg="#000716",
        text="Gönder",
        font=("",15 * -1),
        command=lambda: send_message(message_entry),
        relief="flat"
    )
    send_button.place(
        x=550.0,
        y=400.0,
        width=75.0,
        height=50.0
    )

    canvas.create_text(
        30.0,
        25.0,
        anchor="nw",
        text="Sohbet",
        fill="#D9D9D9",
        font=("Inter", 15 * -1)
    )

    online_users_text = canvas.create_text(
        550.0,
        25.0,
        anchor="nw",
        text="Çevrimiçi Kullanıcılar",
        fill="#D9D9D9",
        font=("Inter", 15 * -1)
    )

    def update():
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d.%m.%Y")
        canvas.delete("time")
        canvas.delete("date")
        canvas.create_text(525, 25.0, anchor="ne", text= time, fill="#D9D9D9", font=("Inter", 15 * -1), tags = "time")
        canvas.create_text(525, 45.0, anchor="ne", text= date, fill="#D9D9D9", font=("Inter", 15 * -1), tags = "date") 
        chat_window.after(1000, update)

    update()
    
    chat_window.bind("<Return>", lambda event: on_enter(event, message_entry,send_button))

    receive_thread = threading.Thread(target=receive_messages, args=(chat_box_entry,online_users_entry,canvas,online_users_text,chat_window,send_button,))
    receive_thread.start()
  
    chat_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(chat_window, receive_thread))
    chat_window.resizable(False, False)
    chat_window.mainloop()

if __name__ == "__main__":
   main()