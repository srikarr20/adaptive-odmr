import pandas as pd
from adaptive_odmr.sensors.recorded import RecordedODMRSensor

def test_recorded_sensor(tmp_path):
    p=tmp_path/"x.csv"
    pd.DataFrame({"Adjusted Frequency [MHz]":[2.,1.],"Normalized Counts":[.9,1.]}).to_csv(p,index=False)
    s=RecordedODMRSensor.from_csv(p)
    assert len(s)==2
    assert s.measure(0)["frequency_mhz"]==1.0
