import token_types as tt
import random, string, sys, os

class Error:
    def __init__(self, title, details):
        self.title = title
        self.details = details

    def __repr__(self):
        return f'{self.title}: {self.details}'

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Char', details)

class ArithmeticError(Error):
    def __init__(self, details):
        super().__init__('Arithmetic Exeption', details)

class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__('Invalid Syntax', details)

class NotFoundError(Error):
    def __init__(self, details):
        super().__init__('Not Found', details)

class IllegalArgumentError(Error):
    def __init__(self, details):
        super().__init__('Illegal Argument', details)

class RuntimeError(Error):
    def __init__(self, details):
        super().__init__('Runtime Error', details)

class Token:
    def __init__(self, type_, value=None): # value é opcional, por isso o =None
        self.type = type_
        self.value = value

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value else f'{self.type}'

class Lexer: 
    def __init__(self, code):
        if code == '':
            fail(InvalidSyntaxError(
                f'Empty file.'
            ))
        self.code = code 
        self.pos = 0
        self.char = self.code[self.pos] # primeiro carátere.
                            
    def advance(self):
        self.pos += 1
        self.char = self.code[self.pos] if self.pos < len(self.code) else None

    def lex(self):
        tokens = []
        while self.char is not None: # self.char != None funciona também
            if self.char in ' \t':
                self.advance()
                continue
        
            if self.char in tt.NUMBERS: # aquela explicacao de antes
                tokens.append(self.lex_nums())
                continue

            if self.char in '\'"':
                tokens.append(self.lex_str())
                self.advance()
                continue

            if self.char in tt.CHARACTERS:
                tokens.append(self.lex_id())
                continue

            if self.char in ';\n':
                tokens.append(Token(tt.NEWLINE))
                self.advance()
                continue
        
            match self.char:
                case '@':
                    while self.char != '\n':
                        self.advance()
                case '+':
                    tokens.append(Token(tt.PLUS))
                case '-':
                    tokens.append(Token(tt.MINUS))
                case '*':
                    tokens.append(Token(tt.MULTI))
                case '/':
                    tokens.append(Token(tt.DIVIS))
                case '^':
                    tokens.append(Token(tt.POW))
                case '.':
                    tokens.append(Token(tt.DOT))
                case '(':
                    tokens.append(Token(tt.OPEN_PAREN))
                case ')':
                    tokens.append(Token(tt.CLOSE_PAREN))
                case '{':
                    tokens.append(Token(tt.OPEN_BRACE))
                case '}':
                    tokens.append(Token(tt.CLOSE_BRACE))
                case '[':
                    tokens.append(Token(tt.OPEN_BRACKET))
                case ']':
                    tokens.append(Token(tt.CLOSE_BRACKET))
                case ',':
                    tokens.append(Token(tt.COMMA))
                case ':':
                    tokens.append(Token(tt.COLON))
                case '=':
                    if self.get_next() == '=':
                        self.advance()
                        tokens.append(Token(tt.LOG_EQ))
                        self.advance()
                        continue

                    tokens.append(Token(tt.ASSIGNMENT))
                case '!':
                    if self.get_next() != '=':
                        fail(InvalidSyntaxError(
                            f"Unknown token: '!'. Did you mean 'not'?"
                        ))

                    self.advance()
                    tokens.append(Token(tt.LOG_NEQ))
                case '>':
                    if self.get_next() == '=':
                        self.advance()
                        tokens.append(Token(tt.LOG_GTE))
                        self.advance()
                        continue

                    tokens.append(Token(tt.LOG_GT))
                case '<':
                    if self.get_next() == '=':
                        self.advance()
                        tokens.append(Token(tt.LOG_LTE))
                        self.advance()
                        continue

                    tokens.append(Token(tt.LOG_LT))
                case ' ':
                    self.advance()
                    continue
                case None:
                    break
                case _:
                    fail(IllegalCharError(f"'{self.char}'"))
            self.advance()

        tokens.append(Token(tt.EOF))
        return tokens
        
    def lex_nums(self):
        num_str = ''
        dot = False # ver se tem um ponto. se tiver, o token sera um float.
        while str(self.char) in tt.NUMBERS + '.' and self.char is not None:
            num_str += self.char 
            if self.char == '.': 
                if dot: # se ja tiver um ponto, quer dizer que o numero e invalido e ele so vai quitar do loop
                    break
        
                dot = True
            self.advance()
        
        try:
            return Token(tt.INT, int(num_str)) if not dot else Token(tt.FLOAT, float(num_str))
        except ValueError: # se, mesmo assim, tiver um erro na conversao
            fail(ArithmeticError("Float definition with more than one dot."))

    def lex_str(self):
        str_str = ''
        self.advance()
        while str(self.char) not in "'\"":
            if self.char == None:
                break

            str_str += str(self.char)
            self.advance()

        return Token(tt.STRING, str_str)

    def lex_id(self):
        id_str = ''
        while self.char is not None and str(self.char) in tt.CHARACTERS:
            id_str += self.char
            self.advance()

        match id_str:
            case 'or':
                return Token(tt.LOG_OR)
            case 'and':
                return Token(tt.LOG_AND)
            case 'not':
                return Token(tt.LOG_NOT)
            case 'in':
                return Token(tt.LOG_IN)

        return Token(tt.IDENTIFIER, id_str) if not id_str in tt.KEYWORDS else Token(tt.KEYWORD, id_str)

    def get_next(self):
        return self.code[self.pos + 1] if self.pos + 1 < len(self.code) else fail(InvalidSyntaxError('Reached end of file while lexing.'))

# Nodes .

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'program: \n{self.statements}'

class StringNode:
    def __init__(self, tok):
        self.str = tok
        
    def __repr__(self):
        return f'string: {self.str}'

class NumberNode: # para numeros
    def __init__(self, num_tok):
        self.tok = num_tok
    
    def __repr__(self):
        return f'{self.tok}'

class BooleanNode:
    def __init__(self, value):
        self.value = value 

    def __repr__(self):
        return f'{self.value}'

class ReturnNode:
    def __init__(self, return_value=None):
        self.value = return_value

    def __repr__(self):
        return f'return: {self.value}' if self.value else f'return'

class BreakNode:
    def __repr__(self):
        return 'break'

class ContinueNode:
    def __repr__(self):
        return 'continue'

class ListNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f'{self.elements}'

class VarAssignNode:
    def __init__(self, identifier, value=None):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f'assign {self.identifier} = {self.value}' if self.value else f'declare {self.identifier}'

class VarAccessNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f'access {self.identifier}'

class BinOpNode: # para operacoes binarias. caso nao sabe o que eh: 1 + 1 eh uma operacao binaria
    def __init__(self, left_node, op_tok, right_node):
        self.left = left_node
        self.op = op_tok
        self.right = right_node

    def __repr__(self):
        return f'({self.left} {self.op} {self.right})'

class UnaryOpNode: # para numeros assim o: -1
    def __init__(self, op_tok, comp):
        self.op = op_tok
        self.comp = comp
    
    def __repr__(self):
        return f'({self.op} {self.comp})'

class IfNode:
    def __init__(self, condition, statements, else_statements=None):
        self.condition = condition
        self.statements = statements
        self.else_statements = else_statements

    def __repr__(self):
       return  f'if: {self.condition} \ndo {self.statements} \nelse {self.else_statements}' if self.else_statements else f'if: {self.condition}\ndo {self.statements}'

class WhileNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f'execute {self.statements}\nwhile {self.condition}'

class ForNode:
    def __init__(self, var_identifier, list_, statements):
        self.id = var_identifier
        self.list = list_
        self.statements = statements

    def __repr__(self):
        return f'for each {self.id} in {self.list}\ndo {self.statements}'

class FuncDefNode:
    def __init__(self, identifier, args_list, statements):
        self.id = identifier
        self.args_list = args_list
        self.statements = statements

    def __repr__(self):
        return f'function {self.id}\n(args: {self.args_list})\nexecute: {self.statements}\n'

class FuncCallNode:
    def __init__(self, identifier, args_list):
        self.id = identifier
        self.args_list = args_list

    def __repr__(self):
        return f'call {self.id}\n(args: {self.args_list})\n'

class SwitchNode:
    def __init__(self, identifier, values, statements, default_case=None):
        self.id = identifier
        self.vals = values
        self.statements = statements
        self.default = default_case

class ElementAccessNode:
    def __init__(self, identifier, idx):
        self.id = identifier
        self.idx = idx

    def __repr__(self):
        return f'get element at {self.idx} from {self.id}'

class ElementAssignNode:
    def __init__(self, identifier, idx, value):
        self.id = identifier
        self.idx = idx
        self.value = value

    def __repr__(self):
        return f'edit element at {self.idx} from {self.id} with value {self.value}'

class ImportNode:
    def __init__(self, module_id):
        self.id = module_id

    def __repr__(self):
        return f'imports {self.id}'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_tok = self.tokens[self.pos]
        self.line = 1
    
    def before(self):
        return self.tokens[self.pos - 1]

    def advance(self):
        self.pos += 1
        self.current_tok = self.tokens[self.pos] if self.pos < len(self.tokens) else Token(tt.EOF)

    def parse(self): # vai fazer a arvore dos nossos tokens
        return ProgramNode(self.parse_statements())

    def parse_statements(self):
        statements = []
        while self.current_tok.type != tt.EOF:
            if self.current_tok.type == tt.NEWLINE:
                self.line += 1
                self.advance()
                continue
        
            statements.append(self.expr())
            if self.current_tok.type == tt.EOF:
                break # because after self.expr we may encounter an EOF before the next iteration

            if self.current_tok.type != tt.NEWLINE:
                if self.before().type == tt.NEWLINE:
                    continue
                fail(InvalidSyntaxError(
                    f'Expected a new line. {self.current_tok}'
                ))
            
            self.advance()

        return statements

    def parse_inner_statements(self):
        statements = []
        while self.current_tok.type != tt.CLOSE_BRACE:
            if self.current_tok.type == tt.NEWLINE:
                self.line += 1
                self.advance()
                continue
        
            statements.append(self.expr())
            if self.current_tok.type == tt.EOF:
                fail(InvalidSyntaxError(
                    f'Reached end of file while parsing: most likely means that there is an unclosed pair of curly-braces.'
                ))

            if self.current_tok.type == tt.CLOSE_BRACE:
                return statements

            if self.current_tok.type != tt.NEWLINE:
                if self.before().type == tt.NEWLINE:
                    continue
                fail(InvalidSyntaxError(
                    f'Expected a new line.'
                ))
            
            self.advance()

        return statements

    def atom(self): # fator: ele faz os numeros e tudo
        tok = self.current_tok

        if tok.type in (tt.INT, tt.FLOAT):
            self.advance()
            return NumberNode(tok)

        if tok.type == tt.STRING:
            self.advance()
            return StringNode(tok)

        if tok.type in tt.IDENTIFIER:
            self.advance()
            if self.current_tok.type == tt.ASSIGNMENT:
                self.advance()
                expr = self.expr()
                return VarAssignNode(tok.value, expr)
            
            if self.current_tok.type == tt.OPEN_BRACKET:
                self.advance()
                idx = self.expr()
                if self.current_tok.type != tt.CLOSE_BRACKET:
                    fail(InvalidSyntaxError(
                        f'Unclosed brackets.\nLine {self.line}.'
                    ))

                self.advance()
                if self.current_tok.type == tt.ASSIGNMENT:
                    self.advance()
                    expr = self.expr()
                    return ElementAssignNode(VarAccessNode(tok.value), idx, expr)

                return ElementAccessNode(VarAccessNode(tok.value), idx)
            
            if self.current_tok.type == tt.OPEN_PAREN:
                args_list = []
                self.advance()
                if self.current_tok.type == tt.CLOSE_PAREN:
                    self.advance()
                    return FuncCallNode(tok.value, args_list)

                while self.current_tok.type != tt.CLOSE_PAREN:
                    self.skip_newlines()
                    args_list.append(self.expr())
                    if self.current_tok.type == tt.CLOSE_PAREN:
                        break # double precaution

                    if self.current_tok.type != tt.COMMA:
                        fail(InvalidSyntaxError(
                            f"')' or ',' were expected, got '{self.current_tok}'."
                        ))

                    self.advance()

                self.advance()
                return FuncCallNode(tok.value, args_list)

            return VarAccessNode(tok.value)

        if tok.type == tt.OPEN_PAREN:
            self.advance()
            expr = self.expr()
            if self.current_tok.type != tt.CLOSE_PAREN:
                fail(InvalidSyntaxError(
                    f'Never closed parens.'
                ))

            self.advance()
            return expr

        fail(InvalidSyntaxError(
            f'Unexpected token: {self.current_tok}.'
        ))

    def power(self):
        return self.bin_op(self.atom, (tt.POW, ), self.factor)

    def factor(self):
        tok = self.current_tok
        if tok.type in (tt.PLUS, tt.MINUS, tt.LOG_NOT):
            self.advance()
            factor = self.factor()
            return UnaryOpNode(tok, factor)

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (tt.DIVIS, tt.MULTI, tt.DOT))

    def arith_expr(self):
        return self.bin_op(self.term, (tt.PLUS, tt.MINUS))

    def comp_expr(self):
        if self.current_tok.type == tt.LOG_NOT:
            op_tok = self.current_tok
            self.advance()
            return UnaryOpNode(op_tok, self.comp_expr())

        return self.bin_op(self.arith_expr, (tt.LOG_EQ, tt.LOG_NEQ, tt.LOG_LT, tt.LOG_LTE, tt.LOG_GT, tt.LOG_GTE, tt.LOG_IN))

    def expr(self):
        if self.current_tok.type == tt.KEYWORD:
            match self.current_tok.value:
                case 'if':
                    return self.parse_if_statement()
                case 'while':
                    return self.parse_while_statement()
                case 'for':
                    return self.parse_for_statement()
                case 'fn':
                    return self.parse_function_definition()
                case 'return':
                    self.advance()
                    return_value = self.expr()
                    return ReturnNode(return_value)
                case 'break':
                    self.advance()
                    return BreakNode()
                case 'continue':
                    self.advance()
                    return ContinueNode()
                case 'load':
                    self.advance()
                    module = self.current_tok
                    self.advance()
                    return ImportNode(module.value)
        
        if self.current_tok.type == tt.OPEN_BRACKET:
            return self.parse_list_definition()

        return self.bin_op(self.comp_expr, (tt.LOG_AND, tt.LOG_OR))

    def parse_function_definition(self):
        self.advance()
        if self.current_tok.type != tt.IDENTIFIER:
            fail(InvalidSyntaxError(
                f"An identifier was expected, got '{self.current_tok}'."
            ))

        identifier = self.current_tok.value
        self.advance()
        if self.current_tok.type != tt.OPEN_PAREN:
            fail(InvalidSyntaxError(
                f"'(' was expected, got '{self.current_tok}'."
            ))

        self.advance()
        args_list = []
        if self.current_tok.type != tt.CLOSE_PAREN and self.current_tok.type == tt.IDENTIFIER:
            while self.current_tok.type != tt.CLOSE_PAREN:
                self.skip_newlines()
                args_list.append(self.expr())
                if self.current_tok.type == tt.CLOSE_PAREN:
                    break # double precaution

                if self.current_tok.type != tt.COMMA:
                    fail(InvalidSyntaxError(
                        f"')' or ',' were expected, got '{self.current_tok}'."
                    ))

                self.advance()
        
        self.advance()
        if self.current_tok.type == tt.COMMA:
            self.advance()
            return FuncDefNode(identifier, args_list, [self.expr()])
        
        self.skip_newlines()
        if self.current_tok.type != tt.OPEN_BRACE:
            fail(InvalidSyntaxError(
                "'{' was expected, got '" + str(self.current_tok) + '\'.'
            ))

        self.advance()
        self.skip_newlines()
        statements = self.parse_inner_statements()
        self.skip_newlines()
        self.advance()
        return FuncDefNode(identifier, args_list, statements)

    def parse_for_statement(self):
        self.advance()
        if self.current_tok.type != tt.IDENTIFIER:
            fail(InvalidSyntaxError(
                f"An identifier was expected, got '{self.current_tok}'."
            ))

        identifier = self.current_tok.value
        self.advance()
        if self.current_tok.type != tt.LOG_IN:
            fail(InvalidSyntaxError(
                f"'in' was expected, got '{self.current_tok}'."
            ))

        self.advance()
        list_ = [self.expr()]
        if self.current_tok.type == tt.COMMA:
            self.advance()
            return ForNode(identifier, ListNode(list_), [self.expr()])
        
        self.skip_newlines()
        if self.current_tok.type != tt.OPEN_BRACE:
            fail(InvalidSyntaxError(
                "'{' or ',' were expected, got '" + str(self.current_tok) + "'\nLine " + str(self.line) + "."
            ))

        self.skip_newlines()
        self.advance()
        statements = self.parse_inner_statements()
        self.advance()
        self.skip_newlines()
        return ForNode(identifier, ListNode(list_), statements)

    def parse_list_definition(self):
        elements = []
        self.skip_newlines()
        self.advance()
        if self.current_tok.type == tt.CLOSE_BRACKET:
            self.advance()
            return ListNode(elements)

        while self.current_tok.type != tt.CLOSE_BRACKET:
            self.skip_newlines()
            elements.append(self.expr())
            if self.current_tok.type == tt.CLOSE_BRACKET:
                self.advance()
                break # double precaution

            if self.current_tok.type != tt.COMMA:
                fail(InvalidSyntaxError(
                    f"']' or ',' were expected, got '{self.current_tok}'."
                ))
            self.advance()
        
        return ListNode(elements)

    def parse_while_statement(self):
        self.advance()
        condition = self.expr()
        if self.current_tok.type == tt.COMMA:
            self.advance()
            return WhileNode(condition, [self.expr()])

        self.skip_newlines()
        if self.current_tok.type != tt.OPEN_BRACE:
            fail(InvalidSyntaxError(
                "'{' or ',' were expected, got " + str(self.current_tok)
            ))

        self.skip_newlines()
        self.advance()
        statements = self.parse_inner_statements()
        self.advance()
        self.skip_newlines()
        return WhileNode(condition, statements)

    def parse_if_statement(self):
        self.advance()
        condition = self.expr()
        if self.current_tok.type == tt.COMMA:
            self.advance()
            statements = [self.expr()]
            if self.current_tok.matches(tt.KEYWORD, 'else'):
                self.skip_newlines()
                else_statements = self.parse_else_statement()
                return IfNode(condition, statements, else_statements)

            return IfNode(condition, statements)
        
        self.skip_newlines()
        if self.current_tok.type != tt.OPEN_BRACE:
            fail(InvalidSyntaxError(
                "'{' or ',' were expected, got " + str(self.current_tok)
            ))
        
        self.skip_newlines()
        self.advance()
        statements = self.parse_inner_statements()
        self.advance()
        self.skip_newlines()
        if self.current_tok.matches(tt.KEYWORD, 'else'):
            self.skip_newlines()
            else_statements = self.parse_else_statement()
            return IfNode(condition, statements, else_statements)
        
        return IfNode(condition, statements)

    def parse_else_statement(self):
        self.advance()
        self.skip_newlines()
        if self.current_tok.type != tt.OPEN_BRACE:
            return [self.expr()]

        self.skip_newlines()
        self.advance()
        statements = self.parse_inner_statements()
        self.skip_newlines()
        self.advance()
        return statements

    def skip_newlines(self):
        while self.current_tok.type == tt.NEWLINE:
            self.line += 1
            self.advance()

    def bin_op(self, left_func, ops, right_func=None):
        if right_func == None:
            right_func = left_func

        left = left_func()
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = right_func()
            left = BinOpNode(left, op_tok, right)

        return left

class Variable:
    def __init__(self, identifier, val=None):
        self.id = identifier
        self.value = val

    def assign(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class VariableScope:
    def __init__(self, id_):
        self.id = id_
        self.symbols = []
        self.children = []

    def exists(self, identifier):
        for v in self.symbols:
            if v.id == identifier:
                return True

        if self.children:
            for c in self.children:
                for v in c.symbols:
                    if v.id == identifier:
                        return True

        return False

    def access(self, identifier):
        for v in self.symbols:
            if v.id == identifier:
                return v

        if self.children:
            for c in self.children:
                for v in c.symbols:
                    if v.id == identifier:
                        return v

        fail(NotFoundError(
            f'{identifier} does not exist.'
        ))

    def set(self, var):
        self.symbols.append(var)

    def set_child(self, scope):
        self.children.append(scope)

    def get_child(self, scope):
        for c in self.children:
            if c.id == scope:
                return c

    def destroy_child(self, scope):
        self.children.remove(scope)

    def __repr__(self):
        return self.id

class Value:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def plus(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} + {other.name}'
        ))

    def minus(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} - {other.name}'
        ))
    
    def multi(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} * {other.name}'
        ))

    def divis(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} / {other.name}'
        ))

    def power(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} ^ {other.name}'
        ))

    def compare_equals(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} == {other.name}'
        ))

    def compare_nequals(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} != {other.name}'
        ))

    def compare_greater(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} > {other.name}'
        ))

    def compare_greater_eq(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} >= {other.name}'
        ))

    def compare_smaller(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} < {other.name}'
        ))

    def compare_smaller_eq(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} <= {other.name}'
        ))

    def is_true(self):
        fail(ArithmeticError(
            f'{self.name} cannot be referred to a boolean type.'
        ))

    def negate(self):
        fail(ArithmeticError(
            f'{self.name} cannot be referred to a boolean type.'
        ))

    def and_(self, other):
        fail(ArithmeticError(
            f'{self.name} cannot be referred to a boolean type.'
        ))

    def or_(self, other):
        fail(ArithmeticError(
            f'{self.name} cannot be referred to a boolean type.'
        ))

    def check_contains(self, other):
        fail(ArithmeticError(
            f'Illegal operation: {self.name} in {other.name}'
        ))

class Number(Value):
    def __init__(self, value):
        super().__init__('<number>', value)

    def plus(self, other):
        return Number(self.value + other.value)

    def minus(self, other):
        return Number(self.value - other.value)
    
    def multi(self, other):
        return Number(self.value * other.value)

    def divis(self, other):
        return Number(self.value / other.value)

    def power(self, other):
        return Number(self.value ** other.value)

    def compare_equals(self, other):
        return Boolean(self.value == other.value)

    def compare_nequals(self, other):
        return Boolean(self.value != other.value)

    def compare_greater(self, other):
        return Boolean(self.value > other.value)

    def compare_greater_eq(self, other):
        return Boolean(self.value >= other.value)

    def compare_smaller(self, other):
        return Boolean(self.value < other.value)

    def compare_smaller_eq(self, other):
        return Boolean(self.value <= other.value)

    def is_true(self):
        return Boolean(self.value > -1)

    def negate(self):
        return Boolean(not self.value)

    def and_(self, other):
        return Boolean(self.value and other.value)

    def or_(self, other):
        return Boolean(self.value or other.value)

    def dot_string(self, argv):
        return String(str(self.value))

    def no_dot_method(self, argv):
        fail(RuntimeError(
            f'<number> has no attribute.'
        ))

    def check_contains(self, other):
        if not (isinstance(other, String) or isinstance(other, List)):
            fail(ArithmeticError(
                f'Illegal operation: {self.name} in {other.name}'
            ))
        
        return Boolean(self.value in other.value)

    def __repr__(self):
        return str(self.value)

class Boolean(Value):
    def __init__(self, bool_value):
        super().__init__('<boolean>', bool_value)

    def compare_nequals(self, other):
        return Boolean(self.value != other.value)

    def compare_equals(self, other):
        return Boolean(self.value == other.value)
        
    def is_true(self):
        return self.value

    def negate(self):
        return Boolean(not self.value)

    def and_(self, other):
        return Boolean(self.value and other.value)

    def or_(self, other):
        return Boolean(self.value or other.value)

    def check_contains(self, other):
        if not (isinstance(other, String) or isinstance(other, List)):
            fail(ArithmeticError(
                f'Illegal operation: {self.name} in {other.name}'
            ))
        
        return Boolean(self.value in other.value)

    def __repr__(self):
        match self.value:
            case True:
                return 'true'
            case False:
                return 'false'
            case None:
                return 'null'

class List(Value):
    def __init__(self, elements):
        super().__init__('<list>', elements)
        self.len = len(elements)

    def dot_string(self, argv):
        return String(str(self.value))

    def dot_append(self, argv):
        if len(argv) > 1:
            fail(RuntimeError(
                f'One argument expected in call \'append\''
            ))

        value = Interpreter().visit(argv[0])
        self.value.append(value)
        return self

    def dot_len(self, argv):
        return Number(len(self.value))

    def no_dot_method(self, argv):
        fail(NotFoundError(
            f'{self.name} has no attribute.'
        ))

    def check_contains(self):
        if not (isinstance(other, String) or isinstance(other, List)):
            fail(ArithmeticError(
                f'Illegal operation: {self.name} in {other.name}'
            ))
        
        return Boolean(self.value in other.value)
    
    def __repr__(self):
        return f'{self.value}'

class String(Value):
    def __init__(self, value):
        super().__init__('<str>', value)

    def plus(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} + {other.name}'
        ))

    def minus(self, other):
        if isinstance(other, String):
            return String(self.value - other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} - {other.name}'
        ))
    
    def multi(self, other):
        if isinstance(other, String):
            return String(self.value * other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} * {other.name}'
        ))

    def divis(self, other):
        if isinstance(other, String):
            return String(self.value / other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} / {other.name}'
        ))

    def power(self, other):
        if isinstance(other, String):
            return String(self.value ** other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} ^ {other.name}'
        ))

    def compare_equals(self, other):
        if isinstance(other, String):
            return Boolean(self.value == other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} == {other.name}'
        ))

    def compare_nequals(self, other):
        if isinstance(other, String):
            return Boolean(self.value != other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} != {other.name}'
        ))

    def compare_greater(self, other):
        if isinstance(other, String):
            return Boolean(self.value > other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} > {other.name}'
        ))

    def compare_greater_eq(self, other):
        if isinstance(other, String):
            return Boolean(self.value >= other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} >= {other.name}'
        ))

    def compare_smaller(self, other):
        if isinstance(other, String):
            return Boolean(self.value < other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} < {other.name}'
        ))

    def compare_smaller_eq(self, other):
        if isinstance(other, String):
            return Boolean(self.value <= other.value)
        
        fail(ArithmeticError(
            f'Illegal operation: {self.name} <= {other.name}'
        ))

    def and_(self, other):
        return Boolean(self.value and other.value)

    def or_(self, other):
        return Boolean(self.value or other.value)

    def dot_num(self, argv):
        try:
            return Number(int(self.value))
        except ValueError:
            fail(ArithmeticError(
                f'Cannot convert {self.value} to <number>.'
            ))

    def dot_len(self, argv):
        return Number(len(self.value))

    def dot_chararray(self, argv):
        return List([String(c) for c in self.value])

    def no_dot_method(self):
        fail(RuntimeError(
            f'<number> has no attribute.'
        ))

    def check_contains(self, other):
        if not (isinstance(other, String) or isinstance(other, List)):
            fail(ArithmeticError(
                f'Illegal operation: {self.name} in {other.name}'
            ))
        
        return Boolean(self.value in other.value)

    def __repr__(self):
        return f'{self.value}'

class Function(Value):
    def __init__(self, identifier, statements, args_list):
        super().__init__('<function>', identifier)
        self.id = identifier
        self.statements = statements
        self.args = args_list

    def __repr__(self):
        return f'<function {self.id}>'

class ExitFunction(Exception):
    def __init__(self, value):
        self.value = value

class ContinueLoop(Exception):
    pass

class BreakLoop(Exception):
    pass

class Interpreter:
    def visit(self, node):
        vst_method = getattr(self, f'visit_{type(node).__name__}', self.undefined_node)
        return vst_method(node)

    def undefined_node(self, node):
        raise Exception(f'No visit method named {type(node).__name__}')

    def visit_ProgramNode(self, node):
        interpreted_statements = []
        for s in node.statements:
            interpreted_statements.append(self.visit(s))

        return interpreted_statements
    
    def visit_ImportNode(self, node):
        run(node.id + '.bs')

    def visit_NumberNode(self, node):
        return Number(node.tok.value)

    def visit_StringNode(self, node):
        return String(node.str.value)

    def visit_BooleanNode(self, node):
        return Boolean(node.value)

    def visit_ListNode(self, node):
        new_elements = []
        for e in node.elements:
            new_elements.append(self.visit(e))

        return List(new_elements)

    def visit_ReturnNode(self, node):
        raise ExitFunction(self.visit(node.value))

    def visit_ContinueNode(self, node):
        raise ContinueLoop()

    def visit_BreakNode(self, node):
        raise BreakLoop()

    def visit_FuncDefNode(self, node):
        if scope.exists(node.id):
            fail(RuntimeError(
                f'Function {node.id} already exists.'
            ))

        if node.id in tt.PRIMITIVE_FUNCTIONS:
            fail(RuntimeError(
                f'Cannot override primitive function {node.id}.'
            ))

        func = Function(node.id, node.statements, node.args_list)
        scope.set(func)
        return func

    def visit_FuncCallNode(self, node):
        if node.id in tt.PRIMITIVE_FUNCTIONS:
            method = getattr(self, f'primitive_{node.id}')
            return method(node.args_list)

        fn = scope.access(node.id)
        if not isinstance(fn, Function):
            fail(InvalidSyntaxError(
                f'{fn.id} is not callable.'
            ))

        names = [a.identifier for a in fn.args]
        if len(fn.args) > len(node.args_list):
            fail(RuntimeError(
                f'Too few args passed into {fn.id}.'
            ))

        if len(fn.args) < len(node.args_list):
            fail(RuntimeError(
                f'Too many args passed into {fn.id}.'
            ))

        func_scope = VariableScope(node.id + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
        for i in range(len(fn.args)):
            func_scope.set(Variable(names[i], self.visit(node.args_list[i])))

        scope.set_child(func_scope)
        interpreted_statements = []
        try:
            for s in fn.statements:
                interpreted_statements.append(self.visit(s))
        except ExitFunction as e:
            scope.destroy_child(func_scope)
            return e.value

        scope.destroy_child(func_scope)

        return interpreted_statements

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right) if node.op.type != tt.DOT else node.right

        match node.op.type:
            case tt.PLUS:
                return left.plus(right)
            case tt.MINUS:
                return left.minus(right)
            case tt.MULTI:
                return left.multi(right)
            case tt.DIVIS:
                return left.divis(right)
            case tt.POW:
                return left.power(right)
            case tt.LOG_AND:
                return left.and_(right)
            case tt.LOG_OR:
                return left.or_(right)
            case tt.LOG_EQ:
                return left.compare_equals(right)
            case tt.LOG_NEQ:
                return left.compare_nequals(right)
            case tt.LOG_GT:
                return left.compare_greater(right)
            case tt.LOG_GTE:
                return left.compare_greater_eq(right)
            case tt.LOG_LT:
                return left.compare_smaller(right)
            case tt.LOG_LTE:
                return left.compare_smaller_eq(right)
            case tt.LOG_IN:
                return left.check_contains(right)
            case tt.DOT:
                if isinstance(right, FuncCallNode):
                    method = getattr(left, f'dot_{right.id}', left.no_dot_method)
                    return method(right.args_list)

    def visit_IfNode(self, node):
        executes = self.visit(node.condition)
        if executes.is_true():
            interpreted_statements = []
            for s in node.statements:
                interpreted_statements.append(self.visit(s))

            return interpreted_statements
        
        if node.else_statements:
            interpreted_statements = []
            for s in node.else_statements:
                interpreted_statements.append(self.visit(s))
            
            return interpreted_statements

    def visit_WhileNode(self, node):
        continues = self.visit(node.condition)
        interpreted_statements = []
        while True:
            continues = self.visit(node.condition) # updating continues each iteration.
            if not continues.is_true():
                break

            try:
                for s in node.statements:
                    interpreted_statements.append(self.visit(s))
            except ContinueLoop as e:
                continue
            except BreakLoop as e:
                break

        return interpreted_statements

    def visit_ForNode(self, node):
        results = []
        list_ = self.visit(node.list)
        if len(list_.value) == 1 and isinstance(list_.value[0], List):
            list_ = list_.value[0]

        idx = -1
        if len(list_.value) < 1:
            fail(IllegalArgumentError(
                f'Cannot iterate through empty list.'
            ))

        if not isinstance(list_, List):
            fail(IllegalArgumentError(
                f'Second argument in for loop must be a list.'
            ))

        scope.set(Variable(node.id, Number(1)))
        while idx < len(list_.value) - 1:
            idx += 1
            scope.access(node.id).assign(list_.value[idx])
            try:
                for s in node.statements:
                    results.append(self.visit(s))
            except ContinueLoop as e:
                continue
            except BreakLoop as e:
                break

        return results

    def visit_UnaryOpNode(self, node):
        expr = self.visit(node.comp)
        match node.op.type:
            case tt.LOG_NOT:
                return expr.negate()
            case tt.MINUS:
                return expr.multi(Number(-1))
            case tt.PLUS:
                return expr

    def visit_VarAssignNode(self, node):
        expr = self.visit(node.value)
        if scope.exists(node.identifier):
            scope.access(node.identifier).assign(expr)
            return expr
        
        scope.set(Variable(node.identifier, expr))
        return expr

    def visit_VarAccessNode(self, node):
        return scope.access(node.identifier).value

    def visit_ElementAccessNode(self, node):
        list_ = self.visit(node.id)
        return list_.value[self.visit(node.idx).value]

    def visit_ElementAssignNode(self, node):
        list_ = self.visit(node.id)
        val = self.visit(node.value)
        list_.value[self.visit(node.idx).value] = val
        return val

    def primitive_print(self, args_list):
        if len(args_list) != 1:
            fail(RuntimeError(
                f"One argument expected in call 'print'."
            ))

        print(self.visit(args_list[0]).value, end='')

    def primitive_println(self, args_list):
        if len(args_list) != 1:
            fail(RuntimeError(
                f"One argument expected in call 'println'."
            ))

        print(self.visit(args_list[0]).value)

    def primitive_readln(self, args_list):
        text = String(str(input()))
        return text

    def primitive_instanceof(self, args_list):
        if len(args_list) != 2:
            fail(RuntimeError(
                f'Two arguments expected in call \'instanceof\'.'
            ))

        return Boolean(self.visit(args_list[0]).name == self.visit(args_list[1]))

    def primitive_range(self, args_list):
        if len(args_list) == 1:
            return List([Number(n) for n in range(self.visit(args_list[0]).value)])

        return List([Number(n) for n in range(self.visit(args[0]), self.visit(args[1]))])
        
def fail(error):
    print(error)
    exit(0)

scope = VariableScope('global')
def run(fn):
   scope.set(Variable('true', Boolean(True)))
   scope.set(Variable('false', Boolean(False)))
   scope.set(Variable('null', Boolean(None)))
   scope.set(Variable('strnull', String('')))
   with open(fn, 'r') as f:
        lexer = Lexer(f.read()) # voce pode botar qualquer outro calculo
        tokens = lexer.lex()
        ast = Parser(tokens).parse()
        Interpreter().visit(ast)

run(sys.argv[1])