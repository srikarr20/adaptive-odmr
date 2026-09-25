import numpy as np, pandas as pd
from adaptive_odmr.sensors.recorded import RecordedODMRSensor
from benchmarks.run_experiment11 import single_model_aqie, model_aware

def fixture(tmp_path):
    f=np.linspace(2800,2940,40)
    y=1-.06/(1+((f-2870)/3)**2)-.03/(1+((f-2862)/4)**2)
    p=tmp_path/"fixture.csv"
    pd.DataFrame({"Adjusted Frequency [MHz]":f,"Normalized Counts":y}).to_csv(p,index=False)
    return RecordedODMRSensor.from_csv(p)

def test_benchmark_strategies_respect_budget(tmp_path):
    s=fixture(tmp_path)
    for fn in (single_model_aqie,model_aware):
        idx,fit=fn(s,20)
        assert len(idx)==20
        assert len(set(idx))==20
        assert np.isfinite(fit.primary_center_mhz)
