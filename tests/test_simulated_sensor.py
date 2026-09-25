import numpy as np
from adaptive_odmr.sensors.simulated import SimulatedUncutGem

def test_uncutgem_grid():
    s=SimulatedUncutGem.uncutgem_v2_grid()
    assert len(s.frequencies_mhz)==128
    assert np.isclose(s.frequencies_mhz[0],2854.0)
    assert np.isclose(s.frequencies_mhz[-1],2885.75)

def test_measurement_contract():
    s=SimulatedUncutGem.uncutgem_v2_grid(seed=1)
    m=s.measure(10)
    assert m["index"]==10
    assert set(("index","frequency_mhz","value")).issubset(m)
