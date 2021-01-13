############ CONSTANTS ###########
DIGITS = '0123456789'
##################################

############## ERROR##############

class Error:
    def __init__(self, name, details):
        self.name = name
        self.details = details

    def return_error(self):
        return f'{self.name}: {self.details}'


class IllegalCharacterError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)



############# Tokens #############

TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MUL = 'MUL'
TOKEN_DIV = 'DIV'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'



class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current_char = None 
        self.advance()

    def advance(self):
        self.position += 1
        self.current_char = self.text[self.position]  if self.position < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in [' ', '\t']:
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char == '+':
                tokens.append(Token(TOKEN_PLUS))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TOKEN_MINUS))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TOKEN_MUL))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TOKEN_DIV))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()
            
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError("'" + char + "'")

        return tokens, None

    def make_number(self):
        number_str = ''
        dots = 0

        while self.current_char != None and self.current_char in DIGITS + '.': 
            if self.current_char == '.':
                if dots == 1: break
                dots += 1
                number_str += '.'
            else:
                number_str += self.current_char
            self.advance()

        if dots == 0:
            return Token(TOKEN_INT, int(number_str))
        else:
            return Token(TOKEN_FLOAT, float(number_str))


############## RUN ###############

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error