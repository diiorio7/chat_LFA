from socket import *
from threading import *
from tkinter import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 7500

clientSocket.connect((hostIp, portNumber))


window = Tk()
window.configure(background='#919191', borderwidth = 3)
window.title("Chat LFA | Conectado com: "+ hostIp+ ":"+str(portNumber))

title_place = Frame(window, background = "#919191")
title_place.place(x = 30, y = 10, width = 150, height = 30)
title = Label(title_place, text = "Chat LFA", font = 'Bahnschrift 20', background = "#919191")
title.pack()

txtMessages = Text(window, width=50, height = 30)
txtMessages.grid(row=0, column=0, padx=10, pady=(50,0))
txtMessages.configure(background='#AEAEAE')

def focus_out_entry_box(widget, widget_text):
    if widget['fg'] == 'Black' and len(widget.get()) == 0:
        widget.delete(0, END)
        widget['fg'] = 'Grey'
        widget.insert(0, widget_text)


def focus_in_entry_box(widget):
    if widget['fg'] == 'Grey':
        widget['fg'] = 'Black'
        widget.delete(0, END)

def on_enter(e):
    btnSendMessage['background'] = '#A2FFC5'

def on_leave(e):
    btnSendMessage['background'] = '#AEAEAE'

def sendMessage():
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, "\n" + "Você: "+ clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))
    txtYourMessage.delete(0, END)

def sendMessageEnter(e):
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, "\n" + "Você: "+ clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))
    txtYourMessage.delete(0, END)

    
entry_text = 'Digite sua mensagem'
txtYourMessage = Entry(window, width =50, font='Bahnschrift', fg='Grey')
txtYourMessage.insert(0, entry_text)
txtYourMessage.bind("<FocusIn>", lambda args: focus_in_entry_box(txtYourMessage))
txtYourMessage.bind("<FocusOut>", lambda args: focus_out_entry_box(txtYourMessage, entry_text))
txtYourMessage.bind("<Return>", sendMessageEnter)
txtYourMessage.pack()
txtYourMessage.grid(row=9, column=0, padx=10, pady=10)
txtYourMessage.configure(background='#AEAEAE')




btnSendMessage = Button(window, text="Enviar", width=50, height = 2, command=sendMessage, font = 'Bahnschrift', bg = '#AEAEAE')
btnSendMessage.grid(row=10, column=0, padx=10, pady=10)
btnSendMessage.bind("<Enter>", on_enter)
btnSendMessage.bind("<Leave>", on_leave)


def recvMessage():
    while True:
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        print(serverMessage)
        txtMessages.insert(END, "\n"+serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

window.mainloop()





