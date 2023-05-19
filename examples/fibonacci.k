int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }
    return fibonacci(index - 1) + fibonacci(index - 2);
}


void main() {
    int hi = 6; # fib numbers
    printf("fib: %d\n", fibonacci(hi));
    printf("finish\n");
    return;
}