int hi() {
    return 5;
}

int main() {
    printf("looping\n");
    int hello = 0;
    hi();
    while (hello < 15) {
        hello++;
        printf("hello: %d\n", hello);
    }
    return 0;
}