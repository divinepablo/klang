from klexer import KLexer
from sly import Parser


class KParser(Parser):
    tokens = KLexer.tokens
    # debugfile = 'parser.out'
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )

    def __init__(self):
        self.vars = {}

    @_('expression')
    def program(self, p):
        return p.expression

    @_('statements')
    def program(self, p):
        return p.statements

    @_('')
    def empty(self, p):
        pass

    @_('empty')
    def program(self, p):
        return ()

    @_('empty')
    def farg_list(self, p):
        return []

    @_('empty')
    def arg_list(self, p):
        return []

    @_('empty')
    def statements(self, p):
        return []

    @_('statement')
    def statements(self, p):
        return (p.statement, )

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement, )

    @_('statement')
    def program(self, p):
        return p.expression

    @_('type')
    def program(self, p):
        return p.type

    @_('INT', 'FLOAT', "STRING")
    def expression(self, p):
        return p[0]

    @_('TRUE')
    def expression(self, p):
        return True

    @_('expression PLUS expression')
    def expression(self, p):
        return ('ADD', p.expression0, p.expression1)

    @_('expression MINUS expression')
    def expression(self, p):
        return ('SUB', p.expression0, p.expression1)

    @_('expression TIMES expression')
    def expression(self, p):
        return ('MUL', p.expression0, p.expression1)

    @_('expression DIVIDE expression')
    def expression(self, p):
        return ('DIV', p.expression0, p.expression1)
    
    @_('expression MODULO expression')
    def expression(self, p):
        return ('MOD', p.expression0, p.expression1)

    @_('var')
    def expression(self, p):
        return p.var

    @_('ID')
    def var(self, p):
        return ('var', p.ID)

    @_('FALSE')
    def expression(self, p):
        return False

    @_('statement SEP')
    def statement(self, p):
        return p.statement

    @_('statement')
    def statement(self, p):
        return p.statement

    @_("declaration")
    def statement(self, p):
        return p.declaration

    @_("import_statement")
    def statement(self, p):
        return p.import_statement

    @_("assignment")
    def statement(self, p):
        return p.assignment

    @_('IMPORT STRING')
    def import_statement(self, p):
        return ('IMPORT', p.STRING)

    @_('FLOAT_TYPE')
    def type(self, p):
        return 'float'

    @_('INT_TYPE')
    def type(self, p):
        return 'int'

    @_('STRING_TYPE')
    def type(self, p):
        return 'string'

    @_('BOOL_TYPE')
    def type(self, p):
        return 'bool'

    @_('VOID_TYPE')
    def type(self, p):
        return 'void'

    @_('type ID ASSIGN expression SEP')
    def declaration(self, p):
        return ("DECLARE", p.type, p.ID, p.expression)

    @_('ID ASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, p.expression)

    @_('expression EQ expression')
    def expression(self, p):
        return ('EQ', p.expression0, p.expression1)
    
    @_('expression NEQ expression')
    def expression(self, p):
        return ('NEQ', p.expression0, p.expression1)

    @_('arg_list')
    def expression(self, p):
        return p.arg_list

    @_('expression')
    def arg_list(self, p):
        return [p.expression]

    @_('arg_list COMMA expression')
    def arg_list(self, p):
        p.arg_list.append(p.expression)
        return p.arg_list

    @_('farg_list')
    def expression(self, p):
        return p.farg_list

    @_('type ID')
    def farg_list(self, p):
        return [(p.type, p.ID)]

    @_('farg_list COMMA type ID')
    def farg_list(self, p):
        p.farg_list.append(p.expression)
        return p.farg_list

    @_('farg_list COMMA expression')
    def arg_list(self, p):
        p.farg_list.append(p.expression)
        return p.farg_list

    @_('function_define')
    def statement(self, p):
        return p.function_define

    @_('function_call')
    def statement(self, p):
        return p.function_call

    @_('if_statement')
    def statement(self, p):
        return p.if_statement
    
    @_('while_loop_statement')
    def statement(self, p):
        return p.while_loop_statement

    @_('type ID LPAREN farg_list RPAREN "{" statements "}"')
    def function_define(self, p):
        return ("DECLARE_FUNC", p.ID, p.type, ('args', p.farg_list), ('block', p.statements))

    @_('IF LPAREN expression RPAREN "{" statements "}"')
    def if_statement(self, p):
        return ("IF", p.expression, ('block', p.statements))
    
    @_('WHILE LPAREN expression RPAREN "{" statements "}"')
    def while_loop_statement(self, p):
        return ("WHILE", p.expression, ('block', p.statements))

    @_('IF LPAREN expression RPAREN "{" statements "}" ELSE "{" statements "}"')
    def if_statement(self, p):
        return ("ELSE", ('if', p.expression, ('if_block', p.statements1)), ('block', p.statements1))

    @_('IF LPAREN expression RPAREN "{" statements "}" ELSE IF LPAREN expression RPAREN "{" statements "}"')
    def if_statement(self, p):
        return ("ELIF", p.expression0, p.expression1, ('block', p.statements1))

    @_('ID LPAREN arg_list RPAREN')
    def function_call(self, p):
        return ("CALL", p.ID, p.arg_list)

    @_('PRINT LPAREN expression RPAREN')
    def function_call(self, p):
        return ("PRINT", p.expression)
