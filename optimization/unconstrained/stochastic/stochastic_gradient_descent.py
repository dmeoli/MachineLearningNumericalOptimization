import numpy as np

from ml.neural_network.initializers import random_uniform
from optimization.unconstrained.stochastic.schedules import constant
from optimization.unconstrained.stochastic.stochastic_optimizer import StochasticOptimizer


class StochasticGradientDescent(StochasticOptimizer):

    def __init__(self, f, x=random_uniform, batch_size=None, eps=1e-6, epochs=1000, step_size=0.01,
                 momentum_type='none', momentum=0.9, step_size_schedule=constant, momentum_schedule=constant,
                 callback=None, callback_args=(), shuffle=True, random_state=None, verbose=False):
        super().__init__(f, x, step_size, momentum_type, momentum, batch_size, eps, epochs,
                         callback, callback_args, shuffle, random_state, verbose)
        self.step_size = step_size_schedule(self.step_size)
        self.momentum = momentum_schedule(self.momentum)

    def minimize(self):

        if self.verbose and not self.iter % self.verbose:
            print('epoch\tf(x)\t', end='')
            if self.f.f_star() < np.inf:
                print('\tf(x) - f*\trate', end='')
                prev_v = np.inf

        for args in self.args:
            self.f_x, g = self.f.function(self.x, *args), self.f.jacobian(self.x, *args)

            if self.verbose and not self.iter % self.verbose:
                print('\n{:4d}\t{:1.4e}'.format(self.iter, self.f_x), end='')
                if self.f.f_star() < np.inf:
                    print('\t{:1.4e}'.format(self.f_x - self.f.f_star()), end='')
                    if prev_v < np.inf:
                        print('\t{:1.4e}'.format((self.f_x - self.f.f_star()) / (prev_v - self.f.f_star())), end='')
                    prev_v = self.f_x

            self.callback(args)

            if self.iter >= self.max_iter:
                status = 'stopped'
                break

            if self.momentum_type == 'standard':
                step_m1 = self.step
                self.step = next(self.step_size) * -g + next(self.momentum) * step_m1
                self.x += self.step
            elif self.momentum_type == 'nesterov':
                step_m1 = self.step
                big_jump = next(self.momentum) * step_m1
                self.x += big_jump
                g = self.f.jacobian(self.x, *args)
                correction = next(self.step_size) * -g
                self.x += correction
                self.step = big_jump + correction
            elif self.momentum_type == 'none':
                self.step = next(self.step_size) * -g
                self.x += self.step

            self.iter += 1

        if self.verbose:
            print('\n')
        return self.x, self.f_x, status