from ..imports import *
from ..core.SpecOnlyBoxes import ArraySpecOnlyBoxes
from ..core.Optimizer import GenericOptimizer, PointsStorage
from ..core.ProgressReporter import ProgressReporter
from ..utils import notInitializedFunction
from ..utils.coresCount import getCoreCount

from math import sqrt
import warnings

from ..core.Spec import HyperparamDefinition
import typing

from lazily.ecabc import abc

class BeeColonyGridSpec(ArraySpecOnlyBoxes):
	class HyperparamsSpecsConverters:
		def uniform(k: str, dist, tp: type):
			return [tp.__name__, (dist.ppf(0), dist.ppf(1))]


maxDefaultAmountOfEmployers = 50

class BeeColony(GenericOptimizer):
	specType = BeeColonyGridSpec

	def __init__(self, blackBoxFunc: typing.Callable, spaceSpec: typing.Mapping[str, object], iters: int = 1000, jobs: int = 1, pointsStorage: PointsStorage = None, numEmployers=None) -> None:
		if jobs is None:
			self.jobs = getCoreCount()
		
		if jobs != 1:
			warnings.warn("Multiprocessing is not supported for this solver: it uses `pickle` and you will get AttributeError: Can't pickle local object 'BeeColony.invokeScoring.<locals>.abcScore' . Setting count of jobs to 1")
			jobs = 1
		
		super().__init__(blackBoxFunc, spaceSpec, iters, jobs, pointsStorage)
		
		if numEmployers is None:
			numEmployers = min(round(sqrt(iters)), maxDefaultAmountOfEmployers)

		self.numEmployers = numEmployers

		self.generations = iters // numEmployers

	def prepareScoring(self, spaceSpec: typing.Iterable[typing.List[typing.Union[str, typing.Tuple[float, float], typing.Tuple[int, int]]]]) -> typing.Tuple[int, str, typing.Iterable[typing.List[typing.Union[str, typing.Tuple[float, float], typing.Tuple[int, int]]]]]:
		colony = abc.ABC(fitness_fxn=notInitializedFunction, value_ranges=spaceSpec, processes=self.jobs)
		colony._num_employers = self.numEmployers # not used for anything but tracking the number of employers to be initialized. create_employers creates colony._num_employers employers
		return (self.iters, "BeeColony", colony)

	def injectPoints(self, pointz, bestPointIndex, colony, initialize=False):
		if initialize:
			for employersInitialized, p in enumerate(pointz):
				if employersInitialized >= colony._num_employers:
					break
				employer = abc.EmployerBee(p[0])
				employer.score = p[1][0]
				colony._employers.append(employer)
			colony._num_employers = colony._num_employers - employersInitialized # rest of points, will be inserted by create_employers. create_employers creates colony._num_employers employers
		else:
			raise NotImplementedException("Mixing values into partially initialized _employers is not yet implemented")

	def invokeScoring(self, fn: typing.Callable, pb: ProgressReporter, colony) -> typing.List[typing.Union[float, int]]:
		def abcScore(hyperparamsDict):
			return fn(hyperparamsDict)[0]

		colony._fitness_fxn = abcScore
		#colony._minimize = True
		#colony._args # TODO: keyword arguments
		colony.create_employers() # inserting missing employers. create_employers creates colony._num_employers employers
		colony._num_employers = self.numEmployers
		for i in range(self.generations):
			colony.run_iteration()
		return colony.best_performer[1]