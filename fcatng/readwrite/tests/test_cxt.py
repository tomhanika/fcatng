
import os
import unittest
import tempfile
import fcatng
from fcatng.readwrite.cxt import read_cxt, write_cxt

class TestCxt(unittest.TestCase):
    def setUp(self):
        self.context = fcatng.Context(
            [[True, False, False, True],
             [True, False, True, False],
             [False, True, True, False],
             [False, True, True, True]],
            ['Obj 1', 'Obj 2', 'Obj 3', 'Obj 4'],
            ['a', 'b', 'c', 'd']
        )
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.cxt', mode='w')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_write_read_cxt(self):
        write_cxt(self.context, self.temp_file.name)
        loaded_context = read_cxt(self.temp_file.name)

        self.assertEqual(self.context.objects, loaded_context.objects)
        self.assertEqual(self.context.attributes, loaded_context.attributes)
        self.assertEqual(self.context._table, loaded_context._table)

if __name__ == '__main__':
    unittest.main()
