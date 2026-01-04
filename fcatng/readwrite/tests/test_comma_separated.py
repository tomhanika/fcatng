
import os
import unittest
import tempfile
import fcatng
from fcatng.readwrite.comma_separated import read_mv_csv

class TestCommaSeparated(unittest.TestCase):
    def setUp(self):
        self.mv_context = fcatng.ManyValuedContext(
             [['7', '6', '7'],
             ['7', '2', '9'],
             ['1', '3', '4']],
             ['obj1', 'obj2', 'obj3'],
             ['attr1', 'attr2', 'attr3']
        )
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_read_mv_csv(self):
        # Create a dummy csv
        with open(self.temp_file.name, 'w') as f:
            f.write("attr1,attr2,attr3\n")
            f.write("obj1,7,6,7\n")
            f.write("obj2,7,2,9\n")
            f.write("obj3,1,3,4\n")

        loaded_context = read_mv_csv(self.temp_file.name)

        self.assertEqual(self.mv_context.objects, loaded_context.objects)
        self.assertEqual(self.mv_context.attributes, loaded_context.attributes)
        self.assertEqual(self.mv_context._table, loaded_context._table)

if __name__ == '__main__':
    unittest.main()
