
import os
import unittest
import tempfile
import fcatng
from fcatng.readwrite.dot import write_dot
from fcatng.readwrite.fimi import write_fimi

class TestDotFimi(unittest.TestCase):
    def setUp(self):
        self.context = fcatng.Context(
            [[True, False, False, True],
             [True, False, True, False],
             [False, True, True, False],
             [False, True, True, True]],
            ['g1', 'g2', 'g3', 'g4'],
            ['a', 'b', 'c', 'd']
        )
        self.lattice = fcatng.ConceptLattice(self.context)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_write_dot(self):
        write_dot(self.lattice, self.temp_file.name)
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
            self.assertIn("digraph L", content)
            # Check for at least one self loop (label) or connection
            self.assertTrue("->" in content)

    def test_write_fimi(self):
        write_fimi(self.context, self.temp_file.name)
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
            # Check for attributes of first object (a, d)
            self.assertIn("a", content)
            self.assertIn("d", content)

if __name__ == '__main__':
    unittest.main()
