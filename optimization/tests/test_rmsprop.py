import numpy as np
import pytest

from optimization.optimization_function import quad1, quad2, quad5, Rosenbrock
from optimization.unconstrained.rmsprop import RMSProp


def test_RmsProp_quadratic():
    x, _ = RMSProp(quad1).minimize()
    np.allclose(x, quad1.x_star())

    x, _ = RMSProp(quad2).minimize()
    np.allclose(x, quad2.x_star())

    x, _ = RMSProp(quad5).minimize()
    np.allclose(x, quad5.x_star())


def test_RmsProp_Rosenbrock():
    obj = Rosenbrock()
    x, _ = RMSProp(obj, nesterov_momentum=True).minimize()
    assert np.allclose(x, obj.x_star(), rtol=1e-3)


if __name__ == "__main__":
    pytest.main()
