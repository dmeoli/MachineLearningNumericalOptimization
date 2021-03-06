import numpy as np

from . import StochasticOptimizer


class RProp(StochasticOptimizer):

    def __init__(self,
                 f,
                 x,
                 batch_size=None,
                 eps=1e-6,
                 epochs=1000,
                 step_size=0.001,
                 min_step=1e-6,
                 step_shrink=0.5,
                 step_grow=1.2,
                 max_step=1,
                 momentum_type='none',
                 momentum=0.9,
                 callback=None,
                 callback_args=(),
                 shuffle=True,
                 random_state=None,
                 verbose=False):
        super().__init__(f=f,
                         x=x,
                         step_size=step_size,
                         momentum_type=momentum_type,
                         momentum=momentum,
                         batch_size=batch_size,
                         eps=eps,
                         epochs=epochs,
                         callback=callback,
                         callback_args=callback_args,
                         shuffle=shuffle,
                         random_state=random_state,
                         verbose=verbose)
        self.min_step = min_step
        self.step_shrink = step_shrink
        self.step_grow = step_grow
        self.max_step = max_step
        self.jacobian = np.zeros_like(self.x)
        self.changes = np.zeros_like(self.x)

    def minimize(self):

        if self.verbose:
            print('epoch\titer\t cost\t', end='')
            if self.f.f_star() < np.inf:
                print('\t gap\t\t rate', end='')
                prev_v = np.inf

        for batch in self.batches:
            self.f_x, self.g_x = self.f.function(self.x, *batch), self.f.jacobian(self.x, *batch)

            if self.is_batch_end():

                if self.is_verbose():
                    print('\n{:4d}\t{:4d}\t{: 1.4e}'.format(self.epoch, self.iter, self.f_x), end='')
                    if self.f.f_star() < np.inf:
                        print('\t{: 1.4e}'.format(self.f_x - self.f.f_star()), end='')
                        if prev_v < np.inf:
                            print('\t{: 1.4e}'.format((self.f_x - self.f.f_star()) /
                                                      (prev_v - self.f.f_star())), end='')
                        else:
                            print('\t\t', end='')
                        prev_v = self.f_x

            try:
                self.callback(batch)
            except StopIteration:
                break

            if self.is_batch_end():
                self.epoch += 1

            if self.epoch >= self.epochs:
                self.status = 'stopped'
                break

            if self.momentum_type == 'standard':
                step_m1 = self.step
                step1 = self.momentum * step_m1
            elif self.momentum_type == 'nesterov':
                step_m1 = self.step
                step1 = self.momentum * step_m1
                self.x -= step1

            g_m1 = self.jacobian

            self.jacobian = self.f.jacobian(self.x, *batch)
            grad_prod = g_m1 * self.jacobian

            self.changes[grad_prod > 0] *= self.step_grow
            self.changes[grad_prod < 0] *= self.step_shrink
            self.changes = np.clip(self.changes, self.min_step, self.max_step)

            step2 = self.changes * np.sign(self.jacobian)

            if self.momentum_type == 'standard':
                self.x -= step1 + step2
            else:
                self.x -= step2

            if self.momentum_type != 'none':
                self.step = step1 + step2
            else:
                self.step = step2

            self.iter += 1

        if self.verbose:
            print('\n')

        return self
