import sys, kpiler, kterpret, argparse, klinker, kpilerllvm
parser = argparse.ArgumentParser(prog='klang', description='Basic operations for the k language')
parser.add_argument('filename')
parser.add_argument('-c', '--compile', action='store_true', required=False)
parser.add_argument('-l', '--link', action='store_true', required=False)
parser.add_argument('-r', '--run', action='store_true', required=False)
parser.add_argument('-o', '--output', default=None, required=False, action='store')
args = parser.parse_args()
print(args)
if args.compile and args.link:
    out_file = args.output
    if args.output is None:
        out_file = args.filename[:-2] + '.ll'
    with open(args.filename, 'r') as f:
        output = kpilerllvm.main(f.read())
        with open(out_file, 'w') as f:
            print(f'Outputting to {out_file}')
            f.write(output)
elif args.compile:
    out_file = args.output
    if args.output is None:
        out_file = args.filename[:-2] + '.kasm'
    with open(args.filename, 'r') as f:
        output = kpiler.main(f.read())
        with open(out_file, 'w') as f:
            print(f'Outputting to {out_file}')
            f.write(output)
elif args.run:
    with open(args.filename, 'r') as f:
        kterpret.main(f.read())
elif args.link:
    out_file = args.output
    if args.output is None:
        out_file = args.filename[:-2]
    with open(args.filename, 'r') as f:
        klinker.main(f.read(), out_file)
else:
    parser.print_help()
