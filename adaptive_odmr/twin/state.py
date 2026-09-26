"""State carried by the ODMR measurement twin."""
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MeasurementTwinState:
    measured_indices: list[int] = field(default_factory=list)
    observed_values: list[float] = field(default_factory=list)
    selected_model: Optional[str] = None
    estimated_primary_center_mhz: Optional[float] = None
    rmse: Optional[float] = None
    lag1_correlation: Optional[float] = None
    adequacy_status: str = "UNINITIALIZED"
    next_index: Optional[int] = None
