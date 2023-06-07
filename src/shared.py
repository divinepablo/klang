from llvmlite import ir

structs: dict[str, ir.BaseStructType] = {}

llvm_types = {
    'int': ir.IntType(32),
    'float': ir.FloatType(),
    'char': ir.IntType(8),
    'bool': ir.IntType(1),
    
    'int[]': lambda count: ir.ArrayType(ir.IntType(32), count),
    'float[]': lambda count: ir.ArrayType(ir.FloatType(), count),
    'char[]': lambda count: ir.ArrayType(ir.IntType(8), count),
    'bool[]': lambda count: ir.ArrayType(ir.IntType(1), count),
    
    
    'int*': ir.IntType(32).as_pointer(),
    'float*': ir.FloatType().as_pointer(),
    'char*': ir.IntType(8).as_pointer(),
    'bool*': ir.IntType(1).as_pointer(),
    'void*': ir.VoidType().as_pointer(),

    'void': ir.VoidType()
}

py_to_llvm_types = {
    int: ir.IntType(32),
    float: ir.FloatType(),
    chr: ir.IntType(8),
    bool: ir.IntType(1),
}