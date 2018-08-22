from ..imports import *
from ..core.Spec import *
from ..core.Optimizer import GenericOptimizer, PointsStorage
from ..core.MetaSpec import *
from ..core.ProgressReporter import ProgressReporter

from numpy import ndarray
from lazily import simple_spearmint


class SimpleSpearmintSpec(MSpec(scalarMode=ScalarMetaMap.degenerateCategory, integerMode=IntegerMetaMap.noIntegers)):
	class HyperparamsSpecsConverters:
		randint = lambda k, dist, tp: __class__._categorical(k, range(dist.a, dist.b))
		# uniform=lambda k, dist, tp: {"type": tp.__name__, "min": dist.a, "max": dist.b}
		uniform = lambda k, dist, tp: {"type": "float", "min": dist.ppf(0), "max": dist.ppf(1)} # a bug in simple_spearmint: float is used instead of round
		_categorical = lambda k, categories: {"type": "enum", "options": categories}


class SimpleSpearmint(GenericOptimizer):
	specType = SimpleSpearmintSpec

	def __init__(self, blackBoxFunc: typing.Callable, spaceSpec: typing.Mapping[str, object], iters: int = 1000, jobs: int = 3, pointsStorage: PointsStorage = None, seedIters: int = 5) -> None:
		super().__init__(blackBoxFunc, spaceSpec, iters, jobs, pointsStorage)

		self.seedIters = seedIters

	def prepareScoring(self, spaceSpec):
		solver = simple_spearmint.SimpleSpearmint(spaceSpec)
		return (self.iters, "SimpleSpearmint", solver)

	def invokeScoring(self, fn: typing.Callable, pb: ProgressReporter, solver):
		def spearmintIteration(suggester):
			suggestion = suggester()
			solver.update(suggestion, fn(suggestion)[0])

		pb.print("Bootstrapping...")
		for i in range(self.seedIters):
			spearmintIteration(solver.suggest_random)

		pb.print("Started predicting")
		for i in range(self.iters - self.seedIters):
			spearmintIteration(solver.suggest)

		self.details = solver
		best, _ = solver.get_best_parameters()
		return best
