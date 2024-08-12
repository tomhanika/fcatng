import json
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import closure_operators, dg_basis
from fcatng import context


def get_test_data():
    """
    This function reads the test data, out of the .txt file.
    """
    # TO-DO : Return an Instance, and the solutions from this function

    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'context_test_instances.txt')

    with open(file_path, 'r') as file:
        test_data = json.load(file)
    return test_data


@pytest.mark.parametrize("test_data", get_test_data())
def test_generalized_compute_dg_basis(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    imp_basis = []
    cond = lambda x: True
    index = 0

    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.simple_closure,
                                                           imp_basis, cond)
    rel_bas_prem, rel_bas_conc = split_implication(relative_basis)
    cor_att_prem, cor_att_conc = split_implication(test_data['correct_attr_imp'])

    # Test for simple_closure
    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(rel_bas_prem[index])
        assert set(cor_conclusion) == set(rel_bas_conc[index])
        index = index + 1

    index = 0
    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.lin_closure,
                                                           imp_basis, cond)
    rel_bas_prem, rel_bas_conc = split_implication(relative_basis)

    # Test for lin_closure
    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(rel_bas_prem[index])
        assert set(cor_conclusion) == set(rel_bas_conc[index])
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
                                                                                   elements of the corresponding
                                                                                   conclusion.

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
