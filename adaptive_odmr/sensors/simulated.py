"""Synthetic ODMR sensors used for reproducible development tests."""
from dataclasses import dataclass
import numpy as np

def lorentzian_dip(f, baseline, contrast, f0, gamma):
    f=np.asarray(f,float)
    return baseline-contrast/(1.0+((f-f0)/gamma)**2)

@dataclass
class SimulatedUncutGem:
    frequencies_mhz: np.ndarray
    f0_mhz: float=2870.0
    gamma_mhz: float=1.6
    baseline_mv: float=1380.0
    contrast_mv: float=55.0
    sample_sigma_mv: float=5.0
    accepted_samples: int=6
    adc_ceiling_mv: float=1500.0
    seed: int=42

    def __post_init__(self):
        self.frequencies_mhz=np.asarray(self.frequencies_mhz,float)
        self.rng=np.random.default_rng(self.seed)

    @classmethod
    def uncutgem_v2_grid(cls, **kwargs):
        return cls(2854.0+0.25*np.arange(128), **kwargs)

    def expected(self,index):
        return float(lorentzian_dip(self.frequencies_mhz[index],self.baseline_mv,
            self.contrast_mv,self.f0_mhz,self.gamma_mhz))

    def measure(self,index):
        vals=[]; rejected=0; mu=self.expected(index)
        while len(vals)<self.accepted_samples:
            x=float(self.rng.normal(mu,self.sample_sigma_mv))
            if x<=self.adc_ceiling_mv: vals.append(x)
            else: rejected+=1
        return {"index":int(index),"frequency_mhz":float(self.frequencies_mhz[index]),
                "value":float(np.mean(vals)),"rejected_samples":rejected}
