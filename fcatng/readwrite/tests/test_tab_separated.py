
import os
import unittest
import tempfile
import fcatng
from fcatng.readwrite.tab_separated import read_txt, read_mv_txt, write_mv_txt

class TestTabSeparated(unittest.TestCase):
    def setUp(self):
        self.context = fcatng.Context(
            [[True, False, False, True],
             [True, False, True, False],
             [False, True, True, False],
             [False, True, True, True]],
            ['g1', 'g2', 'g3', 'g4'],
            ['a', 'b', 'c', 'd']
        )
        self.mv_context = fcatng.ManyValuedContext(
             [['7', '6', '7'],
             ['7', '2', '9'],
             ['1', '3', '4']],
             ['obj1', 'obj2', 'obj3'],
             ['attr1', 'attr2', 'attr3']
        )
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_read_txt(self):
        # Create a dummy context txt file
        with open(self.temp_file.name, 'w') as f:
            f.write("a\tb\tc\td\n\n")
            f.write("1\t0\t0\t1\n")
            f.write("1\t0\t1\t0\n")
            f.write("0\t1\t1\t0\n")
            f.write("0\t1\t1\t1\n")

        loaded_context = read_txt(self.temp_file.name)
        # Note: read_txt generates object names as g1, g2...
        self.assertEqual(self.context.objects, loaded_context.objects)
        self.assertEqual(self.context.attributes, loaded_context.attributes)
        self.assertEqual(self.context._table, loaded_context._table)

    def test_write_read_mv_txt(self):
        write_mv_txt(self.mv_context, self.temp_file.name)
        loaded_context = read_mv_txt(self.temp_file.name)

        self.assertEqual(self.mv_context.objects, loaded_context.objects)
        self.assertEqual(self.mv_context.attributes, loaded_context.attributes)
        self.assertEqual(self.mv_context._table, loaded_context._table)

if __name__ == '__main__':
    unittest.main()
