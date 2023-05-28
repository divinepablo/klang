from klexer import KLexer
from sly import Parser


class KParser(Parser):
    tokens = KLexer.tokens
    precedence = (
        ('right', ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN, MODASSIGN),
        ('left', EQ, NEQ),
        ('left', LT, LTE, GT, GTE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', INCREM, DECREM),
    )

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
    def statements(self, p):
        return []

    @_('empty')
    def expressions(self, p):
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

    @_('expression')
    def expressions(self, p):
        return [p.expression]

    @_('expressions COMMA expression')
    def expressions(self, p):
        return p.expressions + [p.expression]

    @_('INT', 'FLOAT', "STRING")
    def expression(self, p):
        return p[0]

    @_('TRUE')
    def expression(self, p):
        return True

    @_('dereference')
    def expression(self, p):
        return p.dereference
    
    @_('TIMES ID')
    def dereference(self, p):
        return ('DEREFERENCE', p.ID)
    
    @_('\'&\' ID')
    def expression(self, p):
        return ('ADDRESS', p.ID)
    
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

    @_('NULL')
    def expression(self, p):
        return None

    @_('statement SEP')
    def statement(self, p):
        return p.statement

    @_('expression SEP', 'declaration', 'assignment SEP', 'import_statement SEP',
       'return_statement', 'if_statement', 'while_loop_statement')
    def statement(self, p):
        return p[0]

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

    @_('FLOAT_TYPE LBRACKET RBRACKET')
    def type(self, p):
        return 'float[]'

    @_('INT_TYPE LBRACKET RBRACKET')
    def type(self, p):
        return 'int[]'

    @_('STRING_TYPE LBRACKET RBRACKET')
    def type(self, p):
        return 'string[]'

    @_('BOOL_TYPE LBRACKET RBRACKET')
    def type(self, p):
        return 'bool[]'

    @_('VOID_TYPE')
    def type(self, p):
        return 'void'

    @_('FLOAT_TYPE TIMES')
    def type(self, p):
        return 'float*'

    @_('INT_TYPE TIMES')
    def type(self, p):
        return 'int*'

    @_('STRING_TYPE TIMES')
    def type(self, p):
        return 'string*'

    @_('BOOL_TYPE TIMES')
    def type(self, p):
        return 'bool*'

    @_('VOID_TYPE TIMES')
    def type(self, p):
        return 'void*'
    
    @_('TIMES')
    def pointer(self, p):
        return 1
    
    @_('pointer TIMES')
    def pointer(self, p):
        return p.pointer + 1
    
    @_('INT_TYPE pointer')
    def type(self, p):
        return ('int*', p.pointer)

    @_('type ID ASSIGN expression SEP')
    def declaration(self, p):
        return ("DECLARE", p.type, p.ID, p.expression)

    @_('ID ASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, p.expression)
    
    # @_('dereference ASSIGN expression')
    # def assignment(self, p):
    #     return ("ASSIGN", p.ID, p.expression)

    @_('ID ADDASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('ADD', ('var', p.ID), p.expression))

    @_('ID SUBASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('SUB', ('var', p.ID), p.expression))

    @_('ID MULASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('MUL', ('var', p.ID), p.expression))

    @_('ID DIVASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('DIV', ('var', p.ID), p.expression))

    @_('ID MODASSIGN expression')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('MOD', ('var', p.ID), p.expression))

    @_('ID INCREM')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('ADD', ('var', p.ID), 1))

    @_('ID DECREM')
    def assignment(self, p):
        return ("ASSIGN", p.ID, ('SUB', ('var', p.ID), 1))

    @_('expression EQ expression', 'expression NEQ expression', 'expression GT expression', 'expression LT expression', 'expression GTE expression', 'expression LTE expression')
    def expression(self, p):
        return (p._slice[1].type, p.expression0, p.expression1)

    @_('LBRACKET expressions RBRACKET')
    def expression(self, p):
        return [p.expressions]

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

    @_('RETURN expression SEP')
    def return_statement(self, p):
        return ('RETURN', p.expression)

    @_('RETURN SEP')
    def return_statement(self, p):
        return ('RETURN', 'void')

    @_('function_call')
    def expression(self, p):
        return p.function_call

    @_('ID LPAREN expressions RPAREN')
    def function_call(self, p):
        return ("CALL", p.ID, p.expressions)

    @_('type ID LPAREN farg_list RPAREN "{" statements "}"')
    def declaration(self, p):
        return ("DECLARE_FUNC", p.ID, p.type, ('args', p.farg_list), ('block', p.statements))

    @_('type ID LPAREN farg_list RPAREN SEP')
    def declaration(self, p):
        return ("DECLARE_FUNC", p.ID, p.type, ('args', p.farg_list), ('block', None))

    @_('WHILE LPAREN expression RPAREN "{" statements "}"')
    def while_loop_statement(self, p):
        return ("WHILE", p.expression, ('block', p.statements))

    @_('IF LPAREN expression RPAREN "{" statements "}"')
    def if_statement(self, p):
        return ("IF", p.expression, ('block', p.statements))

    @_('IF LPAREN expression RPAREN "{" statements "}" else_statement')
    def if_statement(self, p):
        return ("IF", p.expression, ('block', p.statements), else_statement)

    @_('ELSE "{" statements "}"')
    def else_statement(self, p):
        return ("ELSE", ('if', p.expression, ('block', p.statements1)))

    @_('ELSE IF LPAREN expression RPAREN "{" statements "}"')
    def else_statement(self, p):
        return ("ELIF", p.expression, ('block', p.statements))

    
    @_('')  # no else or elif case
    def else_statement(self, p):
        return None
