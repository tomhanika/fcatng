import os
import sys

import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import norris, derivation
from fcatng import context, Concept, ConceptSystem, compute_covering_relation
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


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_covering_relation(test_data):
    global key_int, key_ext, val_cov
    concept = Concept(test_data["concept"][0], test_data["concept"][1])
    conc_sys = ConceptSystem([concept])

    covering_relation = compute_covering_relation(conc_sys)

    for key, val in covering_relation.items():
        key_ext = key.extent
        key_int = key.intent
        val_cov = val

    if test_data["concept_val"][0] == []:
        correct_result = set()
    else:
        correct_result = test_data["concept_val"]

    assert key_ext == set(test_data["concept"][0])
    assert key_int == set(test_data["concept"][1])
    assert val_cov == correct_result

