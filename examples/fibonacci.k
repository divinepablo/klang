int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }
    return fibonacci(index - 1) + fibonacci(index - 2);
}


void main() {
    int hi = 50; # fib numbers
    print(fibonacci(hi));
    print("finish");
}