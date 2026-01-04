
import os
import unittest
import tempfile
import fcatng
from fcatng.readwrite.xml_ import read_xml, write_xml

class TestXml(unittest.TestCase):
    def setUp(self):
        self.context = fcatng.Context(
            [[True, False, False, True],
             [True, False, True, False],
             [False, True, True, False],
             [False, True, True, True]],
            ['Obj 1', 'Obj 2', 'Obj 3', 'Obj 4'],
            ['a', 'b', 'c', 'd']
        )
        self.lattice = fcatng.ConceptLattice(self.context)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xml', mode='w')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_write_read_xml(self):
        write_xml(self.temp_file.name, self.lattice)
        loaded_cs = read_xml(self.temp_file.name)

        # Verify concepts are similar
        # Since order might not be preserved in XML or ConceptSystem, we check existence
        self.assertEqual(len(self.lattice), len(loaded_cs))

        # Simple check for intent/extent sizes matching
        original_extents = sorted([len(c.extent) for c in self.lattice])
        loaded_extents = sorted([len(c.extent) for c in loaded_cs])
        self.assertEqual(original_extents, loaded_extents)

if __name__ == '__main__':
    unittest.main()
