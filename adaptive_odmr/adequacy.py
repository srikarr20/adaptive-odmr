"""Simple measurement-model adequacy diagnostics."""
import numpy as np

def residual_diagnostics(observed,predicted,parameter_count,noise_scale=None):
    r=np.asarray(observed,float)-np.asarray(predicted,float)
    rmse=float(np.sqrt(np.mean(r*r)))
    dof=max(len(r)-parameter_count,1)
    reduced_chi2=None if noise_scale is None else float(np.sum((r/noise_scale)**2)/dof)
    lag1=0.0
    if len(r)>5 and np.std(r[:-1])>0 and np.std(r[1:])>0:
        lag1=float(np.corrcoef(r[:-1],r[1:])[0,1])
    return {"rmse":rmse,"reduced_chi2":reduced_chi2,"lag1_correlation":lag1}
