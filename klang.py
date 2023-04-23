import sys, kpiler, kterpret, argparse
parser = argparse.ArgumentParser(prog='klang', description='Basic operations for the k language')
parser.add_argument('filename')
parser.add_argument('-c', '--compile', action='store_true', required=False)
parser.add_argument('-r', '--run', action='store_true', required=False)
parser.add_argument('-o', '--output', default=None, required=False, action='store')
args = parser.parse_args()

if args.compile:
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
else:
    parser.print_help()