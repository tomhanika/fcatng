import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import closure_operators, dg_basis
from fcatng import context, Implication
from fcatng.tests import helper_test
from fcatng import partial_context


# Path to the test_instances.txt
file_path = os.path.join(os.path.dirname(__file__), 'dg_basis_test_data.json')


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_generalized_compute_dg_basis(test_data):

    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    imp_basis = []
    cond = lambda x: True
    index = 0

    correct_implications = []
    for prem, conc in zip(test_data['correct_attr_imp_prem'], test_data['correct_attr_imp_conc']):
        correct_implications.append(Implication(prem, conc))

    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.simple_closure,
                                                           imp_basis, cond)

    for imp, test in zip(relative_basis, correct_implications):
        assert imp.__cmp__(test)

    relative_basis = dg_basis.generalized_compute_dg_basis(cxt.attributes, aclose, closure_operators.lin_closure,
                                                           imp_basis, cond)

    for imp, test in zip(relative_basis, correct_implications):
        assert imp.__cmp__(test)


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_partial_dg_basis(test_data):

    correct_implications = []
    for prem, conc in zip(test_data['correct_attr_imp_prem'], test_data['correct_attr_imp_conc']):
        correct_implications.append(Implication(prem, conc))

    p_cont_inst = partial_context.PartialContext(test_data['ct'], test_data['ct'], test_data['objs'],
                                                 test_data['attrs'])
    p_basis = dg_basis.compute_partial_dg_basis(p_cont_inst, closure_operators.simple_closure, [])

    for imp, test in zip(p_basis, correct_implications):
        assert imp.__cmp__(test)


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_dg_basis(test_data):

    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    imp_basis = []
    cond = lambda x: True

    correct_implications = []
    for prem, conc in zip(test_data['correct_attr_imp_prem'], test_data['correct_attr_imp_conc']):
        correct_implications.append(Implication(prem, conc))

    basis = dg_basis.compute_dg_basis(cxt, closure_operators.simple_closure, imp_basis, cond)

    for imp, test in zip(basis, correct_implications):
        assert imp.__cmp__(test)
