from typing import Dict
from kparser import KParser
from klexer import KLexer
from dataclasses import dataclass, field
from shared import predefined_functions_to_argc, llvm_types
from llvmlite import ir
from llvmlite import binding as llvm
import os, subprocess, llvmlite

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

class KPiler:
    def __init__(self) -> None:
        self.create_module()
        self.llvm_functions: dict[str, ir.Function] = {}
        self.llvm_functions2: dict[str, ir.Function] = {}
        self.stringc = 0

    def create_module(self, hello: int = 0):
        self.module = ir.Module(name=f"kmodule={int}")
        self.module.triple = "x86_64-pc-linux-gnu"
        self.llvm_functions2 = {}
        # for name, argc in predefined_functions_to_argc.items():
        #     func_type = ir.FunctionType(llvm_types['int'], [ir.IntType(32)] * argc)
        #     func = ir.Function(self.module, func_type, name=name)
        #     self.llvm_functions[name] = func

    def compile_function(self, func):
        name = func[1]
        ftype = func[2]
        block = func[4][1]
        args = func[3][1]
        arg_count = len(args)
        farg_types = [llvm_types[arg[0]] for arg in args]
        func_type = ir.FunctionType(llvm_types[ftype], farg_types)
        llvm_func = ir.Function(self.module, func_type, name=name)
        self.llvm_functions[name] = llvm_func
        self.llvm_functions2[name] = llvm_func
        entry_block = llvm_func.append_basic_block("entry")
        builder = ir.IRBuilder(entry_block)

        func_def = FunctionDefinition(name, llvm_function=llvm_func)
        for i, hi in enumerate(args):
            func_def.local_variables[hi[1]] = llvm_func.args[i]

        for inst in block:
            self.compile_instruction(func_def, inst, builder)
        
        # if ftype == 'int':
        #     builder.ret(llvm_types['int'](0))
        # elif ftype == 'void':
        #     builder.ret_void()

    def compile_instruction(self, func: FunctionDefinition, inst, builder: ir.IRBuilder):
        if isinstance(inst, tuple):
            opcode = inst[0]
            if opcode == 'var':
                var_value = func.local_variables[inst[1]]
                return builder.load(var_value)

            elif opcode == 'DECLARE':
                if isinstance(inst[3], str):
                    value = self.compile_instruction(func, inst[3], builder)
                    var_type = value.type
                    alloca = builder.alloca(var_type, name=inst[2])
                    
                    func.local_variables[inst[2]] = alloca
                    builder.store(value, alloca)
                else:
                    value = self.compile_instruction(func, inst[3], builder)
                    var_type = llvm_types[inst[1]]
                    alloca = builder.alloca(var_type, name=inst[2])
                    func.local_variables[inst[2]] = alloca
                    builder.store(value, alloca)
            
            elif opcode == 'CALL':
                args = []
                for arg in inst[2]:
                    args.append(self.compile_instruction(func, arg, builder))
                print(f'Calling {self.llvm_functions2[inst[1]].name}')
                builder.call(self.llvm_functions2[inst[1]], args)
            elif opcode == 'ASSIGN':
                value = self.compile_instruction(func, inst[2], builder)
                index = func.local_variables[inst[1]]
                builder.store(value, index)
            elif opcode == 'RETURN':
                if inst[1] != 'void':
                    value = self.compile_instruction(func, inst[1], builder)
                    builder.ret(value)
                else:
                    builder.ret_void()



            # Add more opcode handling cases here, similar to the previous implementation
            # but using the ir.Builder methods instead of string-based instructions

            else:
                raise Exception(f'Unknown opcode \'{opcode}\': "{inst}"')

        elif isinstance(inst, str):
            inst += '\0'
            self.stringc += 1
            string_constant = ir.Constant(ir.ArrayType(llvm_types['char'], len(inst)), bytearray(inst.encode("utf-8")))
            string_global = ir.GlobalVariable(self.module, string_constant.type, name=f".str{self.stringc}")
            string_global.global_constant = True
            string_global.initializer = string_constant
            return builder.gep(string_global, [llvm_types['int'](0), llvm_types['int'](0)])

        elif isinstance(inst, bool):
            return llvm_types['bool'](int(inst))

        elif isinstance(inst, list):
            # Implement array handling using ir.Builder methods
            pass
        else:
            return llvm_types['int'](inst)

    def compile_code(self, src: str, module: ir.Module = None):
        if module is not None:
            self.module = module
        for func_name, func in self.llvm_functions.items():
            self.llvm_functions2[func_name] = ir.Function(self.module, func.ftype, func_name)
            self.llvm_functions2[func_name].linkage = 'external'
        
        if not 'printf' in self.llvm_functions:
            func_type = ir.FunctionType(llvm_types['int'], [ir.IntType(8).as_pointer()], True)
            llvm_func = ir.Function(self.module, func_type, name='printf')
            self.llvm_functions['printf'] = llvm_func
            self.llvm_functions2['printf'] = llvm_func
            
        lexer = KLexer()
        parser = KParser()
        parsed = parser.parse(lexer.tokenize(src))

        for hi in parsed:
            opcode = hi[0]
            if opcode == 'DECLARE_FUNC':
                self.compile_function(hi)
            elif opcode == 'IMPORT':
                with open(hi[1], 'r') as f:
                    self.compile_code(f.read())

        return self.module
    
    def compile(self, *files):
        hi = 0
        os.makedirs('build', exist_ok=True)
        _files = files
        for file in _files:
            hi += 1
            print(f'Compiling {file} ({hi}/{len(_files)})', end='', flush=True)
            with open(file, 'r') as f:
                self.create_module(hi)
                hi2 = self.compile_code(f.read())
                print(f'\rSaving {file} ({hi}/{len(_files)})', end='', flush=True)
                compiled = str(hi2)

                with open('build/' + file.replace('/', '.') + '.ll', 'w') as f:
                    f.write(compiled)
            
            print(f'\rCompiled {file} ({hi}/{len(_files)})')
        subprocess.run(['llvm-link', *['build/' + file.replace('/', '.') + '.ll' for file in _files], '-o', 'build/output.ll.bc'])
        subprocess.run(['llvm-dis', 'build/output.ll.bc', '-o', 'build/output.ll'])

        with open('build/output.ll', 'r') as f:
            contents = f.read()
        # for f in os.listdir('build'):
        #     os.remove('build/' + f)
        
        return contents

def main(*sources):
    compiled = KPiler().compile(*sources)
    print('Compiled successfully')
    return str(compiled)


if __name__ == '__main__':
    src = input("Source file: ")
    with open(src, 'r') as f:
        with open(src + '.ll', 'w') as f2:
            f2.write(KPiler().compile_code(f.read()))
