int fibonacci(int hi) {
    int a = 1;
    int b = 0;
    int i = 0;
    while (i < hi) {
        int c = b;
        b = a;
        a = c + b;
        i++;
    }
    
    print(a);
}

void main() {
    int hi = 50; # fib numbers
    print(fibonacci(hi));
    print("finish");
}