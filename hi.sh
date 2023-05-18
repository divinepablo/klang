source .venv/bin/activate
python3 src/klang.py -o examples/hellohi.ll -cl examples/llvm.k
echo "output from lli:"
lli examples/hellohi.ll
deactivate
