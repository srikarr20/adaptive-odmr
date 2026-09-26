import numpy as np

from adaptive_odmr.discovery import uniform_indices
from adaptive_odmr.sensors.simulated import SimulatedUncutGem
from adaptive_odmr.twin import ODMRMeasurementTwin

def test_measurement_twin_reconciles_and_selects_next():
    sensor=SimulatedUncutGem.uncutgem_v2_grid(seed=7)
    twin=ODMRMeasurementTwin(sensor)
    for i in uniform_indices(len(sensor.frequencies_mhz),15):
        twin.observe(i)
    fit,state=twin.update()
    assert state.selected_model in {"M1","M1S","M2","M2S"}
    assert np.isfinite(state.estimated_primary_center_mhz)
    assert np.isfinite(state.rmse)
    assert state.adequacy_status in {"NOMINAL","REVIEW","STRUCTURED_RESIDUAL"}
    assert state.next_index not in state.measured_indices
    n=len(state.measured_indices)
    twin.step()
    assert len(state.measured_indices)==n+1
