import numpy as np
import pytest

from optimization_test_functions import *
from unconstrained.newton import Newton


def test_quadratic():
    x0 = np.random.standard_normal(2).reshape((2, 1))

    x, status = Newton(gen_quad_1, x0)
    assert np.allclose(x, [[2.1875], [1.5625]])
    assert status is 'optimal'

    x, status = Newton(gen_quad_2, x0)
    assert np.allclose(x, [[4.0625], [3.4375]])
    assert status is 'optimal'

    x, status = Newton(gen_quad_5, x0)
    assert np.allclose(x, [[3.7625], [3.7375]])
    assert status is 'optimal'


def test_Rosenbrock():
    x0 = np.random.standard_normal(2).reshape((2, 1))

    x, status = Newton(Rosenbrock(), x0)
    assert np.allclose(x, [[1], [1]])
    assert status is 'optimal'


if __name__ == "__main__":
    pytest.main()
