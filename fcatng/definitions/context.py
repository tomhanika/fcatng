# -*- coding: utf-8 -*-
"""
Holds class for context
"""
import copy
from typing import List, Any, Optional, Set, Generator, Callable, Dict

import fcatng.algorithms


class Context:
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
    ...     print(o)
    ...     break
    ...
    [True, False, False, True]
    >>> transposed_c = c.transpose()
    >>> for o in transposed_c:
    ...     print(o)
    ...
    [True, True, False, False]
    [False, False, True, True]
    [False, True, True, True]
    [True, False, False, True]

    Class emulates container type.

    >>> len(c)
    4
    >>> c[1]
    [True, False, True, False]

    Usage of examples.

    >>> c.get_object_intent_by_index(1)
    {'a', 'c'}
    >>> for ex in c.examples():
    ...     print(ex)
    ...     break
    ...
    {'a', 'd'}
    
    Implications basis
    
    >>> for imp in c.attribute_implications:
    ...     print(imp)
    ...
    c, d => b
    b => c
    a, c, b => d
    
    >>> for imp in c.object_implications:
    ...     print(imp)
    ...
    3 => 4
    2, 4 => 3
    1, 3, 4 => 2
    """

    def __init__(self, cross_table: List[List[bool]] = [], objects: List[Any] = [], attributes: List[Any] = []):
        """Create a context from cross table and list of objects, list
        of attributes
        
        Args:
            cross_table (List[List[bool]]): the list of bool lists
            objects (List[Any]): the list of objects
            attributes (List[Any]): the list of attributes
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
        
    def __deepcopy__(self, memo) -> 'Context':
        return Context(copy.deepcopy(self._table, memo),
                       self._objects[:],
                       self._attributes[:])

    def get_objects(self) -> List[Any]:
        return self._objects

    objects = property(get_objects)

    def get_attributes(self) -> List[Any]:
        return self._attributes

    attributes = property(get_attributes)
    
    def get_attribute_implications(self, 
                                   basis: Optional[Callable] = None,
                                   confirmed: Optional[List] = None,
                                   cond: Callable[[Any], bool] = lambda x: True) -> List[Any]:
        if basis is None:
            basis = fcatng.algorithms.compute_dg_basis
        if confirmed is None:
            confirmed = []
        return basis(self, imp_basis=confirmed, cond=cond)
        # if not self._attr_imp_basis or (confirmed != self._confirmed):
        #             self._attr_imp_basis = basis(self, imp_basis=confirmed)
        #             self._confirmed = confirmed
        #         return self._attr_imp_basis
    
    _attr_imp_basis = None
    _confirmed = None
    attribute_implications = property(get_attribute_implications)
    
    def get_object_implications(self, 
                                basis: Optional[Callable] = None,
                                confirmed: Optional[List] = None) -> List[Any]:
        if basis is None:
            basis = fcatng.algorithms.compute_dg_basis
        cxt = self.transpose()
        if not self._obj_imp_basis:
            self._obj_imp_basis = basis(cxt, imp_basis=confirmed)
        return self._obj_imp_basis
    
    _obj_imp_basis = None
    object_implications = property(get_object_implications)
        
    def examples(self) -> Generator[Set[Any], None, None]:
        """Generator. Generate set of corresponding attributes
        for each row (object) of context
        """
        for obj in self._table:
            attrs_indexes = [i for i in range(len(obj)) if obj[i]]
            yield set([self.attributes[i] for i in attrs_indexes])
            
    def intents(self) -> Generator[Set[Any], None, None]:
        return self.examples()

    def get_object_intent_by_index(self, i: int) -> Set[Any]:
        """Return a set of corresponding attributes for row with index i"""
        # TODO: !!! Very inefficient. Avoid using
        attrs_indexes = [j for j in range(len(self._table[i])) if self._table[i][j]]
        return set([self.attributes[i] for i in attrs_indexes])
    
    def get_object_intent(self, o: Any) -> Set[Any]:
        index = self._objects.index(o)
        return self.get_object_intent_by_index(index)
    
    def get_attribute_extent_by_index(self, j: int) -> Set[Any]:
        """Return a set of corresponding objects for column with index i"""
        objs_indexes = [i for i in range(len(self._table)) if self._table[i][j]]
        return set([self.objects[i] for i in objs_indexes])
    
    def get_attribute_extent(self, a: Any) -> Set[Any]:
        index = self._attributes.index(a)
        return self.get_attribute_extent_by_index(index)
        
    def get_value(self, o: Any, a: Any) -> bool:
        io = self.objects.index(o)
        ia = self.attributes.index(a)
        return self[io][ia]
    
    def add_attribute(self, col: List[bool], attr_name: Any):
        """Add new attribute to context with given name"""
        for i in range(len(self._objects)):
            self._table[i].append(col[i])
        self._attributes.append(attr_name)

    def add_column(self, col: List[bool], attr_name: Any):
        """Deprecated. Use add_attribute."""
        print("Deprecated. Use add_attribute.")
        self.add_attribute(col, attr_name)

    def add_object(self, row: List[bool], obj_name: Any):
        """Add new object to context with given name"""
        self._table.append(row)
        self._objects.append(obj_name)
        
    def add_object_with_intent(self, intent: Set[Any], obj_name: Any):
        self._attr_imp_basis = None
        self._objects.append(obj_name)
        row = [(attr in intent) for attr in self._attributes]
        self._table.append(row)
        
    def add_attribute_with_extent(self, extent: Set[Any], attr_name: Any):
        col = [(obj in extent) for obj in self._objects]
        self.add_attribute(col, attr_name)
        
    def set_attribute_extent(self, extent: Set[Any], name: Any):
        attr_index = self._attributes.index(name)
        for i in range(len(self._objects)):
            self._table[i][attr_index] = (self._objects[i] in extent)
            
    def set_object_intent(self, intent: Set[Any], name: Any):
        obj_index = self._objects.index(name)
        for i in range(len(self._attributes)):
            self._table[obj_index][i] = (self._attributes[i] in intent)
        
    def delete_object(self, obj_index: int):
        del self._table[obj_index]
        del self._objects[obj_index]
        
    def delete_object_by_name(self, obj_name: Any):
        self.delete_object(self.objects.index(obj_name))
    
    def delete_attribute(self, attr_index: int):
        for i in range(len(self._objects)):
            del self._table[i][attr_index]
        del self._attributes[attr_index]
        
    def delete_attribute_by_name(self, attr_name: Any):
        self.delete_attribute(self.attributes.index(attr_name))
        
    def rename_object(self, old_name: Any, name: Any):
        self._objects[self._objects.index(old_name)] = name
        
    def rename_attribute(self, old_name: Any, name: Any):
        self._attributes[self._attributes.index(old_name)] = name
        
    def transpose(self) -> 'Context':
        """Return new context with transposed cross-table"""
        new_objects = self._attributes[:]
        new_attributes = self._objects[:]
        new_cross_table = []
        for j in range(len(self._attributes)):
            line = []
            for i in range(len(self._objects)):
                line.append(self._table[i][j])
            new_cross_table.append(line)
        return Context(new_cross_table, new_objects, new_attributes)
        
    def extract_subcontext_filtered_by_attributes(self, attributes_names: List[Any],
                                                    mode: str = "and") -> 'Context':
        """Create a subcontext with such objects that have given attributes"""
        values = dict( [(attribute, True) for attribute in attributes_names] )
        object_names, subtable = \
                            self._extract_subtable_by_attribute_values(values, mode)
        return Context(subtable,
                       object_names,
                       self.attributes)
                            
    def extract_subcontext(self, attribute_names: List[Any]) -> 'Context':
        """Create a subcontext with only indicated attributes"""
        return Context(self._extract_subtable(attribute_names),
                       self.objects,
                       attribute_names)
                                
    def _extract_subtable(self, attribute_names: List[Any]) -> List[List[bool]]:
        self._check_attribute_names(attribute_names)
        attribute_indices = [self.attributes.index(a) for a in attribute_names] 
        table = []
        for i in range(len(self)):
            row = []
            for j in attribute_indices:
                row.append(self[i][j])
            table.append(row)
        
        return table
        
    def _extract_subtable_by_condition(self, condition: Callable[[int], bool]):
        """Extract a subtable containing only rows that satisfy the condition.
        Return a list of object names and a subtable.
        
        Keyword arguments:
        condition(object_index) -- a function that takes an an object index and
            returns a Boolean value
        
        """
        indices = [i for i in range(len(self)) if condition(i)]
        return ([self.objects[i] for i in indices],
                [self._table[i] for i in indices])
                
    def _extract_subtable_by_attribute_values(self, values: Dict[Any, Any],
                                                    mode: str = "and"):
        """Extract a subtable containing only rows with certain column values.
        Return a list of object names and a subtable.
        
        Keyword arguments:
        values -- an attribute-value dictionary
        
        """
        self._check_attribute_names(list(values.keys()))
        if mode == "and":
            indices = [i for i in range(len(self)) if self._has_values(i, values)]
        elif mode == "or":
            indices = [i for i in range(len(self)) if self._has_at_least_one_value(i, values)]
        return ([self.objects[i] for i in indices],
                [self._table[i] for i in indices])
                
    def _has_values(self, i: int, values: Dict[Any, Any]) -> bool:
        """Test if ith object has attribute values as indicated.
        
        Keyword arguments:
        i -- an object index
        values -- an attribute-value dictionary
        
        """
        for a in values:
            j = self.attributes.index(a)
            v = values[a]
            if self[i][j] != v:
                return False
        return True
        
    def _has_at_least_one_value(self, i: int, values: Dict[Any, Any]) -> bool:
        """Test if ith object has at least one attribute value as in values.
                
        Keyword arguments:
        i -- an object index
        values -- an attribute-value dictionary
        
        """
        for a in values:
            j = self.attributes.index(a)
            v = values[a]
            if self[i][j] == v:
                return True
        return False
            
    def _check_attribute_names(self, attribute_names: List[Any]):
        if not set(attribute_names) <= set(self.attributes):
            wrong_attributes = ""
            for a in set(attribute_names) - set(self.attributes):
                wrong_attributes += "\t%s\n" % a
            raise ValueError("Wrong attribute names:\n%s" % wrong_attributes)    

    ############################
    # Emulating container type #
    ############################

    def __len__(self) -> int:
        return len(self._table)

    def __getitem__(self, key: int) -> List[bool]:
        return self._table[key]

    ############################
    
    def __repr__(self) -> str:
        output = ", ".join(self.attributes) + "\n"
        output += ", ".join(self.objects) + "\n"
        cross = {True : "X", False : "."}
        for i in range(len(self.objects)):
            output += ("".join([cross[b] for b in self[i]])) + "\n"
        return output

if __name__ == "__main__":
    import doctest
    doctest.testmod()
