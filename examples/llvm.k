import "examples/fibonacci.k";

int rand();

int main() {
    int hello = rand() % 10;
    printf("hello: %d\n", hello);
    hello = fibonacci(hello);
    printf("hello: %d\n", hello);
    return 0;
}