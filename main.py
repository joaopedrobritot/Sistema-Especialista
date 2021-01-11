import sys
import ast
import random
import codecs
import urllib.parse
import webbrowser
from interface.GUI import GUI
import threading
import time
import os

from expert_system import Prompt, Tree
from expert_system.parser.Parser import ESParser
from expert_system.config.Cmd import Cmd
from expert_system.util.Color import Color
import tkinter as tk

dictionary = {}
B_answer = {}
N_answer = {}
BOT_NAME = "juju bot: "
TRUE_ANSWER = ['certo', 'okay', 'sim', 'prefiro', 'ok' , "acho que sim",  "creio que sim"]
FALSE_ANSWER = ['não', 'nao', 'Discordo', "acho que não",  "acho que nao"]
#gui = GUI()

def resolve_lines(parser, prt=False):
    tree = Tree.NPITree(parser.structured_rules, parser.facts, parser.queries)
    results = {}
    for query in parser.queries:
        results[query] = tree.resolve_query(query)
        if(prt):
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

def realType(str, userinput=True):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(random.random()*1/100)
  

def chatbot(parser):
    dictionary = importFromFile('./dictionaries/dictionary')
    B_answer = importFromFile('./dictionaries/B_answer')
    N_answer = importFromFile('./dictionaries/notebooks')

    print(BOT_NAME, end='')
    realType(dictionary['WelcomeMsg'] + '\n\n' + BOT_NAME + 'Para ajudar em sua escolha, vou iniciar fazendo algumas perguntas, certo?\n\n')
    
    while(True):
        answer = input("Usuário: ")
        if any(answer.lower() == s for s in TRUE_ANSWER):
            break
        else:
            print("\n" + BOT_NAME, end='')
            print("não entendi :( vou repetir a pergunta!"+ "\n")
        continue

    prompt = Prompt.ESPrompt(lines)
    while(True):
       
        index = random.choice(range(1, 5))
        Banswer = B_answer[str(index)]
        
        print("\n" + BOT_NAME, end='')
        realType(Banswer + dictionary[parser.atual_fact] + '\n\n')
        answer = input("Usuário: ")

        if any(answer.lower() == s for s in TRUE_ANSWER):
            prompt.do_add_fact(parser.atual_fact.lower())
            next = parser.atual_fact + parser.atual_fact.lower() + '+'
        elif any(answer.lower() == s for s in FALSE_ANSWER):
            next = parser.atual_fact + parser.atual_fact.lower() + '!+'
        else:
            print("\n" + BOT_NAME, end='')
            realType("não entendi :( vou repetir a pergunta!"+ "\n")
            continue
        for w in parser.structured_rules:
            if (next == w.npi_left):
                parser.atual_fact = w.npi_right

        if(ord(parser.atual_fact) in range(76,90)):
            print("\n" + BOT_NAME, end='')
            
            color = Color.GREEN
            realType(f"Certo, com as informações colhidas e utilizando meu algoritmo. Acredito que o melhor notebook para voce é o: { color }{N_answer[parser.atual_fact]}{ Color.END } \n\n")
            finalString = 'https://zoom.com.br/search?sortBy=prod_items_sort_by_price_asc&q='  + urllib.parse.quote(N_answer[parser.atual_fact])
            print(BOT_NAME, end='')
            realType('para facilitar sua vida, abri o produto em seu navegador. Obrigado, volte sempre ♥' + '\n\n')
            time.sleep(2)
            webbrowser.open(finalString, new = 2, autoraise=False)
            #DEBUG
            #prompt.do_solve(parser.queries)
            parserSolve = ESParser(prompt.get_lines())
            res = resolve_lines(parserSolve, True)
            break

if __name__ == "__main__":
    args = Cmd.args

    try:
        with open(args.input) as f:
            lines = f.readlines()

            if args.mode == "interface":
                parser = ESParser(lines)
                gui = GUI()
                gui.setConfig(Prompt.ESPrompt(lines), parser, lines)
            else: 
                os.system('cls' if os.name == 'nt' else 'clear')
                parser = ESParser(lines)
                chatbot(parser)

    except (Exception, BaseException) as e:
        print(e)
        sys.exit(1)


