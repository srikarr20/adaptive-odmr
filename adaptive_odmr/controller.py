"""Discovery-to-adaptive controller.

This is the canonical refactored implementation, not a claim that it is the
untouched source used in the historical interactive experiments.
"""
import numpy as np
from .discovery import uniform_indices, nearest_unmeasured, farthest_unmeasured
from .models import select_model
from .selection import choose_next

class AdaptiveODMRController:
    def __init__(self,sensor,discovery_points=15,localization_points=6,
                 model_names=("M1","M1S","M2","M2S"),explore_every=6):
        self.sensor=sensor
        self.discovery_points=discovery_points
        self.localization_points=localization_points
        self.model_names=model_names
        self.explore_every=explore_every

    def run(self,budget):
        n=len(self.sensor)
        idx=uniform_indices(n,min(self.discovery_points,budget))
        obs=[self.sensor.measure(i) for i in idx]
        values=[m["value"] for m in obs]

        if len(idx)<budget:
            center=idx[int(np.argmin(values))]
            for i in nearest_unmeasured(center,idx,n,min(self.localization_points,budget-len(idx))):
                idx.append(i); values.append(self.sensor.measure(i)["value"])

        step=0
        while len(idx)<budget:
            f=np.asarray(self.sensor.frequencies_mhz)[idx]
            fit,_=select_model(f,values,self.model_names)
            if self.explore_every and step>0 and step%self.explore_every==0:
                nxt=farthest_unmeasured(idx,n)
            else:
                nxt=choose_next(self.sensor.frequencies_mhz,fit,idx)
            idx.append(nxt); values.append(self.sensor.measure(nxt)["value"]); step+=1

        f=np.asarray(self.sensor.frequencies_mhz)[idx]
        fit,allfits=select_model(f,values,self.model_names)
        return {"indices":idx,"values":values,"fit":fit,"candidate_fits":allfits}
