import json


def get_test_data(file_path):
    """
    This function reads the test data, out of the .txt file.
    """
    # TO-DO : Return an Instance, and the solutions from this function
    with open(file_path, 'r') as file:
        test_data = json.load(file)
    return test_data


def split_implication(implications):
    """
    Function to split the given implications in premis and conclusion

    Parameters :
    implications ( List containing strings ) : One string contains one implication

    Returning :
    premis_elements( nested list, lists in the nested list contain strings ) : The content of the lists are the elements
                                                                               of the corresponding premis.
    conclusion_elements( nested list, lists in the nested list contain strings ) : The content of the lists are the
                                                                                   elements of the corresponding conclusion.

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


def get_obj_intent(cross_table, attributes, index):
    """
    Function that returns a set of attributes where the value of the cross-table index is true.
    """
    result_set = []
    for_index = 0
    for element in cross_table[index]:
        if element == True:
            result_set.append(attributes[for_index])
        for_index = for_index + 1

    return set(result_set)


def get_attr_extent(cont_inst, index):
    result_set = []
    for_index = 0

    for element in cont_inst.transpose()._table[index]:
        if element == True:

            result_set.append(cont_inst.objects[for_index])
        for_index = for_index + 1

    return set(result_set)