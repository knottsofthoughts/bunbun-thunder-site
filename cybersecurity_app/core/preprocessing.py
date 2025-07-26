import numpy as np

def clean_data(data):
    # Simple example: remove null values
    if isinstance(data, list) and all(isinstance(i, list) for i in data):
        return [row for row in data if not np.isnan(row).any()]
    return data

def normalize_data(data):
    # Simple example: scale to [0, 1]
    if isinstance(data, list) and all(isinstance(i, list) for i in data):
        data = np.array(data)
        min_val = np.min(data, axis=0)
        max_val = np.max(data, axis=0)
        return (data - min_val) / (max_val - min_val)
    return data

def scale_data(data):
    # Simple example: standardize to mean 0, variance 1
    if isinstance(data, list) and all(isinstance(i, list) for i in data):
        data = np.array(data)
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        return (data - mean) / std
    return data
