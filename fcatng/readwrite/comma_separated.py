# -*- coding: utf-8 -*-
"""Reading many-valued contexts from comma-separated text files"""

import csv
import fcatng

def read_mv_csv(path):
    """Read many-valued context from path, which is comma-separated text file

    Format
    ======

    First line consists of comma-separated attribute names.
    Then comma-separated values, each line corresponds to one object.
    The first value in each line is an object name.

    Examples
    ========

    Load example file from tests directory

    >>> c = read_mv_csv('tests/table.csv')
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
        rdr = csv.reader(input_file, delimiter=",")
        
        objects = []

        try:
            rec = next(rdr) # read attributes names
        except StopIteration:
            return fcatng.ManyValuedContext([], [], [])

        attributes = []
        for attr in rec:
            attributes.append(str(attr).strip())

        table = []
        for rec in rdr:
            if not rec: continue
            objects.append(str(rec[0]).strip())
            line = []
            for val in rec[1:]:
                line.append(val)
            table.append(line)

    return fcatng.ManyValuedContext(table, objects, attributes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    

