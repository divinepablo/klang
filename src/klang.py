"""k language main file"""
import argparse
import kpiler
import kterpret
import klinker
import kpilerllvm
parser = argparse.ArgumentParser(prog='klang', description='Basic operations for the k language')
parser.add_argument('files', metavar='file', nargs='+', help='input file(s)')
parser.add_argument('-c', '--compile', action='store_true', required=False)
parser.add_argument('-l', '--link', action='store_true', required=False)
parser.add_argument('-r', '--run', action='store_true', required=False)
parser.add_argument('-o', '--output', default=None, required=False, action='store')
args = parser.parse_args()

if args.compile and args.link:
    out_file = args.output
    if args.output is None:
        raise ValueError('need output')
    OUTPUT = kpilerllvm.main(*args.files)
    with open(out_file, 'w', encoding='utf-8') as f:
        print(f'Outputting to {out_file}')
        f.write(OUTPUT)
elif args.compile:
    out_file = args.output
    if args.output is None:
        out_file = args.files[0][:-2] + '.kasm'
    with open(args.filename, 'r', encoding='utf-8') as f:
        OUTPUT = kpiler.main(f.read())
        with open(out_file, 'w', encoding='utf-8') as f:
            print(f'Outputting to {out_file}')
            f.write(OUTPUT)
elif args.run:
    with open(args.filename, 'r', encoding='utf-8') as f:
        kterpret.main(f.read())
elif args.link:
    out_file = args.output
    if args.output is None:
        out_file = args.filename[:-2]
    with open(args.filename, 'r', encoding='utf-8') as f:
        klinker.main(f.read(), out_file)
else:
    parser.print_help()
