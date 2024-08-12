import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Includes the above folder
from fcatng import context
import fcatng
import helper_test


# Path to the test_instances.txt
file_path = 'context_test_instances.txt'


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_intent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.objects):
        assert context_inst.get_object_intent_by_index(index) == helper_test.get_obj_intent(test_data['ct'],
                                                                                            test_data['attrs'], index)
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_intent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    for obj in test_data['objs']:
        assert cont_inst.get_object_intent(obj) == helper_test.get_obj_intent(test_data['ct'], test_data['attrs'],
                                                                              cont_inst.objects.index(obj))


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attribute_extent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.attributes):
        assert context_inst.get_attribute_extent_by_index(index) == helper_test.get_attr_extent(context_inst, index)
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attribute_extent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    for attr in test_data['attrs']:
        assert cont_inst.get_attribute_extent(attr) == helper_test.get_attr_extent(cont_inst,
                                                                                   cont_inst.attributes.index(attr))


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attributes(test_data):
    func_attrs = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_attributes()
    correct_attrs = test_data['attrs']

    assert func_attrs == correct_attrs


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attribute_implications(test_data):
    func_implications = (context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
                         .get_attribute_implications())
    func_premis_elements, func_conclusion_elements = helper_test.split_implication(func_implications)
    test_implications = test_data['correct_attr_imp']
    test_premis_elements, test_conclusion_elements = helper_test.split_implication(test_implications)
    index = 0

    for test_premis, test_implication in zip(test_premis_elements, test_conclusion_elements):
        assert set(test_premis) == set(func_premis_elements[index])
        assert set(test_implication) == set(func_conclusion_elements[index])
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_implications(test_data):
    # imp_basis ist in diesem Fall immer 'None' weshalb es in der lin_closure Methode immer einen Fehler gibt.
    # imp_basis sollte ein Set mit implikationen beinhalten, hier wird es manuell übergeben.
    confirmed = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_attribute_implications()
    func_implications = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_object_implications(
        fcatng.algorithms.compute_dg_basis, confirmed)
    func_premis_elements, func_conclusion_elements = helper_test.split_implication(func_implications)
    test_implications = test_data['correct_obj_imp']
    test_premis_elements, test_conclusion_elements = helper_test.split_implication(test_implications)
    index = 0

    for test_premis, test_implication in zip(test_premis_elements, test_conclusion_elements):
        assert set(test_premis) == set(func_premis_elements[index])
        assert set(test_implication) == set(func_conclusion_elements[index])
        index = index + 1
