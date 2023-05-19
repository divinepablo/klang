"""k language main file"""
import argparse
import kterpret
import kpilerllvm
parser = argparse.ArgumentParser(prog='klang', description='Basic operations for the k language')
parser.add_argument('files', metavar='file', nargs='+', help='input file(s)')
parser.add_argument('-c', '--compile', action='store_true', required=False)
parser.add_argument('-S', '--llvm-asm', action='store_true', required=False)
parser.add_argument('-r', '--run', action='store_true', required=False)
parser.add_argument('-o', '--output', default=None, required=False, action='store')
args = parser.parse_args()

if args.compile:
    out_file = args.output
    if args.output is None:
        raise ValueError('need output')
    OUTPUT = kpilerllvm.main(*args.files, output=out_file, asm=args.llvm_asm)
elif args.run:
    with open(args.files[0], 'r', encoding='utf-8') as f:
        module = kpilerllvm.make_module(f.read())
    kterpret.main(module)
elif args.link:
    out_file = args.output
    if args.output is None:
        out_file = args.filename[:-2]
    with open(args.filename, 'r', encoding='utf-8') as f:
        klinker.main(f.read(), out_file)
else:
    parser.print_help()
