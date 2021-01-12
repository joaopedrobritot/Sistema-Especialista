import cmd

from .util.Color import Color
from expert_system.parser.Parser import ESParser
from expert_system import Tree


class ESPrompt(cmd.Cmd):
    def __init__(self, lines):
        super(ESPrompt, self).__init__()
        self.lines = []
        self.prompt = f'{ Color.PURPLE }<ExpertSystem> { Color.END }'
        self.set_lines(lines)

    def get_lines(self):
        return self.lines
        
    def set_lines(self, lines):
        self.lines = [f for f in filter(None, [l.replace("\n", "").replace(" ", "").replace("\s", "") for l in lines])]

    def do_solve(self, id):
        try:
            parser = ESParser(self.lines)
            queries = [id] if id else parser.queries
            tree = Tree.NPITree(parser.structured_rules, parser.facts, parser.queries)

            for query in queries:
                print(f"{query} resolved as", tree.resolve_query(query))
        except (Exception, BaseException) as e:
            print(e)

    def do_open(self, path):
        try:
            with open(path) as f:
                lines = f.readlines()
                ESParser(lines)
                self.set_lines(lines)
            print(f"File { path } was successfully open")
        except Exception as e:
            print(e)

    # Add functions
    def do_add_rule(self, rule):
        if rule is None or rule.__len__() is 0:
            print("<rule> argument required")
            return

        self.lines.insert(0, rule)
        try:
            ESParser(self.lines)
            print(f"{rule} was successfully added")
        except (Exception, BaseException) as e:
            print(f"Error adding the rule {rule}: { e }")
            self.lines.pop(0)

    def do_add_fact(self, fact):
        if fact is None or fact.__len__() is 0:
            print("<fact> argument required")
            return

        for i, line in enumerate(self.lines):
            if line[0] == "=":
                if fact not in line:
                    self.lines[i] = line[:1] + fact + line[1:]
                try:
                    ESParser(self.lines)
                    #print(f"{ fact } was successfully added")

                except:
                    print(f"Error adding the fact { fact }")
                    self.lines[i] = line
                return

    def do_add_query(self, query):
        if query is None or query.__len__() is 0:
            print("<query> argument required")
            return

        for i, line in enumerate(self.lines):
            if line[0] == "?":
                if query not in line:
                    self.lines[i] = line[:1] + query + line[1:]
                try:
                    ESParser(self.lines)
                    print(f"{ query } was successfully added")
                except:
                    print(f"Error adding the query { query }")
                    self.lines[i] = line
                return

    def do_del_rule(self, rule_id):
        if rule_id is None or rule_id.__len__() is 0:
            print("<rule_id> argument required")
            return
        try:
            id = int(rule_id)
            if self.lines[id][0] != "=" and self.lines[id][0] != "!":
                self.lines.pop(id)
            else:
                print("Index is not valid")

        except Exception as e:
            print("Index is not valid")

    def do_del_fact(self, fact):
        if fact and fact.isupper():
            for i, line in enumerate(self.lines):
                if line[0] == "=":
                    self.lines[i] = line.replace(fact, "")

    def do_del_query(self, query):
        if query and query.isupper():
            for i, line in enumerate(self.lines):
                if line[0] == "?":
                    self.lines[i] = line.replace(query, "")