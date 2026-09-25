"""Adaptive setting-selection utilities."""
import numpy as np
from .models import single_lorentzian, single_lorentzian_slope, double_lorentzian, double_lorentzian_slope

def information_score(frequencies,fit):
    f=np.asarray(frequencies,float); p=fit.params.copy(); eps=1e-3
    if fit.name=="M1": fn=lambda q:single_lorentzian(f,q); j=2
    elif fit.name=="M1S":
        center=float(np.mean(f)); fn=lambda q:single_lorentzian_slope(f,q,center); j=3
    elif fit.name=="M2": fn=lambda q:double_lorentzian(f,q); j=2 if p[1]>=p[4] else 5
    else:
        center=float(np.mean(f)); fn=lambda q:double_lorentzian_slope(f,q,center); j=3 if p[2]>=p[5] else 6
    pp=p.copy(); pm=p.copy(); pp[j]+=eps; pm[j]-=eps
    return ((fn(pp)-fn(pm))/(2*eps))**2

def choose_next(frequencies,fit,measured):
    score=information_score(frequencies,fit)
    score[np.asarray(measured,dtype=int)]=-np.inf
    return int(np.argmax(score))
