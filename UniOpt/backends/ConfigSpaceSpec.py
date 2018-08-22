from ..imports import *
from ..core.HyperparamVector import HyperparamVector
from ..core.MetaSpec import *


from lazily.ConfigSpace import ConfigurationSpace
from lazily.ConfigSpace.hyperparameters import UniformIntegerHyperparameter, UniformFloatHyperparameter, NormalFloatHyperparameter, NormalIntegerHyperparameter, CategoricalHyperparameter, Constant


class ConfigSpaceSpecVec(HyperparamVector):
	@classmethod
	def dict2native(cls, dic: typing.Dict[str, typing.Any], spec) -> typing.Iterable[typing.Any]:
		if dic:
			cs = ConfigurationSpace()
			print(dic, list(dic.values()))
			cs.add_hyperparameters(dic.values())
			return cs
		else:
			return None

class ConfigSpaceSpec(MSpec()):
	hyperparamsVectorType = HyperparamVector
	#hyperparamsVectorType = HyperparamArray
	hyperparamsSpecType = ConfigSpaceSpecVec

	class HyperparamsSpecsConverters:
		randint = lambda k, dist, tp: UniformIntegerHyperparameter(k, dist.a, dist.b)
		def uniform(k, dist, tp):
			ctor=(UniformIntegerHyperparameter if tp is int else UniformFloatHyperparameter)
			return ctor(name=k, lower=dist.ppf(0), upper=dist.ppf(1))
		#def norm(k, dist, tp):
		#	ctor=(NormalIntegerHyperparameter if tp is int else NormalFloatHyperparameter)
		#	return ctor(k, dist.mean(), dist.std(), default_value=tp(dist.mean()))
		_categorical = lambda k, categories: CategoricalHyperparameter(k, categories)

	def scalarProcessor(self, i, k, v):
		return Constant(k, v)
