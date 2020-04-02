import numpy as np
import pytest

from optimization.constrained.projected_gradient import ProjectedGradient
from optimization.optimization_function import BoxConstrainedQuadratic


def test():
    np.random.seed(2)
    assert np.allclose(ProjectedGradient(BoxConstrainedQuadratic(n=2)).minimize()[0], 0.)


if __name__ == "__main__":
    pytest.main()