# coding:utf-8
import numpy as np
from sklearn.linear_model import orthogonal_mp_gram


class ApproximateKSVD(object):
    def __init__(self, n_components):
        self.components_ = None
        self.max_iter = 2
        self.tol = 1e-6
        self.n_components = n_components

    def fit(self, X):
        D = np.random.randn(self.n_components, X.shape[1])
        for i in range(self.max_iter):
            gram = D.dot(D.T)
            Xy = D.dot(X.T)
            gamma = orthogonal_mp_gram(gram, Xy).T
            e = np.linalg.norm(X - gamma.dot(D))
            if e < self.tol:
                break
            for j in range(self.n_components):
                D[j, :] = 0
                I = gamma[:, j] > 0
                if np.sum(I) == 0:
                    continue

                g = gamma[I, j].T
                d = X[I, :].T.dot(g) - gamma[I, :].dot(D).T.dot(g)
                d /= np.linalg.norm(d)
                g = X[I, :].dot(d) - gamma[I, :].dot(D).dot(d)
                D[j, :] = d
                gamma[I, j] = g.T
                e = np.linalg.norm(X - gamma.dot(D))
        self.components_ = D

    def transform(self, X):
        gram = self.components_.dot(self.components_.T)
        Xy = self.components_.dot(X.T)
        gamma = orthogonal_mp_gram(gram, Xy).T
        return gamma
