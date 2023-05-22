int fibonacci(int index) {
    if (index <= 1) {
        printf("Index less than or equal to 1: %d\n", index);
        return index;
    }
    int hello = fibonacci(index - 1) + fibonacci(index - 2);
    printf("Returning: %d\n", hello);
    return hello;
}