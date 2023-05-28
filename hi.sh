# read -p "What files do you want to compile: " files

source .venv/bin/activate
python3 src/klang.py -o ignored/output -c $@
echo "output from program:"
./ignored/output
echo Proccess ended with return code: $? 
deactivate
rm ./ignored/output