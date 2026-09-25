#!/usr/bin/env python3
"""Experiment 11 runner.

Implements the benchmark frozen in benchmarks/experiment11_frozen.yaml.
Do not change benchmark rules here after viewing real-data results; create a
new benchmark version instead.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

from adaptive_odmr.sensors.recorded import RecordedODMRSensor
from adaptive_odmr.discovery import uniform_indices, nearest_unmeasured, farthest_unmeasured
from adaptive_odmr.models import fit_model, select_model
from adaptive_odmr.selection import choose_next
from adaptive_odmr.metrics import absolute_error_khz

DISCRETE_REF=2869.000000
FULLFIT_REF=2869.729971034267
BUDGETS=(20,30,40,50,60,80)
SEED=20260925
RANDOM_REPS=100
CATASTROPHIC_MHZ=10.0

def values(sensor,idx):
    return [sensor.measure(i)["value"] for i in idx]

def estimate_model(sensor,idx,names):
    f=np.asarray(sensor.frequencies_mhz)[idx]
    y=values(sensor,idx)
    fit,_=select_model(f,y,names)
    return fit

def uniform_fixed(sensor,N):
    idx=uniform_indices(len(sensor),N)
    fit=estimate_model(sensor,idx,("M1","M1S","M2","M2S"))
    return idx,fit

def random_subset(sensor,N,rng):
    idx=list(np.sort(rng.choice(len(sensor),N,replace=False)))
    fit=estimate_model(sensor,idx,("M1","M1S","M2","M2S"))
    return idx,fit

def single_model_aqie(sensor,N):
    idx=uniform_indices(len(sensor),min(15,N))
    while len(idx)<N:
        f=np.asarray(sensor.frequencies_mhz)[idx]
        y=values(sensor,idx)
        fit=fit_model("M1",f,y)
        nxt=choose_next(sensor.frequencies_mhz,fit,idx)
        idx.append(nxt)
    f=np.asarray(sensor.frequencies_mhz)[idx]
    fit=fit_model("M1",f,values(sensor,idx))
    return idx,fit

def model_aware(sensor,N):
    idx=uniform_indices(len(sensor),min(15,N))
    y=values(sensor,idx)
    if len(idx)<N:
        center=idx[int(np.argmin(y))]
        for i in nearest_unmeasured(center,idx,len(sensor),min(6,N-len(idx))):
            idx.append(i); y.append(sensor.measure(i)["value"])
    adaptive_step=0
    while len(idx)<N:
        f=np.asarray(sensor.frequencies_mhz)[idx]
        fit,_=select_model(f,y,("M1","M1S","M2","M2S"))
        if adaptive_step>0 and adaptive_step%6==0:
            nxt=farthest_unmeasured(idx,len(sensor))
        else:
            nxt=choose_next(sensor.frequencies_mhz,fit,idx)
        idx.append(nxt); y.append(sensor.measure(nxt)["value"])
        adaptive_step+=1
    f=np.asarray(sensor.frequencies_mhz)[idx]
    fit,_=select_model(f,y,("M1","M1S","M2","M2S"))
    return idx,fit

def record(N,strategy,rep,fit):
    est=fit.primary_center_mhz
    egrid=absolute_error_khz(est,DISCRETE_REF)
    efull=absolute_error_khz(est,FULLFIT_REF)
    return {
      "N":N,"strategy":strategy,"rep":rep,"estimate_mhz":est,
      "selected_model":fit.name,
      "error_vs_discrete_khz":egrid,
      "error_vs_fullfit_khz":efull,
      "catastrophic_lock_on":bool(efull>1000*CATASTROPHIC_MHZ),
    }

def summarize(df):
    rows=[]
    for (N,s),g in df.groupby(["N","strategy"],sort=True):
        z=g.error_vs_fullfit_khz.to_numpy()
        rows.append({
          "N":N,"strategy":s,"runs":len(g),
          "median_error_khz":float(np.median(z)),
          "q25_error_khz":float(np.percentile(z,25)),
          "q75_error_khz":float(np.percentile(z,75)),
          "iqr_error_khz":float(np.percentile(z,75)-np.percentile(z,25)),
          "p90_error_khz":float(np.percentile(z,90)),
          "catastrophic_lock_on_rate":float(g.catastrophic_lock_on.mean()),
        })
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--out",default="results/experiment11")
    ap.add_argument("--quick",action="store_true",help="development smoke test only; NOT benchmark result")
    args=ap.parse_args()
    sensor=RecordedODMRSensor.from_csv(args.csv)
    if len(sensor)!=297 and not args.quick:
        raise ValueError(f"Frozen benchmark expects 297 rows, got {len(sensor)}")
    budgets=(20,) if args.quick else BUDGETS
    reps=3 if args.quick else RANDOM_REPS
    rng=np.random.default_rng(SEED)
    rows=[]
    for N in budgets:
        _,fit=uniform_fixed(sensor,N); rows.append(record(N,"uniform_fixed",0,fit))
        for r in range(reps):
            _,fit=random_subset(sensor,N,rng); rows.append(record(N,"random",r,fit))
        _,fit=single_model_aqie(sensor,N); rows.append(record(N,"aqie_single_model",0,fit))
        _,fit=model_aware(sensor,N); rows.append(record(N,"discovery_model_aware",0,fit))
    df=pd.DataFrame(rows); summary=summarize(df)
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df.to_csv(out/"trials.csv",index=False)
    summary.to_csv(out/"summary.csv",index=False)
    metadata={"quick":args.quick,"seed":SEED,"random_repetitions":reps,
              "discrete_reference_mhz":DISCRETE_REF,
              "fullfit_reference_mhz":FULLFIT_REF,
              "catastrophic_threshold_mhz":CATASTROPHIC_MHZ}
    (out/"metadata.json").write_text(json.dumps(metadata,indent=2))
    print(summary.to_string(index=False))

if __name__=="__main__":
    main()
