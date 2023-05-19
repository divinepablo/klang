int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }
    return fibonacci(index - 1) + fibonacci(index - 2);
}

int rand();

int main() {
    int hello = rand() % 10;
    printf("hello: %d\n", hello);
    hello = fibonacci(hello);
    printf("hello: %d\n", hello);
    return 0;
}