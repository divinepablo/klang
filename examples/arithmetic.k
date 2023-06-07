int main() {
    int sir = 0;
    sir = sir + 5;
    sir = sir + 5;
    printf("%d\n", sir);
    printf("%d\n", 30 + 10);
    sir += 15;
    sir++;
    printf("%d\n", sir);
    int sub = sir - 5;
    int mul = sir * 5;
    int div = sir / 5;
    int mod = sir % 5;
    printf("%d\n", sub);
    printf("%d\n", mul);
    printf("%d\n", div);
    printf("%d\n", mod);
    int ultimate = 0;
    ultimate += sir;
    ultimate *= mul;
    ultimate /= div;
    ultimate -= sub;
    printf("ultimate\n");
    printf("%d\n", ultimate);
    return 0;
}