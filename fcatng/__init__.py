# -*- coding: utf-8 -*-
"""FCA library"""

from fcatng.ng.concept import Concept
from fcatng.ng.concept_system import ConceptSystem
from fcatng.ng.concept_lattice import ConceptLattice
from fcatng.ng.context import Context
from fcatng.ng.mvcontext import ManyValuedContext
from fcatng.ng.scale import Scale
from fcatng.ng.implication import Implication

from fcatng.ng.algorithms import (norris, compute_covering_relation,
                            scale_mvcontext, compute_dg_basis)
from fcatng.ng.readwrite import (read_txt, read_cxt, write_cxt, write_dot,
                           read_mv_txt, read_xml, write_xml, write_mv_txt,
                           uread_cxt, uwrite_cxt)
from fcatng.ng.algorithms.filters import (filter_concepts, compute_estability,
compute_istability, compute_separation_index, 
compute_probability, compute_index)
