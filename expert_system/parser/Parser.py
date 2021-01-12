import re
from .Rule import ESRule
from expert_system.util.Log import Logger

logger = Logger("Parser")


class ESParser:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.raw_rules = []
        self.structured_rules = []
        self.facts = []
        self.queries = []
        self.atual_fact = 'A'
        self.ft_parser()
        self.set_structured_rules()

    def set_structured_rules(self):
        for raw_rule in self.raw_rules:
            self.structured_rules.append(ESRule(raw_rule))


    @staticmethod
    def ft_split_operators(formula):
        return re.split(r'!|\||\+|\^|', formula)

    @staticmethod
    def ft_check_parentheses(rule):
        return rule.count("(") == rule.count(")")

    @staticmethod
    def ft_all_atoms(rules):
        atoms = []
        for elem in rules:
            atoms = atoms + list(filter(None, re.split(r'\s|!|\+|\^|=>|\||<=>|=|>|<|\(|\)', elem)))

        return atoms

    @staticmethod
    def ft_check_facts_in_list_atoms(atoms, facts):
        fact = list(filter(None, re.split(r'=|\s', facts)))
        if fact:
            fact = list(fact[0])
        for elem in fact:
            if elem not in atoms:
                return False
        return True

    @staticmethod
    def ft_check_queries_in_list_atoms(atoms, queries):
        query = list(filter(None, re.split(r'\?|\s', queries)))
        if query:
            query = list(query[0])
        else:
            return False
        for elem in query:
            if elem not in atoms:
                return False
        return True

    def ft_parser(self):
        #input_lines obtem as linhas do arquivo em forma sem o \n
        input_lines = [x.strip('\n') for x in self.raw_input]

        #content_file filtra os elementos vazios da lista de input_line
        content_file = list(filter(None, input_lines))

        #Expressoes regulares para aceitação de alfabeto de regras, fatos e quieries.
        regex_rule = re.compile(r"(^((\()*(\s)*(!){0,2})*(\s)*[a-zA-Z](\s)*(\))*((\s*[+|^]\s*((\()*(\s)*(!){0,2})*(\s)*[a-zA-Z](\s)*(\))*)*)?\s*(=>|<=>)\s*((\()*(\s)*(!){0,2})*[a-zA-Z](\s)*(\))*((\s*[+]\s*((\()*(\s)*(!){0,2})*(\s)*[a-zA-Z](\s)*(\))*)*)?\s*$)")
        regex_fact = re.compile(r"(^=[a-zA-Z]*(\s)*$)")
        regex_queries = re.compile(r"(^\?[A-Z]*$)")

        fact = 1
        queries = 1
        rule = 1
        atoms = []
        rules = []

        for elem in content_file:

            if not elem:
                continue
            if elem[0] == '=':
                atoms = ESParser.ft_all_atoms(rules)
                fact -= 1
            elif elem[0] == '?':
                queries -= 1
            else:
                rule -= 1
                rules += elem

            if elem[0] != '=' and elem[0] != '?':
                self.raw_rules.append(elem)
            else:
                if elem[0] == '=':
                    self.facts = list(elem.replace('=', '').replace(' ', '').replace("\t", ""))
                else:
                    self.queries = list(elem.replace('?', '').replace(' ', '').replace("\t", ""))
        if fact > 0 or queries > 0 or rule > 0:
            raise BaseException("Missing one of facts, queries or rules")
