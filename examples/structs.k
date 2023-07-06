struct Hello {
    int hello;
    bool zippo;
}

int main() {
    Hello hello;
    hello->hello = 5;
    hello->zippo = true;
    printf("%p\n", hello.hello);
    printf("%d\n", hello->hello);
    printf("%d\n", hello.zippo);
    return 0;
}