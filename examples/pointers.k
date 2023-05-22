void hi(int* variable) {
    printf("addres: %p\n", variable);
    printf("addres: %d\n", *variable);
    return;
}

int main() {
    int hello = 53;
    printf("hello: %d\n", hello);
    hi(&hello);
    printf("hello: %d\n", hello);
    return 0; # return code
}