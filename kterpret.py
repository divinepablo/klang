import re
from typing import TypedDict
from dataclasses import dataclass, field
from shared import *

@dataclass
class Function:
    name: str
    arg_count: int
    stack: list = field(default_factory=list)
    locals: list = field(default_factory=list)
    code: list[str] = field(default_factory=list)
    pc: int = 0

@dataclass
class PredefinedFunction(Function):
    func: callable = None

class Interpreter:
    def __init__(self):
        self.functions: TypedDict[str, Function] = {}
        self.globals = {}
        for name, func in predefined_functions.items():
            self.functions[name] = PredefinedFunction(name, predefined_functions_to_argc[name], func=func)

    def execute_func(self, func: Function, *args):
        if func.name in predefined_functions:
            return predefined_functions[func.name](*args)
        for i in range(func.arg_count):
            func.locals.append(args[i])
        while func.pc < len(func.code):
            try:
                instruction = func.code[func.pc]
                # print(instruction, func.stack, func.pc)
                func.pc += 1
                if instruction.startswith('PUSH_VALUE'):
                    value = int(instruction.split()[1])
                    func.stack.append(value)
                elif instruction.startswith('PUSH_STRING'):
                    matched = re.findall(r'".*"', instruction)[0]
                    if matched is None:
                        raise Exception(
                            f"No string in PUSH_STRING: '{instruction}'")
                    value = matched
                    func.stack.append(value[1:-1])
                # elif instruction.startswith("STRING_LEN"):
                #     a = func.stack.pop()
                #     func.stack.append(len(a))
                # elif instruction.startswith("STRING_CONCAT"):
                #     a = func.stack.pop()
                #     b = func.stack.pop()
                #     func.stack.append(f"{b}{a}")
                # elif instruction.startswith("STRING_SUB"):
                #     value_a = int(instruction.split()[1])
                #     value_b = int(instruction.split()[2])
                #     a = func.stack.pop()
                #     func.stack.append(a[value_a:value_b])
                elif instruction.strip() == 'ADD':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a + b
                    func.stack.append(result)
                elif instruction.strip() == 'POP':
                    func.stack.pop()
                elif instruction.strip() == 'POLL':
                    func.stack.pop(0)
                    func.stack.append(result)
                elif instruction.strip() == 'INC':
                    a = func.stack.pop()
                    result = a + 1
                    func.stack.append(result)
                elif instruction.strip() == 'DEC':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a - 1
                    func.stack.append(result)
                elif instruction.strip() == 'SUB':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a - b
                    func.stack.append(result)
                elif instruction.strip() == 'MUL':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a * b
                    func.stack.append(result)
                elif instruction.strip() == 'DIV':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a / b
                    func.stack.append(result)
                elif instruction.strip() == 'MOD':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = a % b
                    func.stack.append(result)
                elif instruction.strip() == 'POP':
                    func.stack.pop()
                elif instruction.strip() == 'DUP':
                    value = func.stack[-1]
                    func.stack.append(value)
                elif instruction.strip() == 'COMPARE_EQ':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if a == b else 0
                    func.stack.append(result)
                elif instruction.strip() == 'COMPARE_LT':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if b < a else 0
                    func.stack.append(result)
                elif instruction.strip() == 'COMPARE_NEQ':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if a != b else 0
                    func.stack.append(result)
                elif instruction.strip() == 'COMPARE_GT':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if b > a else 0
                elif instruction.strip() == 'COMPARE_GTE':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if a >= b else 0
                    func.stack.append(result)
                elif instruction.strip() == 'COMPARE_LTE':
                    a = func.stack.pop()
                    b = func.stack.pop()
                    result = 1 if b <= a else 0
                    func.stack.append(result)
                elif instruction.startswith('JUMP_IF_FALSE'):
                    target = int(instruction.split()[1])
                    condition = func.stack.pop()
                    if not condition:
                        func.pc = target
                elif instruction.startswith('JUMP_IF_TRUE'):
                    target = int(instruction.split()[1])
                    condition = func.stack.pop()
                    if condition:
                        func.pc = target
                elif instruction.startswith('JUMP'):
                    target = int(instruction.split()[1])
                    func.pc = target
                elif instruction.strip() == 'DUP_BTM':
                    func.stack.append(func.stack[0])
                elif instruction.strip() == 'ARRAY_NEW':
                    func.stack.append([])
                elif instruction.strip() == 'ARRAY_ADD':
                    new = func.stack.pop()
                    func.stack[-1].append(new)
                elif instruction.strip() == 'RETURN':
                    ret = None
                    if len(func.stack) > 0:
                        ret = func.stack.pop()
                    return ret
                elif instruction.strip() == 'ARRAY_INDEX':
                    index = int(instruction.split()[1])
                    func.stack.append(func.stack[-1][index])
                # elif instruction.startswith('CALL_EXTERNAL'):
                #     split = instruction.split()
                #     _module = split[1]
                #     _func = split[2]
                #     arg_count = int(split[3])
                #     module = __import__(_module)
                #     function = getattr(module, _func)
                #     args = []
                #     for a in range(arg_count):
                #         args.append(func.stack.pop())
                #     result = function(*args)
                #     if result is not None:
                #         func.stack.append(result)
                elif instruction.startswith('SET_GLOBAL'):
                    split = instruction.split()
                    name = split[1]
                    self.globals[name] = func.stack.pop()
                elif instruction.startswith('GET_GLOBAL'):
                    split = instruction.split()
                    name = split[1]
                    func.stack.append(self.globals[name])
                elif instruction.startswith('SET_LOCAL'):
                    split = instruction.split()
                    index = int(split[1])
                    value = func.stack.pop()
                    
                    if index <= len(func.locals):
                        func.locals.append(value)
                    if not isinstance(value, type(func.locals[index])):
                        raise Exception(f"Cannot assign {type(value)} to {type(func.locals[index])}")
                    # print(isinstance(value, type(func.locals[index])))
                    func.locals[index] = value
                elif instruction.startswith('GET_LOCAL'):
                    split = instruction.split()
                    index = int(
                        split[1]) if split[1] != 'stack' else func.stack.pop()
                    func.stack.append(func.locals[index])
                elif instruction.startswith('CALL'):
                    split = instruction.split()
                    arg_count = int(split[2])
                    fargs = []
                    for a in range(arg_count):
                        fargs.append(func.stack.pop())
                    return_value = self.execute_func(
                        self.functions[split[1]], *fargs)
                    if return_value is not None:
                        func.stack.append(return_value)
                
                else:
                    return Exception(f'Unknown instruction {instruction.split()[0]}: "{instruction}"')
                
            except Exception as e:
                print(f'{e} when running: {instruction}')
                return e

    def parse(self, code):
        currentFunction: str = None
        for line in code.split('\n'):

            line = re.sub(r'\#.*', '', line)
            if line.strip() == '':
                continue
            elif line.startswith('DEFINE'):
                split = line.split()

                function = Function(split[1], int(split[2]))

                currentFunction = function.name
                self.functions[currentFunction] = function
            elif line.startswith('END'):
                currentFunction = None
            elif line.split()[0] in opcodes:
                self.functions[currentFunction].code.append(line)
            elif line.strip() in opcodes:
                self.functions[currentFunction].code.append(line)
            elif line.split()[0] == 'FILLER':
                continue
            elif not currentFunction:
                raise Exception(f'No function defined for instruction: {line}')
            else:
                raise Exception(f'Unknown instruction: {line}')

    def interpret(self, code):
        self.parse(code)
        exc = self.execute_func(self.functions['main'])
        if exc is not None and isinstance(exc, Exception):
            raise exc
        elif exc is not None:
            print("Program returned: " + exc)

def main(kasm):
    interpreter = Interpreter()
    interpreter.interpret(kasm)

if __name__ == '__main__':
    interpreter = Interpreter()
    with open('test.kasm', 'r') as f:

        interpreter.interpret(f.read())