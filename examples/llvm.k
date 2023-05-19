int fibonacci(int index) {
    if (index <= 1) {
        return index;
    }
    return hi(index - 1) + hi(index - 2);
}

int main() {
    printf("looping\n");
    int hello = 0;
    while (hello < 15) {
        hello++;
        printf("hello: %d\n", hello);
    }
    hello = hi(15);
    printf("%d\n", hello);
    return 0;
}