from fcatng import ConceptSystem

# import separation
# import probability
# import stability

def compute_index(lattice, function, name):
    indexes = function(lattice)
    
    for concept in indexes.items():
        if concept[0].meta:
            concept[0].meta[name] = concept[1]
        else: 
            concept[0].meta = {name : concept[1]}

def filter_concepts(lattice, function, mode, opt=1):
    """Return new concept system, filtered by function according to the mode.
    
    Modes:
    --- "part" - part of initial concept lattice
    --- "abs" - absolute value of the concepts in resulting concept system
    --- "value" - value of the index
    
    Additionaly add attribute, containing inforamtion about indexes, to the new lattice
    """
    def _filter_value(lattice, indexes, value):
        filtered_concepts = [item for item in indexes.items() if item[1]>=value]
        return ConceptSystem([c[0] for c in filtered_concepts])
    
    def _filter_abs(lattice, indexes, n):
        cmp_ = lambda x,y: cmp(x[1], y[1])
        sorted_indexes = sorted(indexes.items(), cmp_, reverse=True)
        filtered_concepts = sorted_indexes[:int(n)]
            
        return ConceptSystem([c[0] for c in filtered_concepts])
    
    def _filter_part(lattice, indexes, part):
        n = int(len(lattice) * part)
        cmp_ = lambda x,y: cmp(x[1], y[1])
        sorted_indexes = sorted(indexes.items(), cmp_, reverse=True)
        filtered_concepts = sorted_indexes[:n]
        
        values = sorted_indexes
        eps = values[n-2][1]-values[n-1][1]
        
        other_concepts = sorted_indexes[n:]
        for concept in other_concepts:
            if abs(concept[1] - values[n][1]) < eps:
                filtered_concepts.append(concept)
            
        return ConceptSystem([c[0] for c in filtered_concepts])
    
    indexes = function(lattice)
    if indexes:
        if mode == "part":
            ret = _filter_part(lattice, indexes, opt)
        elif mode == "abs":
            ret = _filter_abs(lattice, indexes, opt)
        elif mode == "value":
            ret = _filter_value(lattice, indexes, opt)
    return ret

def compute_extent_size(lattice):
    number_of_objects = len(lattice.context.objects)
    extent_size_index = {}
    
    for c in lattice:
        extent_size_index[c] = len(c.extent) / number_of_objects
            
    return extent_size_index

def compute_intent_size(lattice):
    number_of_attributes = len(lattice.context.attributes)
    intent_size_index = {}
    
    for c in lattice:
        intent_size_index[c] = len(c.intent) / number_of_attributes
            
    return intent_size_index

from math import exp, log

def compute_probability(lattice):
    
    def get_intent_probability(B, p_m, n):
        ans = 0
        log_p_B = log_subset_probability(B, p_m)
        p_B = exp(log_p_B)
        if len(B) == 0:
            p_B = 1
            log_p_B = 0
        
        not_B = set()
        for attr in list(p_m.keys()):
            if not attr in B:
                not_B.add(attr)
        for k in range(n + 1):
            mult = 0
            mult_is_zero = False
            for attr in not_B:
                try:
                    mult += log(1 - ((p_m[attr]) ** k))
                except:
                    mult_is_zero = True
                    break
            if mult_is_zero:
                continue
            try:
                if p_B == 1 and n == k:
                    return exp(mult)
                else:
                    t = k * log_p_B + (n - k) * log((1 - p_B)) + mult
                    t = exp(t)
                    # print k, t
            except:
                t = 0
            nom = list(range(n - k + 1, n + 1))
            den = list(range(1, k + 1))
            if len(den) != len(nom):
                print("False")
            for i in range(len(nom)):
                t *= nom[i] / float(den[i])
            ans += t
        return ans

    def log_subset_probability(subset, p_m):
        ans = 0
        for attr in subset:
            try:
                ans += log(p_m[attr])
            except:
                pass
        return ans

    context = lattice.context
    n = len(context)
    p_m = {}
    for attr in context.attributes:
        m_ = 0
        for i in range(n):
            o = context.get_object_intent_by_index(i)
            if attr in o:
                m_ += 1
        p_m[attr] = m_ / float(n)
        
    probability = {}
    for concept in lattice:
        probability[concept] = get_intent_probability(concept.intent, p_m, n)
        
    return probability


## Rework to test in test file
# if __name__ == '__main__':
#     # Test code
#     from fcatng import ConceptLattice, Context
    
#     ct = [[True, False, False, True],\
#           [True, False, True, False],\
#           [False, True, True, False],\
#           [False, True, True, True]]
#     objs = [1, 2, 3, 4]
#     attrs = ['a', 'b', 'c', 'd']
#     c = Context(ct, objs, attrs)
#     cs = ConceptLattice(c)
#     ci = compute_probability(cs)
#     print(ci)

def compute_separation_index(lattice):
    context = lattice.context
    cross_index = {}
    
    for c in lattice:
        attrs = c.intent
        objs = c.extent
        square = len(attrs)*len(objs)
        crossed = 0
        for attr in attrs:
            crossed += len(context.get_attribute_extent(attr))
                 
        for obj in objs:
            crossed += len(context.get_object_intent(obj))
        crossed -= square
        if square == 0:
            cross_index[c] = 1.0
        else:
            cross_index[c] = square/crossed
            
    return cross_index


## Rework to testfile 
# if __name__ == '__main__':
#     from fcatng import ConceptLattice, Context
    
#     ct = [[True, False, False, True],\
#           [True, False, True, False],\
#           [False, True, True, False],\
#           [False, True, True, True]]
#     objs = [1, 2, 3, 4]
#     attrs = ['a', 'b', 'c', 'd']
#     c = Context(ct, objs, attrs)
#     cl = ConceptLattice(c)
#     ci = compute_separation_index(cl)
#     print(ci)




from copy import deepcopy

from fcatng import ConceptSystem


def compute_istability(lattice):
    """
    Examples
    ========

    >>> from fcatng import Context, ConceptLattice
    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> cl = ConceptLattice(c)
    >>> st = compute_estability(cl)
    >>> print st

    """
    concepts = ConceptSystem(lattice)
    count = {}
    subsets = {}
    stability = {}

    for concept in concepts:
        count[concept] = len([c for c in concepts if c.extent < concept.extent])
        subsets[concept] = 2 ** len(concept.extent)

    bottom_concepts = set([concepts.bottom_concept])
    while not len(concepts) == 0:
        bottom_concept = bottom_concepts.pop()
        stability[bottom_concept] = subsets[bottom_concept] / \
            (2 ** len(bottom_concept.extent))
        concepts.remove(bottom_concept)
        for c in concepts:
            if bottom_concept.intent > c.intent:
                subsets[c] -= subsets[bottom_concept]
                count[c] -= 1
                if count[c] == 0:
                    bottom_concepts.add(c)
    return stability


def compute_estability(lattice):
    concepts = ConceptSystem(lattice)
    count = {}
    subsets = {}
    stability = {}

    for concept in concepts:
        count[concept] = len([c for c in concepts if c.intent < concept.intent])
        subsets[concept] = 2 ** len(concept.intent)

    bottom_concepts = set([concepts.top_concept])
    while not len(concepts) == 0:
        bottom_concept = bottom_concepts.pop()
        stability[bottom_concept] = subsets[bottom_concept] / \
            (2 ** len(bottom_concept.intent))
        concepts.remove(bottom_concept)
        for c in concepts:
            if bottom_concept.intent < c.intent:
                subsets[c] -= subsets[bottom_concept]
                count[c] -= 1
                if count[c] == 0:
                    bottom_concepts.add(c)
    return stability




if __name__ == '__main__':
    # Test code
    from fcatng import ConceptLattice, Context
    from probability import compute_probability
    from stability import (compute_estability, compute_istability)
    from separation import compute_separation_index
    
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, False],\
          [False, True, True, True]]
    objs = ['1', '2', '3', '4']
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cl = ConceptLattice(c)
#    compute_index(cl, compute_probability, "Probability")
#    cs = filter_concepts(cl, compute_probability, "abs", 4)
#    compute_index(cl, compute_separation_index, "Separation")
#    cs = filter_concepts(cl, compute_probability, "value", 0.5)
    # compute_index(cl, compute_istability, "Intensional Stability")
    # print cl
    cs = filter_concepts(cl, compute_istability, "abs", 2)
    print(cs)
