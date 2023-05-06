from llvmlite import ir
# int32 = 
opcodes = [
    'DEFINE',  # Defines function
    # 'END',    # Ends function parsing
    'SET_GLOBAL',  # Sets global variable
    'GET_GLOBAL',
    'SET_LOCAL',
    'GET_LOCAL',
    'PUSH_VALUE',
    'PUSH_STRING',
    # 'STRING_LEN', Scrapped due to predefined methods
    # 'STRING_CONCAT',
    # 'STRING_SUB',
    'POP',
    'POLL',
    'DUP',
    'DUP_BTM',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'INC',  # I accidentally made these useless but ig 'backwards compatiblity' or something
    'DEC',
    'RETURN',
    'COMPARE_EQ',
    'COMPARE_NEQ',
    'COMPARE_LT',
    'COMPARE_GT',
    'COMPARE_LTE',
    'COMPARE_GTE',
    'JUMP',
    'JUMP_IF_FALSE',
    'JUMP_IF_TRUE',
    # 'PRINT', # literally no use when i have predefined functions but was one of the best tests for stack
    'ARRAY_NEW',
    'ARRAY_ADD',
    'ARRAY_INDEX',
    'CALL',
    # 'CALL_EXTERNAL', Scrapped for predefined functions
]


def substring(string, start, end):
    return string[start:end]


def println(*args):
    print(*args)



predefined_functions = {
    # 'input': input,
    # 'length': len,
    # 'substring': lambda string, start, end: string[start:end],
    # 'print': print,
}

predefined_functions_to_argc = {}#{k: -1 if v == print else v.__code__.co_argcount for k, v in predefined_functions.items()}

types = {
    'int': int,
    'float': float,
    'string': str,
    'bool': bool,
    'string[]': list[str],
    'int[]': list[int],
    'float[]': list[float],
    'bool[]': list[bool],
}

llvm_types = {
    'int': ir.IntType(32),
    'float': ir.FloatType(),
    'char': ir.IntType(8),
    'bool': ir.IntType(1),
    
    'int*': ir.IntType(32).as_pointer(),
    'float*': ir.FloatType().as_pointer(),
    'char*': ir.IntType(8).as_pointer(),
    'bool*': ir.IntType(1).as_pointer(),

    'void': ir.VoidType()
    # 'string[]': list[str],
    # 'int[]': list[int],
    # 'float[]': list[float],
    # 'bool[]': list[bool],
}