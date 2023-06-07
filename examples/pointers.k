void hi(int* variable) {
    printf("address: %p\n", variable);
    int** ppVariable = &variable;
    printf("address: %p\n", ppVariable);
    printf("value: %d\n", *variable);
    *variable = 5;
    printf("value: %d\n", **ppVariable);
    return;
}

int main() {
    int hello = 53;
    printf("hello: %d\n", hello);
    hi(&hello);
    printf("hello: %d\n", hello);
    return 0; # return code
}