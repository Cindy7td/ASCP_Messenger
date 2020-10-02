from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button
import socket
import threading
#import pip install pydes
import pyDes
from tkinter import messagebox

ASCP = [65,83,67,80]
version = [48,48,48,48,49]
function = [48,48]
state = [48,48,48,48]
id_session = [48,48,48,48] 
key = ""

class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '13.57.9.228' 
        remote_port = 3023 
        self.client_socket.connect((remote_ip, remote_port)) 

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def encrypt(self,text):
        encrypted = []
        for character in text:
            cNum = ord(character)
            encrypted.append(cNum)
        return encrypted

    # Aqui se desencripta 
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(1024)
            if not buffer:
                break
            #k = pyDes.des(key, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            #buffer = k.decrypt(buffer)
            decrypted = ""
            end = buffer[9]
            print(end)
            x = 0
            y = 19
            while x < end:
                x+=1
                y+=1
                letra = chr(buffer[y])
                decrypted += letra
            
            self.chat_transcript_area.insert('end', decrypted + '\n')
            self.chat_transcript_area.yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Key:', font=("Helvetica", 16)).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, command=self.on_join).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')


    # Este creo que no importa
    def on_join(self):
        self.name_widget.config(state='disabled')
        newJoined =  self.encrypt(" " + self.name_widget.get())
        key = newJoined
        #print(newJoined)
        #tam =  len(newJoined)
        #lista =  self.encrypt(str(tam))
        #message = bytearray(ASCP+version+lista+function+state+id_session+newJoined)
        #print(message)
        #self.client_socket.send(message)

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your key", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    ##AQUI SE ENCRIPTA y manda
    def send_chat(self):
        #senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        encripted = self.encrypt(data)
        print(encripted)
        tam =  len(encripted)
        if tam < 236:
            lista =  self.encrypt(str(tam))
            message = bytearray(ASCP+version+lista+function+state+id_session+encripted)
            #k = pyDes.des(key, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad = None, padmode = pyDes.PAD_PKCS5)
            #d = k.encrypt(message)
            self.chat_transcript_area.insert('end', data + '\n')
            self.chat_transcript_area.yview(END)
            self.client_socket.send(message)
            self.enter_text_widget.delete(1.0, 'end')

        else:
            error = "Mensaje muy largo"
            self.chat_transcript_area.insert('end', error + '\n')
            self.enter_text_widget.delete(1.0, 'end')
            
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
