"""Minimal use of the Measurement Twin with a recorded ODMR trace."""
import argparse
import numpy as np

from adaptive_odmr.discovery import uniform_indices
from adaptive_odmr.sensors.recorded import RecordedODMRSensor
from adaptive_odmr.twin import ODMRMeasurementTwin

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--seed-points",type=int,default=15)
    ap.add_argument("--steps",type=int,default=10)
    args=ap.parse_args()

    sensor=RecordedODMRSensor.from_csv(args.csv)
    twin=ODMRMeasurementTwin(sensor)

    for i in uniform_indices(len(sensor),args.seed_points):
        twin.observe(i)

    _,state=twin.update()
    print("initial:",state)

    for _ in range(args.steps):
        twin.step()
        _,state=twin.update()
        print(
            f"N={len(state.measured_indices):3d} "
            f"model={state.selected_model:3s} "
            f"f0={state.estimated_primary_center_mhz:.6f} MHz "
            f"rmse={state.rmse:.6g} "
            f"adequacy={state.adequacy_status:20s} "
            f"next={state.next_index}"
        )

if __name__=="__main__":
    main()
