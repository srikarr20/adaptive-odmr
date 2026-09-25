"""Evaluation metrics. Keep discrete-grid and continuous-fit references separate."""
def absolute_error_khz(estimate_mhz,reference_mhz):
    return abs(float(estimate_mhz)-float(reference_mhz))*1000.0
