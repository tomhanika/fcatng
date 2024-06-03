# -*- coding: utf-8 -*-
"""FCA library"""

from fcatng.concept import Concept
from fcatng.concept_system import ConceptSystem
from fcatng.concept_lattice import ConceptLattice
from fcatng.context import Context
from fcatng.mvcontext import ManyValuedContext
from fcatng.scale import Scale
from fcatng.implication import Implication

from fcatng.algorithms import (norris, compute_covering_relation,
                            scale_mvcontext, compute_dg_basis)
from fcatng.readwrite import (read_txt, read_cxt, write_cxt, write_dot,
                           read_mv_txt, read_xml, write_xml, write_mv_txt,
                           uread_cxt, uwrite_cxt)
from fcatng.algorithms.filters import (filter_concepts, compute_estability,
compute_istability, compute_separation_index, 
compute_probability, compute_index)
