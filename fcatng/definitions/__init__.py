# -*- coding: utf-8 -*-
"""
Formal Concepts definitions
"""
from .context import Context
from .concept import Concept
from .concept_lattice import ConceptLattice
from .concept_system import ConceptSystem
from .implication import Implication
from .mvcontext import ManyValuedContext
from .scale import Scale
from .partial_context import PartialContext

__all__ = [
    "Context",
    "Concept",
    "ConceptLattice",
    "ConceptSystem",
    "Implication",
    "ManyValuedContext",
    "Scale",
    "PartialContext",
]
