# -*- coding: utf-8 -*-
"""
Holds class for context
"""

class Context(object):
    """
    A Formal Context consists of two sets: *objects* and *attributes*
    and of a binary relation between them.

    As a data type we use a bit matrix.

    Examples
    ========

    Create a context.

    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> c[0][0]
    True
    >>> c[0][2]
    False
    >>> 1 in c.objects
    True
    >>> 'f' in c.attributes
    False
    >>> for o in c:
    ...     print o
    ...     break
    ...
    [True, False, False, True]

    Class emulates container type.

    >>> len(c)
    4
    >>> c[1]
    [True, False, True, False]

    Usage of examples.

    >>> c.get_object_intent_by_index(1)
    set(['a', 'c'])
    >>> for ex in c.examples():
    ...     print ex
    ...     break
    ...
    set(['a', 'd'])
    """

    def __init__(self, cross_table, objects, attributes):
        """Create a context from cross table and list of objects, list
        of attributes
        
        cross_table - the list of bool lists
        objects - the list of objects
        attributes - the list of attributes 
        """
        if len(cross_table) != len(objects):
            raise ValueError("Number of objects (=%i) and number of cross table"
                   " rows(=%i) must agree" % (len(objects), len(cross_table)))
        elif (len(cross_table) != 0) and len(cross_table[0]) != len(attributes):
            raise ValueError("Number of attributes (=%i) and number of cross table"
                    " columns (=%i) must agree" % (len(attributes),
                        len(cross_table[0])))

        self._table = cross_table
        self._objects = objects
        self._attributes = attributes

    def get_objects(self):
        return self._objects

    objects = property(get_objects)

    def get_attributes(self):
        return self._attributes

    attributes = property(get_attributes)

    def examples(self):
        """Generator. Generate set of corresponding attributes
        for each row (object) of context
        
        TODO: Is it proper name?
        """
        for obj in self._table:
            attrs_indexes = filter(lambda i: obj[i], range(len(obj)))
            yield set([self.attributes[i] for i in attrs_indexes])

    def get_object_intent_by_index(self, i):
        """Return a set of corresponding attributes for row with index i"""
        # TODO: !!! Very inefficient. Avoid using
        attrs_indexes = filter(lambda j: self._table[i][j],
                range(len(self._table[i])))
        return set([self.attributes[i] for i in attrs_indexes])
    
    def get_object_intent(self, o):
        index = self._objects.index(o)
        return self.get_object_intent_by_index(index)
    
    def get_attribute_extent_by_index(self, j):
        """Return a set of corresponding objects for column with index i"""
        objs_indexes = filter(lambda i: self._table[i][j],
                range(len(self._table)))
        return set([self.objects[i] for i in objs_indexes])
    
    def get_attribute_extent(self, a):
        index = self._attributes.index(a)
        return self.get_attribute_extent_by_index(index)
    
    def add_attribute(self, col, attr_name):
        """Add new attribute to context with given name"""
        for i in range(len(self._objects)):
            self._table[i].append(col[i])
        self._attributes.append(attr_name)

    def add_column(self, col, attr_name):
        """Deprecated. Use add_attribute."""
        print "Deprecated. Use add_attribute."
        self.add_attribute(col, attr_name)

    def add_object(self, row, obj_name):
        """Add new object to context with given name"""
        self._table.append(row)
        self._objects.append(obj_name)
        
    def delete_object(self, obj_index):
        del self._table[obj_index]
        del self._objects[obj_index]
    
    def delete_attribute(self, attr_index):
        for i in range(len(self._objects)):
            del self._table[i][attr_index]
        del self._attributes[attr_index]

    ############################
    # Emulating container type #
    ############################

    def __len__(self):
        return len(self._table)

    def __getitem__(self, key):
        return self._table[key]

    ############################

if __name__ == "__main__":
    import doctest
    doctest.testmod()
