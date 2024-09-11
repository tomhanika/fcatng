import os
import sys

import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import norris, derivation
from fcatng import context
from fcatng.tests import helper_test


# Path to the test_instances.txt
file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'context_test_instances.json')


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_derivation(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    deriv_ext = derivation(cxt, extent=test_data["derivation_extent"])
    deriv_int = derivation(cxt, intent=test_data["derivation_intent"])

    assert deriv_ext == set(test_data["deriv_ext_result"])
    assert deriv_int == set(test_data["deriv_int_result"])


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_norris(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    norris_data = norris(cxt)
    element_list_objs = []
    element_list_attrs = []

    result_list_int = []
    result_list_ext = []

    for element in norris_data[0]:
        print(element.extent)
        element_list_objs.append(element.intent)
        element_list_attrs.append(element.extent)

    for element in test_data["norris_result_ext"]:
        if element == []:
            result_list_ext.append(set())
        else:
            result_list_ext.append(set(element))

    for element in test_data["norris_result_int"]:
        if element == []:
            result_list_int.append(set(element))
        else:
            result_list_int.append(set(element))

    assert element_list_attrs == result_list_ext
    assert element_list_objs == result_list_int
