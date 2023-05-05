import os
import subprocess
import sys

"""
this doesnt work yet to compile use

clang -dumpmachine # to get the device triplet
llc -filetype=asm --mtriple=<your-target-triple> output.ll
gcc -c output.s -o output.o
gcc output.o -o output

"""

def main(input_file: str, output_file: str):
    # Find the target triple
    target_triple = subprocess.check_output(["clang", "-dumpmachine"]).decode().strip()

    # Compile LLVM IR to assembly
    asm_file = "output.s"
    print('Running:', ' '.join(["llc", "-filetype=asm", f"--mtriple={target_triple}", input_file]))
    subprocess.run(["llc", "-filetype=asm", f"--mtriple={target_triple}", input_file], check=True)

    # Assemble the assembly file
    obj_file = "output.o"
    subprocess.run(["clang", "-c", asm_file, "-o", obj_file], check=True)

    # Link the object file to create the binary
    subprocess.run(["clang", obj_file, "-o", output_file], check=True)

    # Clean up temporary files
    os.remove(asm_file)
    os.remove(obj_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)

