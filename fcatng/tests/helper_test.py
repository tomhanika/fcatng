import json


def get_test_data(file_path):
    """
    This function reads the test data, out of the .txt file.

    Parameters :
    file_path (String containing the path to 'context_test_instances.txt')

    Returning :
    test_data ( Instances from the .txt)
    """

    with open(file_path, 'r') as file:
        test_data = json.load(file)
    return test_data
