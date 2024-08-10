import json
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Includes the above folder
from fcatng import context
import fcatng
from fcatng.algorithms import closure_operators


def get_test_data():
    """
    This function reads the test data, out of the .txt file.
    """
    # TO-DO : Return an Instance, and the solutions from this function
    with open('context_test_instances.txt', 'r') as file:
        test_data = json.load(file)
    return test_data


# --------------------------------------------------------------------------- #
# Test-Methods
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("test_data", get_test_data())
def test_get_object_intent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.objects):
        assert context_inst.get_object_intent_by_index(index) == get_obj_intent(test_data['ct'],
                                                                                test_data['attrs'], index)
        index = index + 1


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_object_intent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    for obj in test_data['objs']:
        assert cont_inst.get_object_intent(obj) == get_obj_intent(test_data['ct'], test_data['attrs'],
                                                                  cont_inst.objects.index(obj))


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_attribute_extent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.attributes):
        assert context_inst.get_attribute_extent_by_index(index) == get_attr_extent(context_inst, index)
        index = index + 1


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_attribute_extent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    for attr in test_data['attrs']:
        assert cont_inst.get_attribute_extent(attr) == get_attr_extent(cont_inst, cont_inst.attributes.index(attr))


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_attributes(test_data):
    func_attrs = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_attributes()
    correct_attrs = test_data['attrs']

    assert func_attrs == correct_attrs


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_attribute_implications(test_data):
    func_implications = (context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
                         .get_attribute_implications())
    func_premis_elements, func_conclusion_elements = split_implication(func_implications)
    test_implications = test_data['correct_attr_imp']
    test_premis_elements, test_conclusion_elements = split_implication(test_implications)
    index = 0

    for test_premis, test_implication in zip(test_premis_elements, test_conclusion_elements):
        assert set(test_premis) == set(func_premis_elements[index])
        assert set(test_implication) == set(func_conclusion_elements[index])
        index = index + 1


@pytest.mark.parametrize("test_data", get_test_data())
def test_get_object_implications(test_data):
    # imp_basis ist in diesem Fall immer 'None' weshalb es in der lin_closure Methode immer einen Fehler gibt.
    # imp_basis sollte ein Set mit implikationen beinhalten, hier wird es manuell übergeben.
    confirmed = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_attribute_implications()
    func_implications = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_object_implications(
        fcatng.algorithms.compute_dg_basis, confirmed)
    func_premis_elements, func_conclusion_elements = split_implication(func_implications)
    test_implications = test_data['correct_obj_imp']
    test_premis_elements, test_conclusion_elements = split_implication(test_implications)
    index = 0

    for test_premis, test_implication in zip(test_premis_elements, test_conclusion_elements):
        assert set(test_premis) == set(func_premis_elements[index])
        assert set(test_implication) == set(func_conclusion_elements[index])
        index = index + 1


# --------------------------------------------------------------------------- #
# Helper-Methods
# --------------------------------------------------------------------------- #

def split_implication(implications):
    """
    Function to split the given implications in premis and conclusion

    Parameters :
    implications ( List containing strings ) : One string contains one implication

    Returning :
    premis_elements( nested list, lists in the nested list contain strings ) : The content of the lists are the elements
                                                                               of the corresponding premis.
    conclusion_elements( nested list, lists in the nested list contain strings ) : The content of the lists are the
                                                                                   elements of the corresponding conclusion.

    Example :
    implications : ["c, d => b",
                   "b => c",
                   "a, c, b => d"]

    premis_elements : [["c", "d"],
                      ["b"],
                      ["a", "c", "d"]]

    conclusion_elements : [["b"],
                          ["c"],
                          ["d"]]
    """

    premis_elements = []
    conclusion_elements = []
    for implication in implications:
        element_parts = str(implication).replace(" ", "").split("=>")
        premis_elements.append(element_parts[0].split(","))
        conclusion_elements.append(element_parts[1].split(","))

    return premis_elements, conclusion_elements


def get_obj_intent(cross_table, attributes, index):
    """
    Function that returns a set of attributes where the value of the cross-table index is true.
    """
    result_set = []
    for_index = 0
    for element in cross_table[index]:
        if element == True:
            result_set.append(attributes[for_index])
        for_index = for_index + 1

    return set(result_set)


def get_attr_extent(cont_inst, index):
    result_set = []
    for_index = 0

    for element in cont_inst.transpose()._table[index]:
        if element == True:

            result_set.append(cont_inst.objects[for_index])
        for_index = for_index + 1

    return set(result_set)
