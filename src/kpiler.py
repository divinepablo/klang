from typing import Dict
from kparser import KParser
from klexer import KLexer
from dataclasses import dataclass, field
from shared import predefined_functions_to_argc, types
from llvmlite import ir
from llvmlite import binding as llvm

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
    llvm_function: ir.Function = None
    local_variables: Dict[str, ir.Value] = field(default_factory=dict)
    local_variable_to_type: Dict[str, type] = field(default_factory=dict)

class KPiler:
    def __init__(self) -> None:
        self.func_to_argc = dict(predefined_functions_to_argc)
        self.create_module()

    def create_module(self):
        self.module = ir.Module(name="kmodule")
        self.llvm_functions = {}
        for name, argc in predefined_functions_to_argc.items():
            func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32)] * argc)
            func = ir.Function(self.module, func_type, name=name)
            self.llvm_functions[name] = func

    def compile_function(self, func):
        name = func[1]
        block = func[4][1]
        args = func[3][1]
        arg_count = len(args)
        self.func_to_argc[name] = arg_count

        func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32)] * arg_count)
        llvm_func = ir.Function(self.module, func_type, name=name)
        self.llvm_functions[name] = llvm_func

        entry_block = llvm_func.append_basic_block("entry")
        builder = ir.IRBuilder(entry_block)

        func_def = FunctionDefinition(name, llvm_function=llvm_func)
        for i, hi in enumerate(args):
            func_def.local_variables[hi[1]] = llvm_func.args[i]
            func_def.local_variable_to_type[hi[1]] = type(hi[1])

        for inst in block:
            self.compile_instruction(func_def, inst, builder)
        
        builder.ret(0)

    def compile_instruction(self, func: FunctionDefinition, inst, builder: ir.IRBuilder):
        int32 = ir.IntType(32)

        if isinstance(inst, tuple):
            opcode = inst[0]

            if opcode == 'var':
                var_value = func.local_variables[inst[1]]
                builder.load(var_value)

            elif opcode == 'DECLARE':
                value = self.compile_instruction(func, inst[3], builder)
                index = len(func.local_variables)
                var_type = types[inst[1]]
                alloca = builder.alloca(var_type, name=inst[2])
                func.local_variables[inst[2]] = alloca
                func.local_variable_to_type[inst[2]] = var_type
                builder.store(value, alloca)

            elif opcode == 'ASSIGN':
                value = self.compile_instruction(func, inst[2], builder)
                index = func.local_variables[inst[1]]
                builder.store(value, index)

            # Add more opcode handling cases here, similar to the previous implementation
            # but using the ir.Builder methods instead of string-based instructions

            else:
                raise Exception(f'Unknown opcode \'{opcode}\': "{inst}"')

        elif isinstance(inst, str):
            string_constant = ir.Constant(ir.ArrayType(int32, len(inst)), bytearray(inst.encode("utf-8")))
            string_global = ir.GlobalVariable(self.module, string_constant.type, name=f".str{len(self.module.global_variables)}")
            string_global.global_constant = True
            string_global.initializer = string_constant
            return builder.gep(string_global, [int32(0), int32(0)])

        elif isinstance(inst, bool):
            return int32(int(inst))

        elif isinstance(inst, list):
            # Implement array handling using ir.Builder methods
            pass
        else:
            return int32(inst)

    def compile(self, src: str):
        lexer = KLexer()
        parser = KParser()
        parsed = parser.parse(lexer.tokenize(src))

        for hi in parsed:
            opcode = hi[0]
            if opcode == 'DECLARE_FUNC':
                self.compile_function(hi)
            elif opcode == 'IMPORT':
                with open(hi[1], 'r') as f:
                    self.compile(f.read())

        return str(self.module)

def main(source: str):
    compiled = KPiler().compile(source)
    print('Compiled successfully')
    return compiled


if __name__ == '__main__':
    src = input("Source file: ")
    with open(src, 'r') as f:
        with open(src + '.ll', 'w') as f2:
            f2.write(main(f.read()))
