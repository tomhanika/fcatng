import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Includes the above folder
from fcatng.algorithms import closure_operators, dg_basis
from fcatng import context
from fcatng.tests import helper_test
from fcatng import partial_context


# Path to the test_instances.txt
file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'context_test_instances.json')


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_generalized_compute_dg_basis(test_data):
    """
    Tests the function 'generalized_compute_dg_basis' from 'dg_basis'.

    Parameters of 'generalized_compute_dg_basis' :
    - cxt       : Context object.
    - aclose    : 'aclosure' function from 'closure_operators'.
    - close     : 'lin_closure' or 'simple_closure' from 'closure_operators'.
    - imp_basis : List that is always = []
    - cond      : Always remains True.
    """

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


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_partial_dg_basis(test_data):
    """
    Fehler in der Methode gefunden!
    In 'compare_context' Zeile : 25 (if not (table_left[b][a] <= table_right[b][a]):)

    Ursache :
    a und b werden vorher durch Division berechnet, in Python 3 ist das ergebnis einer Division standardmäßig ein Float.
    Ein Indice muss allerdings eine Ganzzahl sein.

    Lösung :
    / durch // erstzen.

    In compare_context Zeile 5 ist ein Syntax-Warning, ausgelöst durch das '\'.

    Lösung :
    Rohstring verwenden.



    - Wird nur mit simple_closure aufgerufen.
    """
    p_cont_inst = partial_context.PartialContext(test_data['ct'], test_data['ct'], test_data['objs'],
                                                 test_data['attrs'])
    p_basis = dg_basis.compute_partial_dg_basis(p_cont_inst, closure_operators.simple_closure, [])
    p_bas_prem, p_bas_conc = helper_test.split_implication(p_basis)
    cor_att_prem, cor_att_conc = helper_test.split_implication(test_data['correct_attr_imp'])
    index = 0

    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(p_bas_prem[index])
        assert set(cor_conclusion) == set(p_bas_conc[index])
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_compute_dg_basis(test_data):
    """
    Eigentlich nur Wrapper-Klasse für den Aufruf von 'generalized_compute_dg_basis'.
    """

    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    imp_basis = []
    cond = lambda x: True
    index = 0

    basis = dg_basis.compute_dg_basis(cxt, closure_operators.simple_closure, imp_basis, cond)
    rel_bas_prem, rel_bas_conc = helper_test.split_implication(basis)
    cor_att_prem, cor_att_conc = helper_test.split_implication(test_data['correct_attr_imp'])

    # Test for simple_closure
    for cor_premis, cor_conclusion in zip(cor_att_prem, cor_att_conc):
        assert set(cor_premis) == set(rel_bas_prem[index])
        assert set(cor_conclusion) == set(rel_bas_conc[index])
        index = index + 1
