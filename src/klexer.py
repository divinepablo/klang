from sly import Lexer, Parser


class KLexer(Lexer): # this WILL error due to how SLY works (shit is beyond reflections)
    tokens = {
        ID, IMPORT,
        IF, ELSE, WHILE, RETURN,
        VOID_TYPE, FLOAT_TYPE, INT_TYPE, BOOL_TYPE, STRING_TYPE,
        FLOAT, INT, STRING,
        TRUE, FALSE, NULL,
        PLUS, TIMES, MINUS, DIVIDE, MODULO, 
        INCREM, DECREM, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN, MODASSIGN,
        NEQ, EQ, GT, LT, GTE, LTE,
        ASSIGN, LPAREN, RPAREN, LBRACKET, RBRACKET,
        # LBRACE, RBRACE,
        COMMA, SEP
    }
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['import'] = IMPORT
    ID['void'] = VOID_TYPE
    ID['null'] = NULL
    # ID['ref'] = REFERENCE # Scrapped for now
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['float'] = FLOAT_TYPE
    ID['int'] = INT_TYPE
    ID['string'] = STRING_TYPE
    ID['bool'] = BOOL_TYPE
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['return'] = RETURN

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.', ','}

    # Special symbols
    
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    MODASSIGN = r'%='
    INCREM = r'\+\+'
    DECREM = r'--'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MODULO = r'%'
    NEQ = r'!='
    EQ = r'=='
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    GT = r'>'
    LT = r'<'
    GTE = r'>='
    LTE = r'<='
    # LBRACE = r'\{'
    # RBRACE = r'\}'
    SEP = r';'
    COMMA = r','

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'0x[0-9a-fA-F]+', r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comments = r'\#.*'
    # Extra action for newlines

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
