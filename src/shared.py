from llvmlite import ir

structs: dict[str, ir.BaseStructType] = {}

class LLVMTypeDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        pointer_count = key.count('*')
        base_type_str = key.rstrip('*')

        if base_type_str not in self:
            raise ValueError(f"Invalid base type: {base_type_str}")

        llvm_type = super().__getitem__(base_type_str)

        for _ in range(pointer_count):
            llvm_type = ir.PointerType(llvm_type)

        return llvm_type


llvm_types = LLVMTypeDict({
    'int': ir.IntType(32),
    'float': ir.FloatType(),
    'char': ir.IntType(8),
    'string': ir.PointerType(ir.IntType(8)),
    'bool': ir.IntType(1),
    'void': ir.VoidType(),
    int: ir.IntType(32),
    float: ir.FloatType(),
    chr: ir.IntType(8),
    bool: ir.IntType(1),
})
