import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng import context, Concept, ConceptSystem, compute_covering_relation, Implication
from fcatng.tests import helper_test
from fcatng.algorithms.implication_covers import compute_implication_cover, is_redundant, is_new, CustomException, \
    is_subsumed_simply, is_subsumed, remove_subsumed_plus, remove_subsumed, remove_subsumed_simply, add_smartly, \
    updated_basis
from fcatng.algorithms import closure_operators

# Path to the test_instances.txt
file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'context_test_instances.json')


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_implication_cover(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    imp_cover = compute_implication_cover(cxt)

    func_premis_elements, func_conclusion_elements = helper_test.split_implication(imp_cover)
    test_premis_elements, test_conclusion_elements = helper_test.split_implication(test_data["implication_covers_imps"])

    sortet_test_prem = []
    sortet_test_conc = []
    for prem in test_premis_elements:
        sortet_test_prem.append(prem.sort())

    for conc in test_conclusion_elements:
        sortet_test_conc.append(conc.sort())

    sortet_func_prem = []
    sortet_func_conc = []
    for prem in func_premis_elements:
        sortet_func_prem.append(prem.sort())

    for conc in func_conclusion_elements:
        sortet_func_conc.append(conc.sort())

    assert sortet_test_prem == sortet_func_prem
    assert sortet_test_conc == sortet_func_conc


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_is_redundant(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    #imp_basis = []
    imp_basis = compute_implication_cover(cxt, closure_operators.closure)

    result = is_redundant(imp, imp_basis)

    assert result == test_data["implication_redundant_correct"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_is_new(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    implications = []

    for i in test_data["correct_attr_imp"]:
        implications.append(Implication(set(i)))

    try:
        result = is_new(imp, implications)
    except CustomException as e:
        print(e)
        result = False

    assert result == test_data["implications_is_new"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_is_subsumed_simply(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    by_imp = Implication(set(test_data["implication_subsummed"]))

    result = is_subsumed_simply(imp, by_imp)

    assert result == test_data["implication_subsummed_correct"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_is_subsumed(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    by_imp = Implication(set(test_data["implication_subsummed"]))

    result = is_subsumed(imp, by_imp)

    assert result == test_data["implication_subsummed_correct"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_remove_subsumed_plus(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    implications = []

    for i in test_data["correct_attr_imp"]:
        implications.append(Implication(set(i)))

    result = remove_subsumed_plus(imp, implications)

    assert result == test_data["remove_subsumed_plus"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_remove_subsumed(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    implications = []

    for i in test_data["correct_attr_imp"]:
        implications.append(Implication(set(i)))

    result = remove_subsumed(imp, implications)

    assert result == test_data["remove_subsumed_plus"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_remove_subsumed_simply(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))
    implications = []

    for i in test_data["correct_attr_imp"]:
        implications.append(Implication(set(i)))

    result = remove_subsumed_simply(imp, implications)

    assert result == test_data["remove_subsumed_plus"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_add_smartly(test_data):
    imp = Implication(set(test_data["implication_redundant"][0]), set(test_data["implication_redundant"][1]))

    implications = []

    for i in test_data["correct_attr_imp"]:
        implications.append(Implication(set(i)))

    try:
        result = add_smartly(imp, implications, implications)
    except CustomException as e:
        print(e)
        result = False

    if result == None:
        result = False

    assert result == test_data["add_smartly_new"]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_updated_basis(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    attributes = test_data['attrs']
    intent = test_data["correct_intent"][1]
    imp_basis = compute_implication_cover(cxt, closure_operators.closure)

    result = updated_basis(set(intent), imp_basis, attributes)

    func_premis_elements, func_conclusion_elements = helper_test.split_implication(result)
    test_premis_elements, test_conclusion_elements = helper_test.split_implication(test_data["updated_basis_result"])

    sortet_test_prem = []
    sortet_test_conc = []
    for prem in test_premis_elements:
        sortet_test_prem.append(prem.sort())

    for conc in test_conclusion_elements:
        sortet_test_conc.append(conc.sort())

    sortet_func_prem = []
    sortet_func_conc = []
    for prem in func_premis_elements:
        sortet_func_prem.append(prem.sort())

    for conc in func_conclusion_elements:
        sortet_func_conc.append(conc.sort())

    assert sortet_test_prem == sortet_func_prem
    assert sortet_test_conc == sortet_func_conc


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_minimiz(test_data):
    print("Hello World!")
