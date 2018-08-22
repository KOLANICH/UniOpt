from ..imports import *
from .HyperparamVector import HyperparamVector
from .Spec import Spec, HyperparamDefinition
from ..core.MetaSpec import *


class SpecOnlyBoxes(MSpec(scalarMode=ScalarMetaMap.noScalars)):
	"""A very dumb spec, allowing only uniformly distributed variables, no categoricals and scalars and internal space spec is just a sequence `(lower_bound, upper_bound)`. A widespread situation."""
	class HyperparamsSpecsConverters:
		randint = lambda k, dist, tp: (dist.a, dist.b)
		uniform = lambda k, dist, tp: (dist.ppf(0), dist.ppf(1))


class SpecOnlyBoxesNoIntegers(MSpec(integerMode=IntegerMetaMap.noIntegers), SpecOnlyBoxes):
	pass


class ArraySpecOnlyBoxes(MSpec(isArray=True, scalarMode=ScalarMetaMap.noScalars), SpecOnlyBoxes):
	pass


class ArraySpecOnlyBoxesNoIntegers(MSpec(isArray=True, scalarMode=ScalarMetaMap.noScalars, integerMode=IntegerMetaMap.noIntegers), SpecOnlyBoxes):
	pass
