from llvmlite import ir # should probably be renamed to kjit.py but now not the time
from llvmlite import binding as llvm
import ctypes

class Interpreter:
    def interpret(self, module):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create a target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()

        backing_mod = llvm.parse_assembly("")

        # Create an execution engine
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

        # Add the module to the execution engine
        mod = llvm.parse_assembly(str(module))
        mod.verify()
        # Now add the module and make sure it is ready for execution
        engine.add_module(mod)
        engine.finalize_object()
        engine.run_static_constructors()

        # Finalize the engine
        engine.finalize_object()

        # Get a pointer to the 'foo' function
        func_ptr = engine.get_function_address("main")

        # Cast the function pointer to a callable Python function
        main_func = ctypes.CFUNCTYPE(ctypes.c_int)(func_ptr)

        # Now you can call the function directly from Python
        print(f"Returned: {main_func()}")  # prints 123

def main(module):
    interpreter = Interpreter()
    interpreter.interpret(module)
