"""ODMR response models and complexity-penalized model selection."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import least_squares

def single_lorentzian(f,p):
    b,c,f0,g=p
    return b-c/(1+((np.asarray(f)-f0)/g)**2)

def single_lorentzian_slope(f,p,center):
    b,s,c,f0,g=p
    f=np.asarray(f)
    return b+s*(f-center)-c/(1+((f-f0)/g)**2)

def double_lorentzian(f,p):
    b,c1,f1,g1,c2,f2,g2=p
    f=np.asarray(f)
    return b-c1/(1+((f-f1)/g1)**2)-c2/(1+((f-f2)/g2)**2)

def double_lorentzian_slope(f,p,center):
    b,s,c1,f1,g1,c2,f2,g2=p
    f=np.asarray(f)
    return b+s*(f-center)-c1/(1+((f-f1)/g1)**2)-c2/(1+((f-f2)/g2)**2)

@dataclass
class Fit:
    name:str
    params:np.ndarray
    rss:float
    aicc:float

    @property
    def primary_center_mhz(self):
        p=self.params
        if self.name=="M1": return float(p[2])
        if self.name=="M1S": return float(p[3])
        if self.name=="M2": return float(p[2] if p[1]>=p[4] else p[5])
        return float(p[3] if p[2]>=p[5] else p[6])

def _aicc(rss,n,k):
    aic=n*np.log(max(rss/n,1e-15))+2*k
    return aic+(2*k*(k+1)/(n-k-1) if n>k+1 else 1e6)

def fit_model(name,f,y):
    f=np.asarray(f,float); y=np.asarray(y,float); center=float(np.mean(f))
    b=float(np.percentile(y,85)); f0=float(f[np.argmin(y)]); c=max(.002,b-float(y.min()))
    if name=="M1":
        fn=single_lorentzian; p0=[b,c,f0,4]; lo=[.5,0,f.min(),.1]; hi=[1.6,1,f.max(),100]
    elif name=="M1S":
        fn=lambda x,p:single_lorentzian_slope(x,p,center); p0=[b,0,c,f0,4]
        lo=[.5,-.01,0,f.min(),.1]; hi=[1.6,.01,1,f.max(),100]
    elif name=="M2":
        fn=double_lorentzian; p0=[b,.7*c,f0,3,.5*c,max(f.min(),f0-6),3]
        lo=[.5,0,f.min(),.1,0,f.min(),.1]; hi=[1.6,1,f.max(),100,1,f.max(),100]
    elif name=="M2S":
        fn=lambda x,p:double_lorentzian_slope(x,p,center); p0=[b,0,.7*c,f0,3,.5*c,max(f.min(),f0-6),3]
        lo=[.5,-.01,0,f.min(),.1,0,f.min(),.1]; hi=[1.6,.01,1,f.max(),100,1,f.max(),100]
    else: raise ValueError(name)
    r=least_squares(lambda p:fn(f,p)-y,p0,bounds=(lo,hi),max_nfev=3000)
    rss=float(np.sum((y-fn(f,r.x))**2))
    return Fit(name,np.asarray(r.x),rss,_aicc(rss,len(y),len(r.x)))

def select_model(f,y,names=("M1","M1S","M2","M2S")):
    fits=[fit_model(n,f,y) for n in names]
    return min(fits,key=lambda z:z.aicc),fits
