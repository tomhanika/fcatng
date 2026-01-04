# -*- coding: utf-8 -*-
"""Holds function that read context from tab separated txt file"""

import csv
import fcatng

def read_txt(path):
    """Read context from path, which is tab separated txt file

    Format
    ======

    First line is tab separated attributes' names
    Next an empty line
    Then tab separated 1 and 0, each line corresponds to one object.

    Examples
    ========

    Load example file from tests directory

    >>> c = read_txt('tests/context.txt')
    >>> len(c)
    4
    >>> len(c[0])
    4
    >>> for o in c:
    ...     print o
    ...
    [True, False, False, True]
    [True, False, True, False]
    [False, True, True, False]
    [False, True, True, True]
    >>> print c.objects
    ['g1', 'g2', 'g3', 'g4']
    >>> print c.attributes
    ['a', 'b', 'c', 'd']

    """
    with open(path, "r", newline='', encoding='utf-8') as input_file:
        rdr = csv.reader(input_file, delimiter="\t")
        rec = next(rdr) # read attributes names

        attributes = []
        for attr in rec:
            attributes.append(str(attr).strip())

        try:
            next(rdr) # empty line
        except StopIteration:
            pass

        table = []
        for rec in rdr:
            if not rec: continue
            line = []
            for num in rec:
                if num == "0":
                    line.append(False)
                elif num == "1":
                    line.append(True)
            table.append(line)

    # i + 1 ? 
    objects = ["".join(["g", str(i + 1)]) for i in range(len(table))]

    return fcatng.Context(table, objects, attributes)


def read_mv_txt(path):
    """Read many-valued context from path, which is tab separated txt file

    Format
    ======

    First line is tab separated attributes' names
    Next an empty line
    Then tab separated values, each line corresponds to one object.

    Examples
    ========

    Load example file from tests directory

    >>> c = read_mv_txt('tests/table.txt')
    >>> len(c)
    3
    >>> len(c[0])
    3
    >>> for o in c:
    ...     print o
    ...
    ['7', '6', '7']
    ['7', '2', '9']
    ['1', '3', '4']
    >>> print c.objects
    ['obj1', 'obj2', 'obj3']
    >>> print c.attributes
    ['attr1', 'attr2', 'attr3']

    """
    with open(path, "r", newline='', encoding='utf-8') as input_file:
        rdr = csv.reader(input_file, delimiter="\t")
        rec = next(rdr) # read objects names

        objects = []
        for obj in rec:
            objects.append(str(obj).strip())

        rec = next(rdr) # read attributes names

        attributes = []
        for attr in rec:
            attributes.append(str(attr).strip())

        try:
            next(rdr) # empty line
        except StopIteration:
            pass

        table = []
        for rec in rdr:
            if not rec: continue
            line = []
            for num in rec:
                line.append(num)
            table.append(line)

    return fcatng.ManyValuedContext(table, objects, attributes)

def uread_mv_txt(path):
    return read_mv_txt(path)

def write_mv_txt(context, path):
    with open(path, "w", encoding="utf-8") as output_file:

        output_file.write("\t".join(context.objects))
        output_file.write("\n")

        output_file.write("\t".join(context.attributes))
        output_file.write("\n\n")

        for i in range(len(context.objects)):
            output_file.write("\t".join([str(spam) for spam in context[i]]))
            output_file.write("\n")

def uwrite_mv_txt(context, path):
    write_mv_txt(context, path)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    

