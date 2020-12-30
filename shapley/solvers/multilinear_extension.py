import random
import numpy as np
from scipy.stats import norm
from shapley.solution_concept import SolutionConcept

class MultilinearExtension(SolutionConcept):
    r""". For details see this paper: 
    `"Paper" 
    <https://arxiv.org/abs/1306.4265>`_
    """
    def _setup(self, W: np.ndarray):
        """Creating an empty Shapley value matrix."""
        self._Phi = np.zeros(W.shape)

    def _approximate(self, W: np.ndarray, q: float):
        """Using the naive multilinear approximation method."""
        W = W / W.sum(axis=1)
        mu = np.zeros(W.shape) + np.mean(W, axis=1).reshape(-1, 1)
        std = np.zeros(W.shape) + np.std(W, axis=1).reshape(-1, 1)
        upper = (np.zeros(W.shape) + q - mu)/std
        lower = (np.zeros(W.shape) + q - W - mu)/std
        self._Phi = norm.cdf(upper, 0, 1) - norm.cdf(lower, 0, 1)
        print(self._Phi)
        self._Phi = self._Phi / np.sum(self._Phi, axis=1).reshape(-1, 1)

    def solve_game(self, W: np.ndarray, q: float):
        r"""Solving the weigted voting game(s).

        Args:
            W (Numpy array): An :math:`n \times m` matrix of voting weights for the :math:`n` games with :math:`m` players.
            q (float): Quota in the games.
        """
        self._check_quota(q)
        self._setup(W)
        self._approximate(W, q)
        self._run_sanity_check(W, self._Phi)
        self._set_average_shapley()
        self._set_shapley_entropy()

    def get_solution(self) -> np.ndarray:
        r"""Returning the solution.

        Return Types:
            Phi (Numpy array): Approximate Shapley matrix of players in the game(s) with size :math:`n \times m`.
        """
        return self._Phi
