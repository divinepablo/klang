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
    'INC', # I accidentally made these useless but ig 'backwards compatiblity' or something
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
    'input': input,
    'length': len,
    'substring': substring,
    'print': println,
}

predefined_functions_to_argc = {
    'input': 1,
    'length': 1,
    'substring': 3,
    'print': -1,
}