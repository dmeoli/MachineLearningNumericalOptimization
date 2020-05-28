import numpy as np
import pytest

from optiml.opti import quad1, quad2
from optiml.opti.unconstrained import Rosenbrock
from optiml.opti.unconstrained import ProximalBundle


def test_quadratic():
    assert np.allclose(ProximalBundle(f=quad1, x=np.random.uniform(size=2)).minimize().x, quad1.x_star())
    assert np.allclose(ProximalBundle(f=quad2, x=np.random.uniform(size=2)).minimize().x, quad2.x_star(), rtol=0.1)


def test_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(ProximalBundle(f=rosen, x=np.random.uniform(size=2)).minimize().x, rosen.x_star(), rtol=0.1)


def test_standard_momentum_quadratic():
    assert np.allclose(ProximalBundle(f=quad1, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(ProximalBundle(f=quad2, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       quad2.x_star(), rtol=0.1)


def test_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(ProximalBundle(f=rosen, x=np.random.uniform(size=2), momentum_type='standard',
                                      momentum=0.8, max_iter=2000).minimize().x, rosen.x_star(), rtol=0.1)


def test_Nesterov_momentum_quadratic():
    assert np.allclose(ProximalBundle(f=quad1, x=np.random.uniform(size=2), momentum_type='nesterov',
                                      momentum=0.2).minimize().x, quad1.x_star(), rtol=0.1)
    assert np.allclose(ProximalBundle(f=quad2, x=np.random.uniform(size=2), momentum_type='nesterov',
                                      momentum=0.2).minimize().x, quad2.x_star(), rtol=0.1)


def test_Nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(ProximalBundle(f=rosen, x=np.random.uniform(size=2), momentum_type='nesterov',
                                      momentum=0.4).minimize().x, rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
