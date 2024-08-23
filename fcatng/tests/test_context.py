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
def test_get_objects(test_data):
    func_objs = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_objects()

    assert set(func_objs) == set(test_data["objs"])


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_intent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.objects):

        assert context_inst.get_object_intent_by_index(index) == set(test_data['correct_intent_index'][index])
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_intent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    for obj in test_data['objs']:

        assert cont_inst.get_object_intent(obj) == set(test_data['correct_intent'][index])
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attribute_extent_by_index(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    while index < len(context_inst.attributes):

        assert context_inst.get_attribute_extent_by_index(index) == set(test_data['correct_extent_index'][index])
        index = index + 1


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_attribute_extent(test_data):
    cont_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    index = 0

    for attr in test_data['attrs']:

        assert cont_inst.get_attribute_extent(attr) == set(test_data['correct_extent'][index])
        index = index + 1


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


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_value(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    value = context_inst.get_value(test_data['value_obj'][0], test_data['value_attr'][0])

    assert value == test_data['value_obj'][1]
    assert value == test_data['value_attr'][1]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_add_attribute(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.add_attribute(test_data['for_add_attributes'][0], test_data['for_add_attributes'][1][0])

    assert context_inst.attributes == test_data['after_add_attribute']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_add_object(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.add_object(test_data['for_add_object'][0], test_data['for_add_object'][1][0])

    assert context_inst.objects == test_data['after_add_object']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_add_object_with_intent(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.add_object_with_intent(test_data['add_object_intent'][0], test_data['add_object_intent'][1][0])

    assert context_inst.objects == test_data['after_add_object']
    assert context_inst._table[-1] == test_data['add_object_intent'][2]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_add_attribute_with_extent(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.add_attribute_with_extent(test_data['add_attribute_extent'][0], test_data['add_attribute_extent'][1][0])
    extents = [inner_list[-1] for inner_list in context_inst._table]

    assert context_inst.attributes == test_data['after_add_attribute']
    assert extents == test_data['add_attribute_extent'][2]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_set_attribute_extent(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.set_attribute_extent(test_data['set_attribute_extent'][0], test_data['set_attribute_extent'][1][0])

    assert context_inst._table == test_data['set_attribute_extent_table']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_set_object_intent(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.set_object_intent(test_data['set_object_intent'][0], test_data['set_object_intent'][1][0])

    assert context_inst._table[0] == test_data['set_object_intent'][2]
