import unittest
import numpy as np
from cybersecurity_app.core.ensemble import BaseModel, Ensemble

class MockModel(BaseModel):
    def fit(self, X, y):
        pass

    def predict(self, X):
        return np.ones(X.shape[0])

class TestEnsemble(unittest.TestCase):
    def test_ensemble_predict(self):
        X = np.array([[1, 2], [3, 4]])
        models = [MockModel(), MockModel()]
        ensemble = Ensemble(models)
        predictions = ensemble.predict(X)
        self.assertTrue(np.array_equal(predictions, np.ones(X.shape[0])))

if __name__ == '__main__':
    unittest.main()
