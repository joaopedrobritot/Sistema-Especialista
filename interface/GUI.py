from tkinter import *
import threading 
import codecs
import ast
import sys
import ast
import random
import codecs
import urllib.parse
import webbrowser
import threading
import time
from expert_system.parser.Parser import ESParser
from expert_system import Prompt, Tree


dictionary = {}
B_answer = {}
N_answer = {}
TRUE_ANSWER = ['certo', 'okay', 'sim', 'prefiro', 'ok']
FALSE_ANSWER = ['não', 'nao', 'Discordo']

class GUI:

   
    def __init__(self): 
        
        # chat window which is currently hidden 
        self.Window = Tk() 
        self.Window.withdraw() 
        self.SEND = False
        self.final = False
        ##self.Window.bind('<Enter>', self.enter)
        self.layout("Amber Bot")

    def layout(self,name): 
        
        self.name = name 
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
                                command = lambda : self.sendMsg()) 
          
        self.buttonMsg.place(relx = 0.77, 
                             rely = 0.008, 
                             relheight = 0.06,  
                             relwidth = 0.22) 
          
        self.textCons.config(cursor = "arrow") 
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
    
     
    def importFromFile(self, str):
        fileName = str + ".txt"
        file = codecs.open(fileName, encoding='utf-8')
        contents = file.read()
        result = ast.literal_eval(contents)
        file.close()
        return result

    def setConfig(self, prompt, parser,line):
        
        dictionary = self.importFromFile('./dictionaries/dictionary')
        B_answer = self.importFromFile('./dictionaries/B_answer')
        N_answer = self.importFromFile('./dictionaries/notebooks')

        self.line = line
        self.prompt = prompt
        self.parser = parser
        self.sendButton("Amber Bot: " + dictionary['WelcomeMsg'])
        self.sendButton("Amber Bot: Vamos começar. " + dictionary[self.parser.atual_fact])

        self.Window.mainloop()


    
    def sendMsg(self):
        if(self.final):
            self.setConfig(ESParser(self.line), Prompt.ESPrompt(self.line), self.line)
            self.final = False

        dictionary = self.importFromFile('./dictionaries/dictionary')
        B_answer = self.importFromFile('./dictionaries/B_answer')
        N_answer = self.importFromFile('./dictionaries/notebooks')

        index = random.choice(range(1, 5))
        Banswer = B_answer[str(index)]
       
        answer = self.entryMsg.get()

        if any(answer.lower() == s for s in TRUE_ANSWER):
            self.prompt.do_add_fact(self.parser.atual_fact.lower())
            next = self.parser.atual_fact + self.parser.atual_fact.lower() + '+'
        elif any(answer.lower() == s for s in FALSE_ANSWER):
            next = self.parser.atual_fact + self.parser.atual_fact.lower() + '!+'
        else:
            self.sendButton("Amber Bot: Não entendi :(")
        for w in self.parser.structured_rules:
            if (next == w.npi_left):
                self.parser.atual_fact = w.npi_right

        self.sendButton("Usuário: "+answer)

     
        if(ord(self.parser.atual_fact) in range(76,90)):
            self.sendButton('Amber Bot: Acredito que o melhor notebook para voce é o: ' + N_answer[self.parser.atual_fact])
            finalString = 'https://zoom.com.br/search?sortBy=prod_items_sort_by_price_asc&q='  + urllib.parse.quote(N_answer[self.parser.atual_fact])
            self.sendButton('Amber Bot: Para facilitar sua vida, abri o produto em seu navegador, obrigado :D\n-------------------------------------------------------------' )
            webbrowser.open(finalString, new = 0, autoraise=False)
            self.final = True
            #DEBUG
            # self.prompt.do_solve(self.parser.queries)
            # self.parserSolve = ESself.parser(self.prompt.get_lines())
            # res = resolve_lines(self.parserSolve)
    
        self.sendButton("Amber Bot: " + Banswer + dictionary[self.parser.atual_fact])