source .venv/bin/activate
python3 src/klang.py -o ignored/output -c examples/llvm.k
echo "output from program:"
./ignored/output
deactivate
rm ./ignored/output