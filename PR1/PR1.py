def custom_zip(*iterables):
    iterators = [iter(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            try:
                result.append(next(it))
            except StopIteration:
                return
        yield tuple(result)

# ������� ������������
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [True, False, None]

for item in custom_zip(list1, list2, list3):
    print(item)

# �������� ������ �������
list4 = [10, 20, 30, 40]
list5 = ['x', 'y']

print(list(custom_zip(list4, list5)))  # ���������� ���������: [(10, 'x'), (20, 'y')]