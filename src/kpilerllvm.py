from typing import Dict, Union
from kparser import KParser
from klexer import KLexer
from dataclasses import dataclass, field
from shared import llvm_types, py_to_llvm_types
from llvmlite import ir
from llvmlite import binding as llvm
import os
import subprocess
import llvmlite
import colorama
import traceback


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
    local_variables: Dict[str, Union[int, ir.Value]
                          ] = field(default_factory=dict)


class KPiler:
    def __init__(self) -> None:
        self.create_module()
        self.llvm_functions: dict[str, ir.Function] = {}
        self.stringc = 0

    def create_module(self, hello: int = 0):
        self.module = ir.Module(name=f"kmodule={int}")
        self.module.triple = "x86_64-pc-linux-gnu"

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
        if block is not None:
            entry_block = llvm_func.append_basic_block("entry")
            builder = ir.IRBuilder(entry_block)

            func_def = FunctionDefinition(name, llvm_function=llvm_func)
            for i, hi in enumerate(args):
                name = hi[1]
                local_var = builder.alloca(llvm_func.args[i].type, name=name)
                builder.store(llvm_func.args[i], local_var)
                func_def.local_variables[name] = local_var

            for inst in block:
                self.compile_instruction(func_def, inst, builder)

    def compile_instruction(self, func: FunctionDefinition, inst, builder: ir.IRBuilder):
        if isinstance(inst, tuple):
            opcode = inst[0]
            if opcode == 'var':
                return builder.load(func.local_variables[inst[1]])

            elif opcode == 'DECLARE':
                if isinstance(inst[3], str):
                    value = self.compile_instruction(func, inst[3], builder)
                    var_type = value.type
                    alloca = builder.alloca(var_type, name=inst[2])

                    func.local_variables[inst[2]] = alloca
                    return builder.store(value, alloca)
                else:
                    value = self.compile_instruction(func, inst[3], builder)
                    var_type = llvm_types[inst[1]]
                    alloca = builder.alloca(var_type, name=inst[2])
                    func.local_variables[inst[2]] = alloca
                    return builder.store(value, alloca)
            elif opcode == 'GT':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('>', expression1, expression2)
            elif opcode == 'LT':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('<', expression1, expression2)
            elif opcode == 'GTE':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('>=', expression1, expression2)
            elif opcode == 'ADD':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.add(expression1, expression2)
            elif opcode == 'SUB':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.sub(expression1, expression2)
            elif opcode == 'MUL':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.mul(expression1, expression2)
            elif opcode == 'DIV':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.sdiv(expression1, expression2)
            elif opcode == 'MOD':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.srem(expression1, expression2)
            elif opcode == 'LTE':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('<=', expression1, expression2)
            elif opcode == 'EQ':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('==', expression1, expression2)
            elif opcode == 'NEQ':
                expression1 = self.compile_instruction(func, inst[1], builder)
                expression2 = self.compile_instruction(func, inst[2], builder)
                return builder.icmp_signed('!=', expression1, expression2)
            elif opcode == 'IF':
                if_cond = self.compile_instruction(func, inst[1], builder)
                
                if len(inst) > 3:  # There is an else or else if branch
                    else_inst = inst[3]
                    else_opcode = else_inst[0]
                    if else_opcode == 'ELSE':
                        with builder.if_else(if_cond):
                            with then:
                                for inst2 in inst[2][1]:
                                    self.compile_instruction(func, inst2, builder)
                            with otherwise:
                                for inst2 in else_inst[1][1]:
                                    self.compile_instruction(func, inst2, builder)
                    elif else_opcode == 'ELIF':
                        pass # TODO: like actually make this
                else:
                    with builder.if_then(if_cond):
                        for inst2 in inst[2][1]:
                            self.compile_instruction(func, inst2, builder)
            elif opcode == 'CALL':
                callee_func = self.module.get_global(inst[1])
                args = []
                for arg in inst[2]:
                    if arg:
                        args.append(self.compile_instruction(
                            func, arg, builder))
                return builder.call(callee_func, args)
            elif opcode == 'ASSIGN':
                value = self.compile_instruction(func, inst[2], builder)
                index = func.local_variables[inst[1]]
                return builder.store(value, index)
            elif opcode == 'RETURN':
                if inst[1] != 'void':
                    value = self.compile_instruction(func, inst[1], builder)
                    return builder.ret(value)
                else:
                    return builder.ret_void()
            elif opcode == 'WHILE':
                cond_block = func.llvm_function.append_basic_block(
                    'while.cond')
                loop_block = func.llvm_function.append_basic_block(
                    'while.loop')
                end_block = func.llvm_function.append_basic_block('while.end')

                builder.branch(cond_block)

                builder.position_at_end(cond_block)
                while_cond = self.compile_instruction(func, inst[1], builder)
                builder.cbranch(while_cond, loop_block, end_block)

                builder.position_at_end(loop_block)
                for inst2 in inst[2][1]:
                    self.compile_instruction(func, inst2, builder)
                builder.branch(cond_block)

                builder.position_at_end(end_block)

            # Add more opcode handling cases here, similar to the previous implementation
            # but using the ir.Builder methods instead of string-based instructions

            else:
                raise Exception(f'Unknown opcode \'{opcode}\': "{inst}"')

        elif isinstance(inst, str):
            inst += '\0'
            self.stringc += 1
            string_constant = ir.Constant(ir.ArrayType(
                llvm_types['char'], len(inst)), bytearray(inst.encode("utf-8")))
            string_global = ir.GlobalVariable(
                self.module, string_constant.type, name=f".str{self.stringc}")
            string_global.global_constant = True
            string_global.initializer = string_constant
            return builder.gep(string_global, [llvm_types['int'](0), llvm_types['int'](0)])

        elif isinstance(inst, bool):
            return llvm_types['bool'](int(inst))

        elif isinstance(inst, list):
            # Implement array handling using ir.Builder methods
            pass
        else:
            for pytype, lltype in py_to_llvm_types.items():
                if isinstance(inst, pytype):
                    return lltype(inst)
            raise Exception("unexpected type")
            # return llvm_types['int'](inst)

    def compile_code(self, src: str, module: ir.Module = None):
        if module is not None:
            self.module = module

        if not 'printf' in self.llvm_functions:
            func_type = ir.FunctionType(
                llvm_types['int'], [ir.IntType(8).as_pointer()], True)
            llvm_func = ir.Function(self.module, func_type, name='printf')
            self.llvm_functions['printf'] = llvm_func

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

    def compile(self, *files, output, asm=False):
        fail = False
        hi = 0
        if os.path.exists('build'):
            for f in os.listdir('build'):
                os.remove('build/' + f)
            os.removedirs('build')
        os.makedirs('build')
        _files = files
        try:
            for file in _files:
                hi += 1
                print(
                    f'{colorama.Fore.YELLOW}Compiling {file} ({hi}/{len(_files)}){colorama.Fore.RESET}', end='', flush=True)
                with open(file, 'r') as f:
                    self.create_module(hi)
                    hi2 = self.compile_code(f.read())
                    compiled = str(hi2)
                    print(
                        f'\r{colorama.Fore.LIGHTGREEN_EX}Saving {file} ({hi}/{len(_files)}){colorama.Fore.RESET}', end='', flush=True)

                    with open('build/' + file.replace('/', '.') + '.ll', 'w', encoding='utf-8') as f:
                        f.write(compiled)

                print(
                    f'\r{colorama.Fore.GREEN}Compiled {file} ({hi}/{len(_files)}) {colorama.Fore.RESET}')
        except Exception as e:
            print(
                f'\r{colorama.Fore.RED}Failed to compile {file} ({hi}/{len(_files)}) {colorama.Fore.RESET}')
            traceback.print_exc()
            fail = True

        if asm:
            subprocess.run(['llvm-link', *['build/' + file.replace('/', '.') +
                           '.ll' for file in _files], '-o', 'build/output.ll.bc'], check=True)
            subprocess.run(['llvm-dis', 'build/output.ll.bc',
                           '-o', output], check=True)

        else:
            subprocess.run(['clang', *['build/' + file.replace('/', '.') +
                           '.ll' for file in _files], '-o', output], check=True)

        for f in os.listdir('build'):
            os.remove('build/' + f)

        return fail


def main(*sources, output, asm=False):
    compiled = KPiler().compile(*sources, asm=asm, output=output)
    if not compiled:
        print(f'{colorama.Fore.GREEN}Compiled successfully{colorama.Fore.RESET}')
    else:
        print(f'{colorama.Fore.RED}Compiled unsuccessfully{colorama.Fore.RESET}')
    return str(compiled)

def make_module(source):
    return KPiler().compile_code(source)


if __name__ == '__main__':
    src = input("Source file: ")
    with open(src, 'r') as f:
        with open(src + '.ll', 'w') as f2:
            f2.write(KPiler().compile_code(f.read()))
