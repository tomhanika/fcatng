# -*- coding: utf-8 -*-
"""Holds a function that scale a many-valued context to "one-valued" context"""

import fcatng

def scale_mvcontext(mvcontext, scales):
    """Scale many-valued context to one-valued. 
    Return fcatng.Context
    
    scales is a list of the scales(fcatng.Scale) applied
    to current many-valued context. Number of the scales
    in the list must agree with number of attributes in 
    many-valued context.
    
    Example
    =======
    
    >>> s = fcatng.read_cxt("tests/scale.cxt")
    >>> mvc = fcatng.read_mv_txt("../readwrite/tests/table.txt")
    >>> for o in mvc:
    ...     print o
    ...
    ['7', '6', '7']
    ['7', '2', '9']
    ['1', '3', '4']
    >>> c = scale_mvcontext(mvc, [s]*len(mvc.attributes))
    >>> for o in c:
    ...     print o
    ...
    [True, False, True, False, True, False]
    [True, False, False, False, True, False]
    [False, True, False, False, False, False]
    >>> print c.attributes
    ['attr1>5', 'attr1==1', 'attr2>5', 'attr2==1', 'attr3>5', 'attr3==1']
    >>> print c.objects
    ['g1', 'g2', 'g3']
    
    """
    derived_context = fcatng.Context([[] for i in range(len(mvcontext.objects))],
                                   mvcontext.objects, [])
    for attr_index in range(len(mvcontext.attributes)):
        scale = scales[attr_index]
        for col in range(len(scale.attributes)):
            derived_attr = [False for i in range(len(mvcontext.objects))]
            for row in range(len(scale.objects)):
                for obj in range(len(mvcontext.objects)):
                    if derived_attr[obj]:
                        continue
                    else:
                        try:
                            value = float(mvcontext[obj][attr_index])
                        except:
                            value = str(mvcontext[obj][attr_index])
                        if eval(scale.objects[row], {"value" : value}):
                            derived_attr[obj] = scale[row][col]
            new_attribute_name = ":".join([mvcontext.attributes[attr_index],
                                                  scale.attributes[col]])
            derived_context.add_column(derived_attr, new_attribute_name)                                    
    return derived_context
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
