def calc_implications():
    attrs = ['a', 'b', 'c', 'd']
    cross_table = [[True, False, False, True],
                   [True, False, True, False],
                   [False, True, True, False],
                   [False, True, True, True]]

    # Finden Sie die Attribute, die in jeder Zeile wahr sind
    true_attrs_in_rows = [frozenset(attr for attr, val in zip(attrs, row) if val) for row in cross_table]

    # Finden Sie die Implikationen
    implications = set()
    for i, true_attrs_i in enumerate(true_attrs_in_rows):
        for j, true_attrs_j in enumerate(true_attrs_in_rows):
            if i != j and true_attrs_i.issubset(true_attrs_j):
                implications.add((true_attrs_i, true_attrs_j - true_attrs_i))

    # Drucken Sie die Implikationen
    for premise, conclusion in implications:
        print(f"{set(premise)} => {set(conclusion)}")


if __name__ == "__main__":
    calc_implications()
