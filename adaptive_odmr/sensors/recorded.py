"""Replay a recorded ODMR trace behind the same indexed-measurement API."""
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class RecordedODMRSensor:
    frequencies_mhz: np.ndarray
    values: np.ndarray

    @classmethod
    def from_csv(cls,path,frequency_column="Adjusted Frequency [MHz]",
                 value_column="Normalized Counts"):
        d=pd.read_csv(path).sort_values(frequency_column)
        return cls(d[frequency_column].to_numpy(float),d[value_column].to_numpy(float))

    def __len__(self): return len(self.frequencies_mhz)

    def measure(self,index):
        i=int(index)
        return {"index":i,"frequency_mhz":float(self.frequencies_mhz[i]),
                "value":float(self.values[i])}
