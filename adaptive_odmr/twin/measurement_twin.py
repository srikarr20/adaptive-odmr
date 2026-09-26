"""Thin measurement-twin abstraction over the existing Adaptive ODMR stack.

This module does not replace the existing controller. It exposes the already
implemented model -> measure -> reconcile -> assess -> select loop explicitly.
"""
import numpy as np

from adaptive_odmr.models import select_model
from adaptive_odmr.selection import choose_next
from .reconcile import reconcile
from .state import MeasurementTwinState

class ODMRMeasurementTwin:
    def __init__(self, sensor, model_names=("M1","M1S","M2","M2S")):
        self.sensor=sensor
        self.model_names=model_names
        self.state=MeasurementTwinState()

    def observe(self,index):
        m=self.sensor.measure(int(index))
        self.state.measured_indices.append(int(index))
        self.state.observed_values.append(float(m["value"]))
        return m

    def update(self):
        if len(self.state.measured_indices)<8:
            raise ValueError("Need at least 8 observations for the current model bank.")
        idx=self.state.measured_indices
        f=np.asarray(self.sensor.frequencies_mhz)[idx]
        y=np.asarray(self.state.observed_values,float)
        fit,_=select_model(f,y,self.model_names)
        _,diag,status=reconcile(f,y,fit)
        self.state.selected_model=fit.name
        self.state.estimated_primary_center_mhz=fit.primary_center_mhz
        self.state.rmse=diag["rmse"]
        self.state.lag1_correlation=diag["lag1_correlation"]
        self.state.adequacy_status=status
        self.state.next_index=choose_next(self.sensor.frequencies_mhz,fit,idx)
        return fit,self.state

    def step(self,index=None):
        if index is None:
            if self.state.next_index is None:
                raise ValueError("Provide an initial index or call update() after seeding.")
            index=self.state.next_index
        measurement=self.observe(index)
        return measurement
