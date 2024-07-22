from fcatng import context


# Initialise the Variables
ct = [[True, False, False, True],
      [True, False, True, False],
      [False, True, True, False],
      [False, True, True, True]]
objs = [1, 2, 3, 4]
attrs = ['a', 'b', 'c', 'd']


# Create a Context object
context_inst = context.Context(ct, objs, attrs)


def test_get_object_intent_by_index():

    # Store the results of the 4 different rows
    result_row1 = context_inst.get_object_intent_by_index(0)
    result_row2 = context_inst.get_object_intent_by_index(1)
    result_row3 = context_inst.get_object_intent_by_index(2)
    result_row4 = context_inst.get_object_intent_by_index(3)

    assert result_row1 == {'a', 'd'}
    assert result_row2 == {'a', 'c'}
    assert result_row3 == {'b', 'c'}
    assert result_row4 == {'b', 'c', 'd'}


def test_get_attributes():

    result = context_inst.get_attributes()

    attributes = ['a', 'b', 'c', 'd']

    assert result == attributes


def test_get_attribute_implications():
    result = context_inst.get_attribute_implications()

    result_str = str(result)

    print("Elemente :")

    index = 1

    for element in result:
        print(element)
        if index == 1:
            assert str(element) == 'c, d => b' or str(element) == 'd, c => b'

        if index == 2:
            assert str(element) == 'b => c'

        if index == 3:
            assert (str(element) == 'a, b, c => d' or str(element) == 'a, c, b => d' or str(element) == 'b, a, c => d' or
                    str(element) == 'b, c, a => d' or str(element) == 'c, a, b => d' or str(element) == 'c, b, a => d')

        index = index + 1