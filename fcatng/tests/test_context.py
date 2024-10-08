import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Includes the above folder
from fcatng import context, Implication
import fcatng
import helper_test


# Path to the test_instances.txt
file_path = 'context_test_data.json'


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
    cxt = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    correct_implications = []
    for prem, conc in zip(test_data['correct_attr_imp_prem'], test_data['correct_attr_imp_conc']):
        correct_implications.append(Implication(prem, conc))

    implication = cxt.get_attribute_implications()
    for imp, test in zip(implication, correct_implications):
        assert imp.__cmp__(test)


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_get_object_implications(test_data):
    confirmed = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_attribute_implications()
    func_implications = context.Context(test_data['ct'], test_data['objs'], test_data['attrs']).get_object_implications(
        fcatng.algorithms.compute_dg_basis, confirmed)

    correct_implications = []
    for prem, conc in zip(test_data['correct_obj_imp_prem'], test_data['correct_obj_imp_conc']):
        correct_implications.append(Implication(prem, conc))

    for imp, test in zip(func_implications, correct_implications):
        assert imp.__cmp__(test)


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


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_delete_object(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.delete_object(len(test_data['objs']) - 1)

    assert context_inst.objects == test_data['delete_object']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_delete_object_by_name(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.delete_object_by_name(test_data['delete_object_name'])

    assert context_inst.objects == test_data['delete_object']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_delete_attribute(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.delete_attribute(len(test_data['attrs']) - 1)

    assert context_inst.attributes == test_data['delete_attribute']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_delete_attribute_by_name(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.delete_attribute_by_name(test_data['delete_attribute_name'])

    assert context_inst.attributes == test_data['delete_attribute']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_rename_object(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.rename_object(test_data['rename_object'][0], test_data['rename_object'][1])

    assert context_inst.objects == test_data['renamed_objects']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_rename_attribute(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    context_inst.rename_attribute(test_data['rename_attribute'][0], test_data['rename_attribute'][1])

    assert context_inst.attributes == test_data['renamed_attributes']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_transpose(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    assert context_inst.transpose()._table == test_data['transposed']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_extract_subcontext_filtered_by_attributes(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    subcontext = context_inst.extract_subcontext_filtered_by_attributes(test_data['subcontext_attributes'])

    assert subcontext._table == test_data['subcontext_cor_attributes']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_extract_subcontext(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    subcontext = context_inst.extract_subcontext_filtered_by_attributes(test_data['subcontext_attributes'])

    assert subcontext._table == test_data['subcontext_cor_attributes']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_extract_subtable(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    subtable = context_inst._extract_subtable(test_data['subcontext_attributes'])

    assert subtable == test_data['subtable_cor_attributes']


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_extract_subtable_by_condition(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    def condition(index):
        return context_inst.objects[index] == test_data['subtable_condition'][0][0]

    # Verwende die condition-Funktion, um die Indizes zu filtern
    indices = [i for i in range(len(context_inst.objects)) if condition(i)]

    # Extrahiere die Subtabelle basierend auf den gefilterten Indizes
    subtable = context_inst._extract_subtable_by_condition(condition)

    assert subtable[1] == test_data['subtable_condition'][1]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_extract_subtable_by_attribute_values(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    values = {
        test_data['subcontext_attributes'][0]: True,
        test_data['subcontext_attributes'][1]: False
    }

    subtable = context_inst._extract_subtable_by_attribute_values(values)

    assert subtable[1] == test_data['subtable_attribute'][1]


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_has_values(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    values = {
        test_data['subcontext_attributes'][0]: True,
        test_data['subcontext_attributes'][1]: False
    }

    assert context_inst._has_values(1, values) == True


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_has_at_least_one_value(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])
    values = {
        test_data['subcontext_attributes'][0]: True,
        test_data['subcontext_attributes'][1]: False
    }

    assert context_inst._has_at_least_one_value(1, values) == True


@pytest.mark.parametrize("test_data", helper_test.get_test_data(file_path))
def test_check_attribute_names(test_data):
    context_inst = context.Context(test_data['ct'], test_data['objs'], test_data['attrs'])

    assert context_inst._check_attribute_names(test_data['attrs']) is None
