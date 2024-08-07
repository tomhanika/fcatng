import concepts as cs
import sys
import os

# Fügen Sie den übergeordneten Ordner zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath('..'))

# Jetzt sollte Python in der Lage sein, das Modul fcatng zu finden
from fcatng import context

# Initialise the Variables
ct = [[True, True, True, True],
      [True, False, True, True],
      [False, True, True, True],
      [False, True, True, True],
      [True, False, False, False]]
objs = ['x_1', 'x_2', 'x_3', 'x_4', 'x_5']
attrs = ['y_1', 'y_2', 'y_3', 'y_4']


# Create a Context object
context_inst = context.Context(ct, objs, attrs)


def print_attribute_implications():
    result = context_inst.get_attribute_implications()

    print(result)


def calc_implications():
    attrs = ['a', 'b', 'c', 'd']
    cross_table = [[True, False, False, True],
                   [True, False, True, False],
                   [False, True, True, False],
                   [False, True, True, True]]

    # Attribute finden, die in jeder Zeile wahr sind
    true_attrs_in_rows = [frozenset(attr for attr, val in zip(attrs, row) if val) for row in cross_table]

    # Implikationen finden
    implications = set()
    for i, true_attrs_i in enumerate(true_attrs_in_rows):
        for j, true_attrs_j in enumerate(true_attrs_in_rows):
            if i != j and true_attrs_i.issubset(true_attrs_j):
                implications.add((true_attrs_i, true_attrs_j - true_attrs_i))

    # Implikationen printen
    for premise, conclusion in implications:
        print(f"{set(premise)} => {set(conclusion)}")


def calc_implications_other():
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']
    cross_table = [[True, False, False, True],
                   [True, False, True, False],
                   [False, True, True, False],
                   [False, True, True, True]]

    # Attribute finden, die für jedes Objekt wahr sind
    true_attrs_in_objs = {obj: set(attr for attr, val in zip(attrs, row) if val) for obj, row in zip(objs, cross_table)}

    # Implikationen finden
    implications = set()
    for obj_i, true_attrs_i in true_attrs_in_objs.items():
        for obj_j, true_attrs_j in true_attrs_in_objs.items():
            if obj_i != obj_j and true_attrs_i.issubset(true_attrs_j):
                implications.add((obj_i, obj_j))

    # Implikationen printen
    for premise, conclusion in implications:
        print(f"Objekt {premise} => Objekt {conclusion}")


def calc_implications_conc_lib():

    # Objekte und Attribute definieren
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']

    # Kreuztabelle definieren
    cross_table = [[True, False, False, True],
                   [True, False, True, False],
                   [False, True, True, False],
                   [False, True, True, True]]

    # Kontext erstellen
    c = cs.Context(objs, attrs,
                   [(obj, attr) for obj, row in zip(objs, cross_table) for attr, val in zip(attrs, row) if val])

    # Implikationen berechnen
    implications = c.lattice.implications

    # Implikationen drucken
    for implication in implications:
        print(f"{implication[0]} => {implication[1]}")


if __name__ == "__main__":
    calc_implications()
    calc_implications_other()
