############ CONSTANTS ##########
DIGITS = '0123456789'
#################################

############# ERROR #############

class Error:
    def __init__(self, pos_start, pos_end, name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.details = details

    def return_error(self):
        message = f'{self.name}: {self.details}\n'
        message += f'File {self.pos_start.file_n}, line {self.pos_start.ln + 1}'
        return message


class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


############ Position ############

class Position:
    def __init__(self, index, ln, col, file_n, file_txt):
        self.index = index
        self.ln = ln
        self.col = col
        self.file_n = file_n
        self.file_txt = file_txt

    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1 
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.file_n, self.file_txt)


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


############# Lexer #############

class Lexer:
    def __init__(self, file_n, text):
        self.file_n = file_n
        self.text = text
        self.pos = Position(-1, 0, -1, file_n, text)
        self.current_char = None 
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index]  if self.pos.index < len(self.text) else None

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
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos, "'" + char + "'")

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

def run(file_n, text):
    lexer = Lexer(file_n, text)
    tokens, error = lexer.make_tokens()
    return tokens, error