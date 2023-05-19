int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }
    return fibonacci(index - 1) + fibonacci(index - 2);
}

int rand();

int main() {
    printf("looping\n");
    int hello = 0;
    while (hello < 15) {
        hello++;
        printf("hello: %d\n", hello);
    }
    hello = fibonacci(15);
    printf("%d\n", hello);
    printf("%d\n", rand());
    return 0;
}