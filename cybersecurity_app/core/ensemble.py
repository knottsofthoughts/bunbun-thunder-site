import numpy as np

class BaseModel:
    def __init__(self, C=1.0, penalty='l2'):
        self.C = C
        self.penalty = penalty

    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)

class Ensemble:
    def __init__(self, models):
        self.models = models

    def fit(self, X, y):
        for model in self.models:
            model.fit(X, y)

    def predict(self, X):
        predictions = np.array([model.predict(X) for model in self.models])
        return np.mean(predictions, axis=0)
