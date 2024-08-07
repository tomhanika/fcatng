import ast
import sys
import os
from fcatng import context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Includes the above folder


# Initialise the Variables
ct = [[True, False, False, True],
      [True, False, True, False],
      [False, True, True, False],
      [False, True, True, True]]
objs = [1, 2, 3, 4]
attrs = ['a', 'b', 'c', 'd']


# Create a Context object
context_inst = context.Context(ct, objs, attrs)


def get_test_data():
    test_data = []
    with open('context_test_instances.txt', 'r') as file:
        txt_content = file.read().strip()
        instances = txt_content.split('\n\n')
        for instance in instances:
            data = {}
            for row in instance.split('\n'):
                key, value = row.split(' = ')
                data[key] = ast.literal_eval(value)
            test_data.append(data)
    return test_data


def test_get_object_intent_by_index():

    # Store the results of the 4 different rows
    result_row1 = context_inst.get_object_intent_by_index(0)
    result_row2 = context_inst.get_object_intent_by_index(1)
    result_row3 = context_inst.get_object_intent_by_index(2)
    result_row4 = context_inst.get_object_intent_by_index(3)

    assert result_row1 == {'a', 'd'}
    assert result_row2 == {'a', 'c'}
    assert result_row3 == {'b', 'c'}
    assert result_row4 == {'b', 'c', 'd'}


def test_get_attributes():
    result = context_inst.get_attributes()

    attributes = ['a', 'b', 'c', 'd']

    assert result == attributes


def test_get_attribute_implications():
    result = context_inst.get_attribute_implications()

    index = 1

    for element in result:
        if index == 1:
            assert str(element) == 'c, d => b' or str(element) == 'd, c => b'

        if index == 2:
            assert str(element) == 'b => c'

        if index == 3:
            assert (str(element) == 'a, b, c => d' or str(element) == 'a, c, b => d' or str(element) == 'b, a, c => d' or
                    str(element) == 'b, c, a => d' or str(element) == 'c, a, b => d' or str(element) == 'c, b, a => d')

        index = index + 1


def test_get_attribute_implications_auto():
    context_instance = context_inst.get_attribute_implications()

    func_implications = context_instance
    func_premis_elements, func_conclusion_elements = split_implication(func_implications)
    test_implications = ["c, d => b", "b => c", "a, c, b => d"]
    test_premis_elements, test_conclusion_elements = split_implication(test_implications)
    index = 0

    for test_premis, test_implication in zip(test_premis_elements, test_conclusion_elements):
        assert set(test_premis) == set(func_premis_elements[index])
        assert set(test_implication) == set(func_conclusion_elements[index])
        index = index + 1


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

