import sys
import ast
import random
import codecs
import urllib.parse
import webbrowser
from interface.GUI import GUI
import threading
import time

from expert_system import Prompt, Tree, Print
from expert_system.parser.Parser import ESParser
from expert_system.config.Env import Env
from expert_system.config.Cmd import Cmd
from expert_system.util.Color import Color
import tkinter as tk

dictionary = {}
B_answer = {}
N_answer = {}
#gui = GUI()

def resolve_lines(parser):
    tree = Tree.NPITree(parser.structured_rules, parser.facts, parser.queries)
    results = {}
    for query in parser.queries:
        results[query] = tree.resolve_query(query)
        color = Color.GREEN if results[query] is True else Color.FAIL
        print(f"{ query } resolved as { color }{ results[query] }{ Color.END }")
    return results


def importFromFile(str):
    fileName = str + ".txt"
    file = codecs.open(fileName, encoding='utf-8')
    contents = file.read()
    result = ast.literal_eval(contents)
    file.close()
    return result

def chatbot(parser):
    dictionary = importFromFile('dictionary')
    B_answer = importFromFile('B_answer')
    N_answer = importFromFile('notebooks')

    print("Juju Bot: " + dictionary['WelcomeMsg'])
    
    prompt = Prompt.ESPrompt(lines)
    while(True):
       
        index = random.choice(range(1, 5));
        Banswer = B_answer[str(index)]
        
        answer = input("Juju Bot: " + Banswer + dictionary[parser.atual_fact] + '\n' +
                        "Usuário: ")
        if('sim' in answer.lower()):
            prompt.do_add_fact(parser.atual_fact.lower())
            next = parser.atual_fact + parser.atual_fact.lower() + '+'
        elif('nao' in answer.lower()):
            next = parser.atual_fact + parser.atual_fact.lower() + '!+'
        else:
            print("Juju Bot: Não entendi :(")
            continue
        for w in parser.structured_rules:
            if (next == w.npi_left):
                parser.atual_fact = w.npi_right

        if(ord(parser.atual_fact) in range(76,90)):
            print('>> Acredito que o melhor notebook para voce é o: ' + N_answer[parser.atual_fact] + ' <<')
            finalString = 'https://zoom.com.br/search?sortBy=prod_items_sort_by_price_asc&q='  + urllib.parse.quote(N_answer[parser.atual_fact])
            print('Juju Bot: Para facilitar sua vida, abri o produto em seu navegador, obrigado :D' )
            time.sleep(5)
            webbrowser.open(finalString, new = 2, autoraise=False)
            #DEBUG
            # prompt.do_solve(parser.queries)
            # parserSolve = ESParser(prompt.get_lines())
            # res = resolve_lines(parserSolve)
            break

def chatbotInterface(parser):
    dictionary = importFromFile('dictionary')
    B_answer = importFromFile('B_answer')
    N_answer = importFromFile('notebooks')

    gui.sendButton("Juju Bot: " + dictionary['WelcomeMsg'])

    prompt = Prompt.ESPrompt(lines)
    gui.Window.mainloop()

    while(True):
        index = random.choice(range(1, 5))
        Banswer = B_answer[str(index)]
        gui.sendButton("Juju Bot: " + Banswer + dictionary[parser.atual_fact] + '\n' +
                        "Usuário: ")
        answer = gui.entryMsg.get()
        print(answer)

        if('sim' in answer.lower()):
            prompt.do_add_fact(parser.atual_fact.lower())
            next = parser.atual_fact + parser.atual_fact.lower() + '+'
        elif('nao' in answer.lower()):
            next = parser.atual_fact + parser.atual_fact.lower() + '!+'
        else:
            gui.sendButton("Juju Bot: Não entendi :(")
            continue
        for w in parser.structured_rules:
            if (next == w.npi_left):
                parser.atual_fact = w.npi_right

        if(ord(parser.atual_fact) in range(76,90)):
            gui.sendButton('>> Acredito que o melhor notebook para voce é o: ' + N_answer[parser.atual_fact] + ' <<')
            finalString = 'https://zoom.com.br/search?sortBy=prod_items_sort_by_price_asc&q='  + urllib.parse.quote(N_answer[parser.atual_fact])
            gui.sendButton('Juju Bot: Para facilitar sua vida, abri o produto em seu navegador, obrigado :D' )
            webbrowser.open(finalString, new = 0, autoraise=False)
            #DEBUG
            # prompt.do_solve(parser.queries)
            # parserSolve = ESParser(prompt.get_lines())
            # res = resolve_lines(parserSolve)
            break


def createGUI():
    gui = GUI()

if __name__ == "__main__":
    args = Cmd.args

    try:
        with open(args.input) as f:
            lines = f.readlines()

            #teste interface
            
            if args.mode == "interactive":
                Prompt.ESPrompt(lines).cmdloop()  
            elif args.mode == "interface":
                parser = ESParser(lines)
                gui = GUI()
                snd = threading.Thread(target = chatbotInterface(parser)) 
                snd.start() 
            else: 
                parser = ESParser(lines)
                chatbot(parser)

    except (Exception, BaseException) as e:
        print(e)
        sys.exit(1)


