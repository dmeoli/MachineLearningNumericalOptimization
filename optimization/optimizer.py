import itertools

import numpy as np

from optimization.test_functions import Function


class Minimizer:
    def __init__(self, f, x=None, eps=1e-6, verbose=False, plot=False, args=None):
        """

        :param f:        the objective function.
        :param x:        ([n x 1] real column vector): the point where to start the algorithm from.
        :param eps:      (real scalar, optional, default value 1e-6): the accuracy in the stopping
                         criterion: the algorithm is stopped when the norm of the gradient is less
                         than or equal to eps.
        :param verbose:  (boolean, optional, default value False): print details about each iteration
                         if True, nothing otherwise.
        :param plot:     (boolean, optional, default value False): plot the function's surface and its contours
                         if True and the function's dimension is 2, nothing otherwise.
        """
        if not isinstance(f, Function):
            raise ValueError('f not a function')
        self.f = f
        if x is None:
            x = f.x0
        if not np.isrealobj(x):
            raise ValueError('x not a real vector')
        self.x = np.asarray(x)
        self.n = x.shape[0]
        if not np.isrealobj(eps) or not np.isscalar(eps):
            raise ValueError('eps is not a real scalar')
        if eps < 0:
            raise ValueError('eps can not be negative')
        self.eps = eps
        self.verbose = verbose
        self.plot = plot
        if args is None:
            self.args = itertools.repeat(([], {}))
        else:
            self.args = args
        self.state_fields = None

    def set_from_info(self, info):
        """
        Populate the fields of this object with the corresponding fields of a dictionary.
        :param info: (dict) has to contain a key for each of the objects in the ``state_fields`` list.
                     The field will be set according to the entry in the dictionary.
        """
        for f in self.state_fields:
            self.__dict__[f] = info[f]

    def extended_info(self, **kwargs):
        """
        Return a dictionary populated with the values of the state fields.
        Further values can be given as keyword arguments.
        :param kwargs:  (dict) arbitrary data to place into dictionary
        :return: (dict) contains all attributes of the class given by the ``state_fields`` attribute.
                        Additionally updated with elements from ``kwargs``.
        """
        return dict((f, getattr(self, f)) for f in self.state_fields).update(kwargs)

    def __iter__(self):
        yield NotImplementedError


class Optimizer(Minimizer):
    def __init__(self, f, x=None, eps=1e-6, max_iter=1000, verbose=False, plot=False, args=None):
        """

        :param f:        the objective function.
        :param x:        ([n x 1] real column vector): the point where to start the algorithm from.
        :param eps:      (real scalar, optional, default value 1e-6): the accuracy in the stopping
                         criterion: the algorithm is stopped when the norm of the gradient is less
                         than or equal to eps.
        :param max_iter: (integer scalar, optional, default value 1000): the maximum number of iterations.
        :param verbose:  (boolean, optional, default value False): print details about each iteration
                         if True, nothing otherwise.
        :param plot:     (boolean, optional, default value False): plot the function's surface and its contours
                         if True and the function's dimension is 2, nothing otherwise.
        """
        super().__init__(f, x, eps, verbose, plot, args)
        if not np.isscalar(max_iter):
            raise ValueError('max_iter is not an integer scalar')
        self.max_iter = max_iter


class LineSearchOptimizer(Minimizer):
    def __init__(self, f, x=None, eps=1e-6, max_f_eval=1000, m1=0.01, m2=0.9, a_start=1, tau=0.9,
                 sfgrd=0.01, m_inf=-np.inf, min_a=1e-16, verbose=False, plot=False, args=None):
        """

        :param f:          the objective function.
        :param x:          ([n x 1] real column vector): the point where to start the algorithm from.
        :param eps:        (real scalar, optional, default value 1e-6): the accuracy in the stopping
                           criterion: the algorithm is stopped when the norm of the gradient is less
                           than or equal to eps.
        :param max_f_eval: (integer scalar, optional, default value 1000): the maximum number of
                           function evaluations (hence, iterations will be not more than max_f_eval
                           because at each iteration at least a function evaluation is performed,
                           possibly more due to the line search).
        :param m1:         (real scalar, optional, default value 0.01): first parameter of the
                           Armijo-Wolfe-type line search (sufficient decrease). Has to be in (0,1).
        :param m2:         (real scalar, optional, default value 0.9): typically the second parameter
                           of the Armijo-Wolfe-type line search (strong curvature condition). It should
                           to be in (0,1); if not, it is taken to mean that the simpler Backtracking
                           line search should be used instead.
        :param a_start:    (real scalar, optional, default value 1): starting value of alpha in the
                           line search (> 0).
        :param tau:        (real scalar, optional, default value 0.9): scaling parameter for the line
                           search. In the Armijo-Wolfe line search it is used in the first phase: if the
                           derivative is not positive, then the step is divided by tau (which is < 1,
                           hence it is increased). In the Backtracking line search, each time the step is
                           multiplied by tau (hence it is decreased).
        :param sfgrd:      (real scalar, optional, default value 0.01): safeguard parameter for the line search.
                           To avoid numerical problems that can occur with the quadratic interpolation if the
                           derivative at one endpoint is too large w.r.t. The one at the other (which leads to
                           choosing a point extremely near to the other endpoint), a *safeguarded* version of
                           interpolation is used whereby the new point is chosen in the interval
                           [as * (1 + sfgrd) , am * (1 - sfgrd)], being [as , am] the current interval, whatever
                           quadratic interpolation says. If you experience problems with the line search taking
                           too many iterations to converge at "nasty" points, try to increase this.
        :param m_inf:      (real scalar, optional, default value -inf): if the algorithm determines a value for
                           f() <= m_inf this is taken as an indication that the problem is unbounded below and
                           computation is stopped (a "finite -inf").
        :param min_a:      (real scalar, optional, default value 1e-16): if the algorithm determines a step size
                           value <= min_a, this is taken as an indication that something has gone wrong (the gradient
                           is not a direction of descent, so maybe the function is not differentiable) and computation
                           is stopped. It is legal to take min_a = 0, thereby in fact skipping this test.
        :param verbose:    (boolean, optional, default value False): print details about each iteration
                           if True, nothing otherwise.
        :param plot:       (boolean, optional, default value False): plot the function's surface and its contours
                           if True and the function's dimension is 2, nothing otherwise.
        """
        super().__init__(f, x, eps, verbose, plot, args)
        if not np.isscalar(max_f_eval):
            raise ValueError('max_f_eval is not an integer scalar')
        self.max_f_eval = max_f_eval
        if not np.isscalar(m1):
            raise ValueError('m1 is not a real scalar')
        if m1 <= 0 or m1 >= 1:
            raise ValueError('m1 is not in (0,1)')
        self.m1 = m1
        if not np.isscalar(m2):
            raise ValueError('m2 is not a real scalar')
        self.m2 = m2
        if not np.isscalar(a_start):
            raise ValueError('a_start is not a real scalar')
        if a_start < 0:
            raise ValueError('a_start must be > 0')
        self.a_start = a_start
        if not np.isscalar(tau):
            raise ValueError('tau is not a real scalar')
        if tau <= 0 or tau >= 1:
            raise ValueError('tau is not in (0,1)')
        self.tau = tau
        if not np.isscalar(sfgrd):
            raise ValueError('sfgrd is not a real scalar')
        if sfgrd <= 0 or sfgrd >= 1:
            raise ValueError('sfgrd is not in (0,1)')
        self.sfgrd = sfgrd
        if not np.isscalar(m_inf):
            raise ValueError('m_inf is not a real scalar')
        self.m_inf = m_inf
        if not np.isscalar(min_a):
            raise ValueError('min_a is not a real scalar')
        if min_a < 0:
            raise ValueError('min_a is < 0')
        self.min_a = min_a