int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }asd
    return fibonacci(index - 1) + fibonacci(index - 2);
}

int main() {
    printf("looping\n");
    int hello = 0;
    while (hello < 15) {
        hello++;
        printf("hello: %d\n", hello);
    }
    hello = fibonacci(15);
    printf("%d\n", hello);
    return 0;
}