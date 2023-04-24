void main() {
    int sir = 0;
    sir = sir + 5;
    sir = sir + 5;
    print(sir);
    print(30 + 10);
    sir += 15;
    sir++;
    print(sir);
    int sub = sir - 5;
    int mul = sir * 5;
    int div = sir / 5;
    int mod = sir % 5;
    print(sub);
    print(mul);
    print(div);
    print(mod);
    int ultimate = 0;
    ultimate += sir;
    ultimate *= mul;
    ultimate /= div;
    ultimate -= sub;
    print("ultimate");
    print(ultimate);
}