"""Prediction-versus-observation reconciliation using existing ODMR models."""
import numpy as np

from adaptive_odmr.adequacy import residual_diagnostics
from adaptive_odmr.models import (
    single_lorentzian,
    single_lorentzian_slope,
    double_lorentzian,
    double_lorentzian_slope,
)

def predict(frequencies_mhz, fit):
    f=np.asarray(frequencies_mhz,float)
    p=fit.params
    center=float(np.mean(f))
    if fit.name=="M1":
        return single_lorentzian(f,p)
    if fit.name=="M1S":
        return single_lorentzian_slope(f,p,center)
    if fit.name=="M2":
        return double_lorentzian(f,p)
    if fit.name=="M2S":
        return double_lorentzian_slope(f,p,center)
    raise ValueError(f"Unsupported model {fit.name}")

def reconcile(frequencies_mhz, observed, fit):
    predicted=predict(frequencies_mhz,fit)
    diag=residual_diagnostics(observed,predicted,len(fit.params))
    # Deliberately conservative qualitative state. This is a diagnostic flag,
    # not a statistically calibrated acceptance test.
    lag=abs(diag["lag1_correlation"])
    if lag>=0.70:
        status="STRUCTURED_RESIDUAL"
    elif lag>=0.40:
        status="REVIEW"
    else:
        status="NOMINAL"
    return predicted,diag,status
