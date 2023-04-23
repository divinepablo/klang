import sys, kpiler, kpret
argv = sys.argv
if argv[1] == '--compile' or argv[1] == '-c':
    with open(argv[2], 'r') as f:
        out_file = argv[2][:-2] + '.kasm'
        print(f'Outputting to {out_file}')
        output = kpiler.main(f.read())
        with open(out_file, 'w') as f:
            f.write(output)
elif argv[1] == '--run' or argv[1] == '-r':
    with open(argv[2], 'r') as f:
        kpret.main(f.read())
# print(argv)