import unittest
import numpy as np
from cybersecurity_app.core.preprocessing import clean_data, normalize_data, scale_data

class TestPreprocessing(unittest.TestCase):
    def test_clean_data(self):
        data = [[1, 2], [np.nan, 4], [5, 6]]
        cleaned = clean_data(data)
        self.assertEqual(len(cleaned), 2)

    def test_normalize_data(self):
        data = [[1, 2], [3, 4]]
        normalized = normalize_data(data)
        self.assertTrue(np.all(normalized >= 0) and np.all(normalized <= 1))

    def test_scale_data(self):
        data = [[1, 2], [3, 4]]
        scaled = scale_data(data)
        self.assertTrue(np.allclose(np.mean(scaled, axis=0), 0))
        self.assertTrue(np.allclose(np.std(scaled, axis=0), 1))

if __name__ == '__main__':
    unittest.main()
