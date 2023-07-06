from llvmlite import ir

structs_dict: dict[ir.LiteralStructType, dict] = {}
ctx = ir.global_context

class LLVMTypeDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        pointer_count = key.count('*')
        base_type_str = key.rstrip('*')

        if base_type_str not in self:
            struct_name = f'struct.{base_type_str}'
            if struct_name not in ctx.identified_types:
                raise ValueError(f"Invalid base type: {base_type_str}")
            llvm_type = ctx.get_identified_type(struct_name)
        else:
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
    'void': ir.PointerType(ir.IntType(8)),
    int: ir.IntType(32),
    float: ir.FloatType(),
    chr: ir.IntType(8),
    bool: ir.IntType(1),
})
