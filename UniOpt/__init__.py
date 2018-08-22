import sys
from .utils import IterableModule
from .backends.hyperopt import TPE, Random
from .backends.hyperband import HyperBand
from .backends.optunity import OptunityOptimizer as Optunity, NelderMead, Sobol, ParticleSwarm, CMA_ES
from .backends.bayesian import Bayesian
from .backends.ecabc import BeeColony
#from .backends.SMAC import SMAC
from .backends.GPyOpt import GPyOptOptimizer
from .backends.yabox import Yabox
from .backends.hyperengine import HyperEngineBayesian, HyperEnginePortfolio
from .backends.skopt import SKOptBayesian, SKOptForest, SKOptGBTree, SKOptExtraTrees
from .backends.pyshac import PySHAC
from .backends.rbfopt import Gutmann, MSRSM
from .backends.simple_spearmint import SimpleSpearmint
from .backends.EvoFuzzy import EvoFuzzy
from .backends.ypde import YPDE
from .backends.SOpt import SOptSGA, SOptGA
from .backends.pySOT import PySOT
from .backends.BayTune import BayTuneGP, BayTuneGCP, BayTuneGPEi, BayTuneGCPEi
from .backends.RoBO import RoBOForest, RoBOGP


class Optimizers(IterableModule):
	__all__ = ("TPE", "Random", "Optunity", "ParticleSwarm", "Sobol", "NelderMead", "BeeColony", "Yabox", "PySHAC", "HyperEngineBayesian", "HyperEnginePortfolio", "SKOptBayesian", "Forest", "GBTree", "ExtraTrees", "MSRSM", "Gutmann", "HyperBand", "GPyOpt", "Bayesian", "PySOT")
	TPE = TPE
	Random = Random
	Optunity = Optunity
	Bayesian = Bayesian
	BeeColony = BeeColony
	GPyOpt = GPyOptOptimizer
	Yabox = Yabox
	HyperEngineBayesian = HyperEngineBayesian
	HyperEnginePortfolio = HyperEnginePortfolio

	HyperBand = HyperBand

	MSRSM = MSRSM
	Gutmann = Gutmann

	SKOptBayesian = SKOptBayesian
	Forest = SKOptForest
	GBTree = SKOptGBTree
	ExtraTrees = SKOptExtraTrees

	PySHAC = PySHAC

	ParticleSwarm = ParticleSwarm
	Sobol = Sobol
	NelderMead = NelderMead
	CMA_ES = CMA_ES  # seems to be broken in optunity - doesn't catch ConstraintViolation

	#SMAC = SMAC
	Spearmint = SimpleSpearmint # very slow, broken (predicts the same points) and proprietary

	EvoFuzzy = EvoFuzzy
	YPDE = YPDE

	SOptSGA = SOptSGA
	SOptGA = SOptGA

	PySOT = PySOT

	BayTuneGP = BayTuneGP

	RoBOForest = RoBOForest
	RoBOGP = RoBOGP


sys.modules[__name__] = Optimizers(__name__)
