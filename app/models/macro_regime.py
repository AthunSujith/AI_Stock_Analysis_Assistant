from hmmlearn.hmm import GaussianHMM
import numpy as np

class MacroRegime:
    def __init__(self):
        self.model = GaussianHMM(n_components=4)

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)
