import numpy as np
import pytest

from optiml.optimization.unconstrained import quad2, quad1, Rosenbrock
from optiml.optimization.unconstrained.line_search import SteepestGradientDescent
from optiml.optimization.unconstrained.stochastic import StochasticGradientDescent


def test_SteepestGradientDescent_quadratic():
    assert np.allclose(SteepestGradientDescent(f=quad1, x=np.random.uniform(size=2)).minimize().x, quad1.x_star())
    assert np.allclose(SteepestGradientDescent(f=quad2, x=np.random.uniform(size=2)).minimize().x, quad2.x_star())


def test_SteepestGradientDescent_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(SteepestGradientDescent(f=rosen, x=np.random.uniform(size=2)).minimize().x, rosen.x_star())


def test_GradientDescent_quadratic():
    assert np.allclose(StochasticGradientDescent(f=quad1, x=np.random.uniform(size=2)).minimize().x, quad1.x_star())
    assert np.allclose(StochasticGradientDescent(f=quad2, x=np.random.uniform(size=2)).minimize().x, quad2.x_star())


def test_GradientDescent_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(f=rosen, x=np.random.uniform(size=2)).minimize().x,
                       rosen.x_star(), rtol=0.1)


def test_GradientDescent_standard_momentum_quadratic():
    assert np.allclose(StochasticGradientDescent(f=quad1, x=np.random.uniform(size=2),
                                                 momentum_type='standard').minimize().x, quad1.x_star())
    assert np.allclose(StochasticGradientDescent(f=quad2, x=np.random.uniform(size=2),
                                                 momentum_type='standard').minimize().x, quad2.x_star())


def test_GradientDescent_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(f=rosen, x=np.random.uniform(size=2),
                                                 momentum_type='standard').minimize().x, rosen.x_star())


def test_GradientDescent_Nesterov_momentum_quadratic():
    assert np.allclose(StochasticGradientDescent(f=quad1, x=np.random.uniform(size=2),
                                                 momentum_type='nesterov').minimize().x, quad1.x_star())
    assert np.allclose(StochasticGradientDescent(f=quad2, x=np.random.uniform(size=2),
                                                 momentum_type='nesterov').minimize().x, quad2.x_star())


def test_GradientDescent_Nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(f=rosen, x=np.random.uniform(size=2),
                                                 momentum_type='nesterov').minimize().x, rosen.x_star())


if __name__ == "__main__":
    pytest.main()