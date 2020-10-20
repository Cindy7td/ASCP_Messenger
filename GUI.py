from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button
import socket
import threading
#import pip install pydes
import pyDes
from tkinter import messagebox

q=353
x= 233
alpha= 3

ASCP = [65,83,67,80]
version = [48,48,48,48,49]
function = [48,49]
state = [48,48,48,48]
id_session = [48,48,48,48] 

class GUI:
    client_socket = None
    authentication = False
    difi = True
    Keyshared= 0

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
        #self.display_name_section()
        self.display_chat_entry_box()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def diffiehellman(self,alpha, x, q):
        #Es alpha a la x mod q
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
        encrypted = []
        for character in text:
            cNum = ord(character)
            encrypted.append(cNum)
        return encrypted

    # Aqui se desencripta 
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(2048)
            #key = self.name_widget.get()
            if not buffer:
                break
            
            if buffer[11] == 50 or buffer[11] == 51:
                self.authentication = True
                self.difi = False
                mensaje = ""
                end = buffer[9] 
                endtonumber = chr(end)
               
                x = 0
                y = 19
                while x < int(endtonumber):
                    x+=1
                    y+=1
                    letra = chr(buffer[y])
                    mensaje += letra
               

                publicYA = int(mensaje)
                print("esto recibi:")
                print(publicYA)
                llave = self.diffiehellman(publicYA,x,q)
                print("soy la llave privada:")
                print(llave)
                self.Keyshared = llave
              
            else:
                key1 = self.Keyshared
                ks = key1.to_bytes(8,'big')
                k = pyDes.des(ks, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
                msg = k.decrypt(buffer)
            
                decrypted = ""
                end = msg[9]
                
                x = 0
                y = 19
                while x < end:
                    x+=1
                    y+=1
                    letra = chr(msg[y])
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
        #self.join_button = Button(frame, text="Join", width=10, command=self.on_join).pack(side='left')
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

    #llave
    # def on_join(self):
    #    self.name_widget.config(state='disabled')
    #    newJoined =  self.encrypt(" " + self.name_widget.get())
    #    end = len(newJoined)
    #    x=0
    #    ktostring = ""
        
    #    while x < end-1:
    #        x+=1
    #        letra = chr(newJoined[x])
    #        ktostring += letra
       
    #    ktobytes = bytes.fromhex(ktostring)
        
    #    key = ktobytes
    #    print(key)


    def on_enter_key_pressed(self, event):
        #if len(self.name_widget.get()) == 0:
            #messagebox.showerror(
           #     "Enter your key", "Enter your name to send a message")
            #return
        self.send_chat()
        self.clear_text()
        

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    ##AQUI SE ENCRIPTA y manda
    def send_chat(self):
        #key = self.name_widget.get()
        data = self.enter_text_widget.get(1.0, 'end').strip()
        encripted = self.encrypt(data)
        tam =  len(encripted) 

        while len(encripted) < 236:
            encripted.append(0)

        if tam < 236:
            
            if self.authentication == True:
                print("esras en autenticacion, est es cuando somos las qe nos conectamos")
                funcion = [48,3]
                publicY = self.diffiehellman(alpha,x,q)
                print("DESPUES DE DF")
                print(publicY)
                publicYEnc = self.encrypt(str(publicY))
                tam =  len(publicYEnc) 
                lista =  self.encrypt(str(tam))
                while len(publicYEnc) < 236:
                    publicYEnc.append(0)
                
                message = bytearray(ASCP+version+lista+funcion+state+id_session+publicYEnc)
                self.authentication = False
                self.difi = False
                print("se mando public y")
                self.client_socket.send(message)

            if self.difi == True:
                print("tu inicias comunicacion")

                funcion = [48,2]
                publicY = self.diffiehellman(alpha,x,q)
                publicYEnc = self.encrypt(str(publicY))
                tam =  len(publicYEnc) 
                lista =  self.encrypt(str(tam))

                while len(publicYEnc) < 236:
                    publicYEnc.append(0)
                
                message = bytearray(ASCP+version+lista+funcion+state+id_session+publicYEnc)

                self.authentication = False
                self.difi = False
                self.client_socket.send(message)

            else:
                
                lista =  self.encrypt(str(tam))
                message = bytearray(ASCP+version+lista+function+state+id_session+encripted)
                print("se supone que ya tenemos la k en ambas partes")
                print(self.Keyshared)
                key1 = self.Keyshared
                print(key1)
                ks = key1.to_bytes(8,'big')
                print("esto es ks")
                print(ks)
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
