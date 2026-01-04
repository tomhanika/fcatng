# -*- coding: utf-8 -*-
"""FCA library"""

from fcatng.definitions import (
    Context,
    Concept,
    ConceptLattice,
    ConceptSystem,
    Implication,
    ManyValuedContext,
    Scale,
    PartialContext
)

# algorithms and readwrite might depend on definitions, so we import them after
from fcatng import algorithms
from fcatng.algorithms import (
    norris,
    compute_covering_relation,
    scale_mvcontext,
    compute_dg_basis
)
from fcatng import readwrite

__all__ = [
    "Context",
    "Concept",
    "ConceptLattice",
    "ConceptSystem",
    "Implication",
    "ManyValuedContext",
    "Scale",
    "PartialContext",
    "algorithms",
    "readwrite",
    "norris",
    "compute_covering_relation",
    "scale_mvcontext",
    "compute_dg_basis"
]
