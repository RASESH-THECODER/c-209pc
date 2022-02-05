import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib 
import os
from ftplib import FTP
import ntpath
import time
from tkinter import filedialog


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None

def getfilesize(file_name):
    with open(file_name,"rb")as file:
        chunk=file.read()
        return len(chunk)

def sendMessage():
    global SERVER
    global textarea
    global text_message
    msgtosend=text_message.get()
    SERVER.send(msgtosend.encode('ascii'))
    textarea.insert(END,"\n"+"You>"+msgtosend)
    textarea.see("end")
    text_message.delete(0,"end")
def connectWithClient():
    global SERVER
    global listbox
    text=listbox.get(ANCHOR)
    list_item=text.split(":")
    msg="connect "+list_item[1]
    SERVER.send(msg.encode('ascii'))

def disconnectWithClient():
    global SERVER
    global listbox
    text=listbox.get(ANCHOR)
    list_item=text.split(":")
    msg="disconnect "+list_item[1]
    SERVER.send(msg.encode('ascii'))  

# Boilerplate Code
def receiveMessage():
    global SERVER
    global BUFFER_SIZE

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass

def browsefiles():
    global textarea
    global filePathLabel
    try:
        filename=filedialog.askopenfilename()
        filePathLabel.configure(text=filename)
        HOSTNAME="127.0.0.1"
        USERNAME="lftpd"
        PASSWORD="lftpd"

        ftp_server=FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding='utf-8'
        ftp_server.cwd("shared files")
        fname=ntpath.basename(filename)
        with open(filename,"rb")as file:
            ftp_server.storbinary(f"STOR{fname}",file)
        ftp_server.dir()
        ftp_server.quit()
    except FileNotFoundError:
        print("cancelButtonPressed")



# Teacher Activity
def showClientsList():
    global listbox
    listbox.delete(0,"end")
    SERVER.send("show list".encode('ascii'))


# Prevoius class code
# Here we ended the last class
def connectToServer():
    global SERVER
    global name
    global sending_file

    cname = name.get()
    SERVER.send(cname.encode())


def openChatWindow():

    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    selectlabel = Label(window, text= "Select Song", font = ("Calibri",10))
    selectlabel.place(x=10, y=8)

    name = Entry(window,width =30,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

PlayButton=Button(openChatWindow,text="Play",width=10,bd=1,bg='skyBlue',font=("Calibri",10))
    PlayButton.place(x=30,y=200)

    Stop=Button(openChatWindow,text="Play",width=10,bd=1,bg='SkyBlue',font=("Calibri",10))
    Stop.place(x=200,y=200)

    connectserver = Button(openChatWindow,text="Connect to Chat Server",bd=1, font = ("Calibri",10), command = connectToServer)
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(openChatWindow, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(openChatWindow, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(openChatWindow,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    # Student Activity 1
    connectButton=Button(openChatWindow,text="Connect",bd=1,bg="cyan",font = ("Calibri",10),command=connectWithClient)
    connectButton.place(x=282,y=160)

    # Bolierplate Code
    disconnectButton=Button(openChatWindow,text="Disconnect",bd=1,bg="red", font = ("Calibri",10),command=disconnectWithClient)
    disconnectButton.place(x=350,y=160)

    # Teacher Activity
    refresh=Button(openChatWindow,text="Refresh",bd=1,bg="green", font = ("Calibri",10), command = showClientsList)
    refresh.place(x=435,y=160)

    labelchat = Label(openChatWindow, text= "Chat Window",bg="light yellow", font = ("Calibri",10))
    labelchat.place(x=10, y=180)

    textarea = Text(openChatWindow, width = 67,height = 6,bg="purple",font = ("Calibri",10))
    textarea.place(x=10,y=200)

    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = listbox.yview)

    attach=Button(openChatWindow,text="Attach & Send",bg="violet",bd=1, font = ("Calibri",10),command=browsefiles)
    attach.place(x=10,y=305)

    text_message = Entry(openChatWindow, width =43,bg="yellow", font = ("Calibri",12))
    text_message.pack()
    text_message.place(x=98,y=306)

    send=Button(openChatWindow,text="Send",bd=1,bg="light green", font = ("Calibri",10),command=sendMessage)
    send.place(x=450,y=305)

    filePathLabel = Label(openChatWindow, text= "",fg= "light yellow", font = ("Calibri",8))
    filePathLabel.place(x=10, y=330)

    openChatWindow.mainloop()


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    # Boilerlate Code
    receive_thread = Thread(target=receiveMessage)               #receiving multiple messages
    receive_thread.start()

    openChatWindow()

setup()