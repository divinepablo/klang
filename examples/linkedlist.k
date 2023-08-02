struct Node;

struct Node {
    int data;
    void* next;
}

struct LinkedList {
    void* head;
}

int main() {
    Node head;
    head->data = 256;
    Node next;
    next->data = 345;
    head->next = &next;
    printf("%p\n", &head);
    printf("%p\n", head->next);
    printf("%p\n", next);
    printf("%d\n", head->data);
    printf("%d\n", head->next->data);
    return 0;
}