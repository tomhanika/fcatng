import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import closure_operators, dg_basis
from fcatng import context
from fcatng.tests import helper_test


# Path to the test_instances.txt
file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'context_test_instances.txt')


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_generalized_compute_dg_basis(test_data):
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    imp_basis = []
    cond = lambda x: True
    index = 0

    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.simple_closure,
                                                           imp_basis, cond)
    rel_bas_prem, rel_bas_conc = helper_test.split_implication(relative_basis)
    cor_att_prem, cor_att_conc = helper_test.split_implication(test_data['correct_attr_imp'])

    # Test for simple_closure
    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(rel_bas_prem[index])
        assert set(cor_conclusion) == set(rel_bas_conc[index])
        index = index + 1

    index = 0
    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.lin_closure,
                                                           imp_basis, cond)
    rel_bas_prem, rel_bas_conc = helper_test.split_implication(relative_basis)

    # Test for lin_closure
    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(rel_bas_prem[index])
        assert set(cor_conclusion) == set(rel_bas_conc[index])
        index = index + 1
