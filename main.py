import sys
import ast
import random
import codecs
import urllib.parse

from expert_system import Prompt, Tree, Print
from expert_system.parser.Parser import ESParser
from expert_system.config.Env import Env
from expert_system.config.Cmd import Cmd
from expert_system.util.Color import Color

dictionary = {}
B_answer = {}
N_answer = {}

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
            s = urllib.parse.quote('stackoverflow.com/questions/48689413/printing-a-link-python')
            print('Sugestão de compra: ' +  'https://'+s)
            #DEBUG
            # prompt.do_solve(parser.queries)
            # parserSolve = ESParser(prompt.get_lines())
            # res = resolve_lines(parserSolve)
            break
           
            
if __name__ == "__main__":
    args = Cmd.args

    try:
        with open(args.input) as f:
            lines = f.readlines()

            if args.mode == "interactive":
                Prompt.ESPrompt(lines).cmdloop()  
            else: 
                parser = ESParser(lines)
                chatbot(parser)

    except (Exception, BaseException) as e:
        print(e)
        sys.exit(1)