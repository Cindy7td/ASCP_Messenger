from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button
from tkinter import messagebox
import threading
import random
import socket
import pyDes

q = 2426697107
a = 17123207
x = random.randint(1, q-1)
y = str(pow(a,x,q))

dh = "q=2426697107,a=17123207,y=" + y
dh2 = "q=2426697107,a=17123207,y=1724324231"

ASCP = bytes('ASCP',"ascii")
state = bytes('0000',"ascii")
id_session = bytes('0000',"ascii")
version = bytes('00001',"ascii")

function = 1
fn1 = function.to_bytes(2,'big')

class GUI:
    client_socket = None
    authentication = False
    difi = True
    Keyshared = 0

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
        remote_ip = '172.16.112.127' 
        remote_port = 2020
        self.client_socket.connect((remote_ip, remote_port)) 

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def diffiehellman(self, alpha, x, q):
        #Es y a la x mod q
        if x == 0: 
            return 1
        else:
            if x % 2 == 0: 
                multi = (alpha * alpha)
                mod = multi % q
                div = x / 2
                return self.diffiehellman(mod, div, q)
            else:
                return alpha * self.diffiehellman(alpha, x - 1, q) % q

    def encrypt(self,text):
        cNum = bytes(text,"ascii")
        return cNum

    # Aqui se desencripta 
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(2048)
            print(buffer)
            if not buffer:
                break
            
            if buffer[11] == 3 or buffer[11] == 2:
                if buffer[11] == 2:
                    self.authentication = True

                self.difi = False
                mensaje = ""
                end = buffer[9] 
                print(end)
                x1 = 0
                y1 = 19
                while x1 < int(end):
                    x1+=1
                    y1+=1
                    letra = chr(buffer[y1])
                    mensaje += letra
                mensaje = mensaje.split("=")
                y = mensaje[3] 
                print("Esta es y: ")
                print(y)
                print("Esta es x: ")
                print(x)
                print("Esta es q: ")
                print(q)
                llave = self.diffiehellman(int(y),x,q)
                print("Esta es la llave: ")
                print(llave)
                self.Keyshared = llave
              
            else:
                key1 = self.Keyshared
                ks = key1.to_bytes(8,'big')
                k = pyDes.des(ks, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
                msg = k.decrypt(buffer)
            
                decrypted = ""
                end = msg[9]
                
                x1 = 0
                y1 = 19
                while x1 < end:
                    x1+=1
                    y1+=1
                    letra = chr(msg[y1])
                    decrypted += letra

                self.chat_transcript_area.insert('end', "Tu:" + '\n')
                self.chat_transcript_area.insert('end', decrypted + '\n')
                self.chat_transcript_area.yview(END)
        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Key:', font=("Helvetica", 16)).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
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

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()
        
    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        encripted = self.encrypt(data)
        tam =  len(encripted) 

        if tam < 236:
            if self.authentication == True:
                print("Estas en autenticacion, esto es cuando somos las que nos conectamos")
                
                funcion = 3
                fn = funcion.to_bytes(2,'big')
                publicYEnc = self.encrypt(dh2)
                tam =  len(publicYEnc) 
                lista =  tam.to_bytes(1,'big')

                message = bytearray()
                message += ASCP
                message += version
                message += lista
                message += fn 
                message += state 
                message += id_session 
                message += publicYEnc
                
                while len(message) < 256:
                    message += bytes('0', "ascii")
               
                self.authentication = False
                self.difi = False
                self.client_socket.send(message)

            if self.difi == True:
                print("Tu inicias comunicacion")
                funcion = 2
                fn = funcion.to_bytes(2,'big')
                publicYEnc = self.encrypt(dh)
                tam =  len(publicYEnc) 
                lista =  tam.to_bytes(1,'big')
                

                message = bytearray()
                message += ASCP
                message += version
                message += lista
                message += fn 
                message += state 
                message += id_session 
                message += publicYEnc
                
                while len(message) < 256:
                    message += bytes('0', "ascii")

                print("Mensaje:")
                print(message)
                self.authentication = False
                self.difi = False
                self.client_socket.send(message)

            else:
                lista =  tam.to_bytes(1,'big')
                #fn = function.to_bytes(2,'big')
                message = bytearray()
                message += ASCP
                message += version
                message += lista
                message += fn1
                message += state 
                message += id_session 
                message += encripted
                
                while len(message) < 256:
                    message += bytes('0', "ascii")

                key1 = self.Keyshared
                ks = key1.to_bytes(8,'big')
                k = pyDes.des(ks, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad = None, padmode = pyDes.PAD_PKCS5)
                d = k.encrypt(message)
                self.client_socket.send(d)

            self.chat_transcript_area.insert('end', "Yo:" + '\n')
            self.chat_transcript_area.insert('end', data + '\n')
            self.chat_transcript_area.yview(END) 
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
