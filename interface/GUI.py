from tkinter import *
import threading 

class GUI:

    def __init__(self): 
        
        # chat window which is currently hidden 
        self.Window = Tk() 
        self.Window.withdraw() 
        self.SEND = False
        ##self.Window.bind('<Enter>', self.enter)
        self.layout("JuJu Bot")



    # The main layout of the chat 
    def layout(self,name): 
        
        self.name = name 
        # to show chat window 
        self.Window.deiconify() 
        self.Window.title("CHATROOM") 
        self.Window.resizable(width = False, 
                              height = False) 
        self.Window.configure(width = 380, 
                              height = 600, 
                              bg = "#FFCC00") 
        self.labelHead = Label(self.Window, 
                             bg = "#FFCC00",  
                              fg = "#FFFFFF", 
                              text = self.name , 
                               font = "Helvetica 13 bold", 
                               pady = 5) 
          
        self.labelHead.place(relwidth = 1) 
        self.line = Label(self.Window, 
                          width = 450, 
                          bg = "#FFCC00") 
          
        self.line.place(relwidth = 1, 
                        rely = 0.07, 
                        relheight = 0.012) 
          
        self.textCons = Text(self.Window, 
                             width = 20,  
                             height = 2, 
                             bg = "#90a4ae", 
                             fg = "#000000", 
                             font = "Helvetica 14",  
                             padx = 5, 
                             pady = 5) 
          
        self.textCons.place(relheight = 0.745, 
                            relwidth = 1,  
                            rely = 0.08) 
          
        self.labelBottom = Label(self.Window, 
                                 bg = "#FFCC00", 
                                 height = 80) 
          
        self.labelBottom.place(relwidth = 1, 
                               rely = 0.825) 
          
        self.entryMsg = Entry(self.labelBottom, 
                              bg = "#90a4ae", 
                              fg = "#000000", 
                              font = "Helvetica 13") 
          
        self.entryMsg.place(relwidth = 0.74, 
                            relheight = 0.06, 
                            rely = 0.008, 
                            relx = 0.011) 
          
        self.entryMsg.focus()           

        self.buttonMsg = Button(self.labelBottom, 
                                text = "Enviar", 
                                font = "Helvetica 10 bold",  
                                width = 12, 
                                bg = "#90a4ae", 
                                command = lambda : self.sendButton("Usuário: " + self.entryMsg.get())) 
          
        self.buttonMsg.place(relx = 0.77, 
                             rely = 0.008, 
                             relheight = 0.06,  
                             relwidth = 0.22) 
          
        self.textCons.config(cursor = "arrow") 
          
        scrollbar = Scrollbar(self.textCons) 
          
        scrollbar.place(relheight = 1, 
                        relx = 0.974) 
          
        scrollbar.config(command = self.textCons.yview) 
          
        self.textCons.config(state = DISABLED) 
  
    def sendButton(self, msg): 
        if(msg == 'Usuário: '):
            return
        if('Usuário: ' in msg):
            self.SEND = True
        self.textCons.config(state = DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, END) 
        self.textCons.config(state = NORMAL)
        self.SEND = False
        
        # self.canvas = Canvas(width=800, height=650, bg = '#afeeee')
        # self.canvas.pack()
        # self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold", 
        #                 text="Click the bubbles that are multiples of two.")
        self.textCons.insert(END, msg+"\n\n") 
        self.textCons.config(state = DISABLED) 
        self.textCons.see(END) 
    
    def enter(self, event=None):
        self.sendButton(self.entryMsg.get())
        
