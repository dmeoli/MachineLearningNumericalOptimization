import matplotlib.pyplot as plt
import numpy as np

from optimization.constrained.box_constrained_quadratic import BoxConstrainedQuadratic


class ConstrainedOptimizer:
    def __init__(self, f, eps=1e-6, max_iter=1000, verbose=False, plot=False):
        if not isinstance(f, BoxConstrainedQuadratic):
            raise TypeError('f is not a box constrained quadratic optimization function')
        self.f = f
        if not np.isscalar(eps):
            raise ValueError('eps is not a real scalar')
        if not eps > 0:
            raise ValueError('eps must be > 0')
        self.eps = eps
        if not np.isscalar(max_iter):
            raise ValueError('max_iter is not an integer scalar')
        if not max_iter > 0:
            raise ValueError('max_iter must be > 0')
        self.max_iter = max_iter
        self.iter = 1
        self.verbose = verbose
        self.plot = plot


class ProjectedGradient(ConstrainedOptimizer):
    # Apply the Projected Gradient algorithm with exact line search to the
    # convex Box-Constrained Quadratic program
    #
    #  (P) min { (1/2) x^T * Q * x + q * x : 0 <= x <= ub }
    #
    # encoded in the structure BCQP.
    #
    # Input:
    #
    # - BCQP, the structure encoding the BCQP to be solved within its fields:
    #
    #   = BCQP.Q: n \times n symmetric positive semidefinite real matrix
    #
    #   = BCQP.q: n \times 1 real vector
    #
    #   = BCQP.ub: n \times 1 real vector > 0
    #
    # - eps (real scalar, optional, default value 1e-6): the accuracy in the
    #   stopping criterion: the algorithm is stopped when the norm of the
    #   (projected) gradient is less than or equal to eps
    #
    # - max_iter (integer scalar, optional, default value 1000): the maximum
    #   number of iterations
    #
    # Output:
    #
    # - v (real scalar): the best function value found so far (possibly the
    #   optimal one)
    #
    # - x ([ n x 1 ] real column vector, optional): the best solution found so
    #   far (possibly the optimal one)
    #
    # - status (string, optional): a string describing the status of the
    #   algorithm at termination, with the following possible values:
    #
    #   = 'optimal': the algorithm terminated having proven that x is a(n
    #     approximately) optimal solution, i.e., the norm of the gradient at x
    #     is less than the required threshold
    #
    #   = 'stopped': the algorithm terminated having exhausted the maximum
    #     number of iterations: x is the bast solution found so far, but not
    #     necessarily the optimal one

    def __init__(self, f, eps=1e-6, max_iter=1000, verbose=False, plot=False):
        super().__init__(f, eps, max_iter, verbose, plot)

    def minimize(self):

        if self.verbose:
            print('iter\tf(x)\t\t||g(x)||')

        x = self.f.ub / 2  # start from the middle of the box

        if self.plot and self.n == 2:
            surface_plot, contour_plot, contour_plot, contour_axes = self.f.plot()

        while True:
            v, g = self.f.function(), self.f.jacobian()
            d = -g

            # project the direction over the active constraints
            d[self.f.ub - x <= 1e-12 and d > 0] = 0
            d[x <= 1e-12 and d < 0] = 0

            # compute the norm of the (projected) gradient
            ng = np.linalg.norm(d)

            if self.verbose:
                print('{:4d}\t{:1.4e}\t{:1.4e}'.format(self.iter, v, ng))

            if ng <= self.eps:
                status = 'optimal'
                break

            if self.iter > self.max_iter:
                status = 'stopped'
                break

            # first, compute the maximum feasible step size maxt such that
            #
            #   0 <= x[i] + maxt * d[i] <= ub[i]   for all i

            ind = d > 0  # positive gradient entries
            maxt = min((self.f.ub(ind) - x(ind)) / d[ind])
            ind = d < 0  # negative gradient entries
            maxt = min(maxt, min(-x(ind) / d[ind]))

            # compute optimal unbounded step size:
            # min (1/2) ( x + a d )^T * Q * ( x + a d ) + q^T * ( x + a d ) =
            #     (1/2) a^2 ( d^T * Q * d ) + a d^T * ( Q * x + q ) [ + const ]
            #
            # ==> a = - d^T * ( Q * x + q ) / d^T * Q * d
            den = d.T.dot(self.f.hessian()).dot(d)

            if den <= 1e-16:  # d^T * Q * d = 0  ==>  f is linear along d
                t = maxt  # just take the maximum possible step size
            else:
                # optimal unbounded step size restricted to max feasible step
                t = min((-g.T * d) / den, maxt)

            x = x + t * d

            self.iter += 1

        if self.verbose:
            print()
        if self.plot and self.n == 2:
            plt.show()
        return x, status