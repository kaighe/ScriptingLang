from enum import Enum

class Lexer:
    opperators = [":", "+", "-", "*", "/", "=", "^"]
    other_reserved = ["\n", "(", ")"]
    def wordify(string):
        word_list = []
        word = ""
        for c in string:
            if(c == " "):
                if(word != ""):
                    word_list.append(word)
                word = ""
            elif(not c in Lexer.opperators and not c in Lexer.other_reserved):
                word += c
            else:
                if(word != ""):
                    word_list.append(word)
                word_list.append(c)
                word = ""
        if(word != ""):
            word_list.append(word)
                
        return word_list

    def tokenize(string):
        tokens = []
        word_list = Lexer.wordify(string)
        for w in word_list:
            if(w in Lexer.opperators):
                tokens.append(Token(TokenType.OP, w))
            elif(Lexer.is_number(w)):
                tokens.append(Token(TokenType.NUM, float(w)))
            elif(w == "\n"):
                tokens.append(Token(TokenType.END_LINE))
            elif(w == "("):
                tokens.append(Token(TokenType.OPEN_BRACKET))
            elif(w == ")"):
                tokens.append(Token(TokenType.CLOSE_BRACKET))
            else:
                tokens.append(Token(TokenType.ID, w))
        return tokens

    def is_number(string):
        decimals = 0
        if(string.replace(".", "").isdigit()):
            for c in string:
                if(c == "."):
                    decimals += 1
            if(decimals <= 1):
                return True
            else:
                return False
        else:
            return False
        
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    def __str__(self):
        if(self.value != None):
            return f"({self.type.name}: '{self.value}')"
        else:
            return f"({self.type.name})"
    def __repr__(self):
        return str(self)

class TokenType(Enum):
    OP = 0
    ID = 1
    END_LINE = 2
    NUM = 3
    OPEN_BRACKET = 4
    CLOSE_BRACKET = 5

class Parser:
    op_order = {
        "=":0, ":":0,
        "+":1, "-":1,
        "*":2, "/":2,
        "^":3
    }
    max_op = 3
    def parse(string):
        final = []
        action_list = Parser.split_actions(Lexer.tokenize(string))
        for a in action_list:
            final += Parser.parse_action_from_tokens(a)
        return final
        
    def split_actions(tokens):
        action_list = []
        temp = []
        for i in tokens:
            if(i.type != TokenType.END_LINE):
                temp.append(i)
            else:
                if(temp != []):
                    action_list.append(temp)
                temp = []
        if(temp != []):
            action_list.append(temp)
        return action_list
        
    def parse_action_from_tokens(tokens, d=0):
        action = tokens[0]

        while(tokens[0].type == TokenType.OPEN_BRACKET and tokens[-1].type == TokenType.CLOSE_BRACKET):
            tokens = tokens[1:-1]
        for op_depth in range(Parser.max_op+1):
            brackets_high = 0
            for i, token in enumerate(tokens):
                if(token.type == TokenType.OPEN_BRACKET):
                    brackets_high += 1
                elif(token.type == TokenType.CLOSE_BRACKET):
                    brackets_high -= 1
                if(token.type == TokenType.OP and Parser.op_order[token.value] == op_depth and brackets_high == 0):
                    left_tokens = []
                    right_tokens = []
                    brackets = 0
                    for l in reversed(range(0, i)):
                        if(tokens[l].type == TokenType.OPEN_BRACKET):
                            brackets += 1
                        elif(tokens[l].type == TokenType.CLOSE_BRACKET):
                            brackets -= 1
                        elif(tokens[l].type == TokenType.OP and Parser.op_order[tokens[l].value] < op_depth and brackets == 0):
                            break
                        left_tokens.insert(0, tokens[l])
                    brackets = 0
                    for l in range(i+1, len(tokens)):
                        if(tokens[l].type == TokenType.OPEN_BRACKET):
                            brackets += 1
                        elif(tokens[l].type == TokenType.CLOSE_BRACKET):
                            brackets -= 1
                        elif(tokens[l].type == TokenType.OP and Parser.op_order[tokens[l].value] < op_depth and brackets == 0):
                            break
                        right_tokens.append(tokens[l])
                    action = [token, Parser.parse_action_from_tokens(left_tokens, d=d+1), Parser.parse_action_from_tokens(right_tokens,  d=d+1)]
                    return action
        return action

class Functions:
    def print(a):
        print(a)

class Interpreter:
    def __init__(self):
        self.functions = [self.print]
        self.variables = {}
        self.out = ""
    def run(self, action_tree, d=0):
        if(type(action_tree) is Token):
            return action_tree
        function_dict = {}
        for f in self.functions:
            function_dict[f.__name__] = f

        for i, action in enumerate(action_tree):
            if(not type(action) is list and action.type == TokenType.OP):
                left = self.run(action_tree[i+1], d=d+1)
                right = self.run(action_tree[i+2], d=d+1)
                if(action.value == ":"):
                    right = self.handel_var(right)
                    out = function_dict[left.value](right.value)
                if(action.value == "+"):
                    out = self.to_num(left) + self.to_num(right)
                    out = Token(TokenType.NUM, out)
                if(action.value == "-"):
                    out = self.to_num(left) - self.to_num(right)
                    out = Token(TokenType.NUM, out)
                if(action.value == "*"):
                    out = self.to_num(left) * self.to_num(right)
                    out = Token(TokenType.NUM, out)
                if(action.value == "/"):
                    out = self.to_num(left) / self.to_num(right)
                    out = Token(TokenType.NUM, out)
                if(action.value == "^"):
                    out = pow(self.to_num(left), self.to_num(right))
                    out = Token(TokenType.NUM, out)
                if(action.value == "="):
                    right = self.handel_var(right)
                    self.variables[left.value] = right.value
                if(d != 0):
                    return out
    def print(self, string):
        print(string)
        self.out += str(string) + "\n"

    def handel_var(self, token):
        if(token.type == TokenType.ID):
            return Token(TokenType.NUM, self.variables[token.value])
        return token
    def to_num(self, token):
        token = self.handel_var(token)
        return float(token.value)