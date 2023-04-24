from typing import Dict
from kparser import KParser
from klexer import KLexer
from dataclasses import dataclass, field
def hid(t):
    if isinstance(t, tuple):
        return "\n".join([hid(x) for x in t])
    if isinstance(t, list):
        return '['+", ".join([hid(x) for x in t])+']'
    else:
        return str(t)

@dataclass
class FunctionDefinition:
    name: str
    bytecode_index: int = 0
    code: list[str] = field(default_factory=list)
    local_variables: Dict[str, int] = field(default_factory=dict)
    local_variable_to_type: Dict[str, type] = field(default_factory=dict)

class KPiler:
    def __init__(self) -> None:
        self.func_to_argc = {}
        self.types = {
            'int': int,
            'float': float,
            'string': str,
        }

    def compile_function(self, func):
        output = []
        name = func[1]
        block = func[4][1]
        args = func[3][1]
        arg_count = len(args)
        self.func_to_argc[name] = arg_count
        func_def = FunctionDefinition(name)
        output.append(f"DEFINE {name} {arg_count}")
        for hi in args:
            func_def.local_variables[hi[1]] = len(func_def.local_variables)
            func_def.local_variable_to_type[hi[1]] = type(hi[1])
        for inst in block:
            result = self.compile_instruction(func_def, inst)
            func_def.bytecode_index += len(result)
            output.extend(result)
        output.append('RETURN')
        
        output.append('END')
        
        return output
    
    def invert_condition(self, instruction):
        outcode = ""
        opcode = instruction.split()[0]
        if opcode == 'EQ':
            outcode = instruction.replace(opcode, 'COMPARE_NEQ')
        elif opcode == 'NEQ':
            outcode = instruction.replace(opcode, 'COMPARE_EQ')
        elif opcode == 'GT':
            outcode = instruction.replace(opcode, 'COMPARE_LTE')
        elif opcode == 'LT':
            outcode = instruction.replace(opcode, 'COMPARE_GTE')
        elif opcode == 'GTE':
            outcode = instruction.replace(opcode, 'COMPARE_LT')
        elif opcode == 'LTE':
            outcode = instruction.replace(opcode, 'COMPARE_GT')
        return outcode

    def compile_instruction(self, func: FunctionDefinition, inst):
        result = []
        if isinstance(inst, tuple):
            opcode = inst[0]
            if opcode == 'var':
                result.append(f"GET_LOCAL {func.local_variables[inst[1]]}")
            elif opcode == 'DECLARE':
                result.extend(self.compile_instruction(func, inst[3]))
                index = len(func.local_variables)
                func.local_variables[inst[2]] = index
                func.local_variable_to_type[inst[2]] = self.types[inst[1]]
                result.append(f'SET_LOCAL {index}')
            elif opcode == 'ASSIGN':
                result.extend(self.compile_instruction(func, inst[2]))
                print("Added:", result)
                index = func.local_variables[inst[1]]
                result.append(f'SET_LOCAL {index}')
            elif opcode == 'ADD':
                result.extend(self.compile_instruction(func, inst[1]))
                result.extend(self.compile_instruction(func, inst[2]))
                result.append(f'ADD')
            elif opcode == 'SUB':
                result.extend(self.compile_instruction(func, inst[1]))
                result.extend(self.compile_instruction(func, inst[2]))
                result.append(f'SUB')
            elif opcode == 'MUL':
                result.extend(self.compile_instruction(func, inst[1]))
                result.extend(self.compile_instruction(func, inst[2]))
                result.append(f'MUL')
            elif opcode == 'DIV':
                result.extend(self.compile_instruction(func, inst[1]))
                result.extend(self.compile_instruction(func, inst[2]))
                result.append(f'DIV')
            elif opcode == 'MOD':
                result.extend(self.compile_instruction(func, inst[1]))
                result.extend(self.compile_instruction(func, inst[2]))
                result.append(f'MOD')
            elif opcode == 'PRINT':
                result.extend(self.compile_instruction(func, inst[1]))
                result.append('PRINT')
            elif opcode == 'CALL':
                for arg in inst[2]:
                    result.extend(self.compile_instruction(func, arg))
                result.append(f'CALL {inst[1]} {self.func_to_argc[inst[1]]}')
            elif opcode == 'EQ':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_EQ')
            elif opcode == 'NEQ':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_NEQ')
            elif opcode == 'GT':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_GT')
            elif opcode == 'LT':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_LT')
            elif opcode == 'GTE':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_GTE')
            elif opcode == 'LTE':
                _, expression1, expression2 = inst
                result.extend(self.compile_instruction(func, expression1))
                result.extend(self.compile_instruction(func, expression2))
                result.append('COMPARE_LTE')
            elif opcode == 'IF':
                print(func.bytecode_index)
                expression = inst[1]
                result.extend(self.compile_instruction(func, expression))
                hi = []
                for hello in inst[2][1]:
                    hi.extend(self.compile_instruction(func, hello))
                    hi[-1] = self.invert_condition(hi[-1])
                jump_index = func.bytecode_index + len(result) + len(hi) + 1
                result.append(f'JUMP_IF_TRUE {jump_index}')
                result.extend(hi)
            elif opcode == 'WHILE':
                print(func.bytecode_index)
                expression = inst[1]
                result.extend(self.compile_instruction(func, expression))
                hi = []
                for hello in inst[2][1]:
                    hi.extend(self.compile_instruction(func, hello))
                hi.append(f'JUMP {func.bytecode_index}')
                jump_index = func.bytecode_index + len(result) + len(hi) + 1
                result.append(f'JUMP_IF_FALSE {jump_index}')
                result.extend(hi)
            elif opcode == 'ELSE':
                for arg in inst[2]:
                    result.extend(self.compile_instruction(func, arg))
                result.append(f'JUMP_IF_TRUE {inst[1]} {self.func_to_argc[inst[1]]}')
                result.append(f'JUMP {inst[1]} {self.func_to_argc[inst[1]]}')
                
            else:
                raise Exception(f'Unknown opcode \'{opcode}\': "{inst}"')
        elif isinstance(inst, str):
            result.append(f"PUSH_STRING \"{inst}\"") 
        elif isinstance(inst, bool):
            result.append(f"PUSH_VALUE {int(inst)}")
        else:
            result.append(f"PUSH_VALUE {inst}")
        return result
    def compile(self, src: str):
        lexer = KLexer()
        parser = KParser()
        parsed = parser.parse(lexer.tokenize(src))
        with open(f'{src.encode().hex()[:8]}.kmasm' ,'w') as f:
            for p in parsed:
                f.write(f'{hid(p)}\n')
        output = []
        
        
        for hi in parsed:
            opcode = hi[0]
            if opcode == 'DECLARE_FUNC':
                output.extend(self.compile_function(hi))
            elif opcode == 'IMPORT':
                with open(hi[1], 'r') as f:
                    output.extend(self.compile(f.read()).split('\n'))
        return '\n'.join(output)

def main(source: str):
    compiled = KPiler().compile(source)
    print('Compiled successfully')
    return compiled

