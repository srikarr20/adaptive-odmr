"""Discovery policies that precede model-directed exploitation."""
import numpy as np

def uniform_indices(n_points,budget):
    return list(np.unique(np.linspace(0,n_points-1,budget,dtype=int)))

def nearest_unmeasured(center,measured,n_points,count):
    measured=set(map(int,measured))
    remaining=[i for i in range(n_points) if i not in measured]
    return sorted(remaining,key=lambda i:abs(i-center))[:count]

def farthest_unmeasured(measured,n_points):
    measured=list(map(int,measured))
    remaining=[i for i in range(n_points) if i not in measured]
    if not remaining: return None
    return max(remaining,key=lambda i:min(abs(i-j) for j in measured))
