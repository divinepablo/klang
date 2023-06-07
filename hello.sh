# read -p "What files do you want to emit llvm ir: " files

source .venv/bin/activate
python3 src/klang.py -S -o ignored/output -c $@