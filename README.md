# Machine Learning & Numerical Optimization [![Build Status](https://travis-ci.org/dmeoli/MachineLearningNumericalOptimization.svg?branch=master)](https://travis-ci.org/dmeoli/MachineLearningNumericalOptimization)

This code is a simple and modular implementation of some of the most important optimization algorithms used as core 
solver for many machine learning models developed during the Machine Learning & Numerical Methods and Optimization 
courses @ [Department of Computer Science](https://www.di.unipi.it/en/) @ [University of Pisa](https://www.unipi.it/index.php/english).

## Contents
- Optimization Algorithms
    - Unconstrained Optimization
        - Exact Line Search Methods
            - [x] Quadratic Steepest Gradient Descent
            - [x] Quadratic Conjugate Gradient
        - Inexact Line Search Methods
            - [x] Subgradient
            - [x] Steepest Gradient Descent
            - [ ] Conjugate Gradient
            - [x] Nonlinear Conjugate Gradient
                - [x] Fletcher–Reeves formula
                - [x] Polak–Ribière formula
                - [x] Hestenes-Stiefel formula
                - [x] Dai-Yuan formula
            - [x] Heavy Ball Gradient
            - [x] Steepest Accelerated Gradient
            - [x] Newton
            - [x] BFGS quasi-Newton
            - [ ] L-BFGS quasi-Newton
        - Fixed Step Size Methods
            - [x] Gradient Descent
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] Accelerated Gradient
                - [ ] standard momentum
                - [ ] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] Adam
                - [x] standard momentum
                - [x] Nadam
            - [x] AMSGrad
                - [x] standard momentum
                - [x] Nesterov momentum
            - [x] AdaMax
                - [x] standard momentum
                - [x] NadaMax
            - [x] AdaGrad
                - [x] standard momentum
                - [x] Nesterov momentum
            - [x] AdaDelta
                - [x] standard momentum
                - [x] Nesterov momentum
            - [x] RProp
                - [x] standard momentum
                - [x] Nesterov momentum
            - [x] RMSProp
                - [x] standard momentum
                - [x] Nesterov momentum
        - [x] Proximal Bundle with [cvxpy](https://github.com/cvxgrp/cvxpy) interface
             - [x] standard momentum
             - [x] Nesterov momentum
    - Box-Constrained Optimization
        - Primal Formulation
            - [x] Projected Gradient
            - [x] Frank-Wolfe
            - [x] Active Set
            - [x] Interior Point
            - [x] [scipy.optimize.slsqp](https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#sequential-least-squares-programming-slsqp-algorithm-method-slsqp) interface
        - Dual Formulation
            - [x] Lagrangian Dual
            - [ ] Sequential Minimal Optimization
            - [x] [qpsolvers](https://github.com/stephane-caron/qpsolvers) interface

- Optimization Functions
    - Unconstrained
        - [x] Rosenbrock
        - [x] Ackley
        - [x] Quadratic
            - [x] Lagrangian Box-Constrained
    - Constrained
        - [x] Box-Constrained Quadratic

- Machine Learning Models
    - [x] Linear Regression
        - Regularizers
            - [x] L1 or Lasso Regression
            - [x] L2 or Ridge Regression
    - [x] Logistic Regression
        - Regularizers
            - [x] L1 or Lasso
            - [x] L2 or Ridge or Tikhonov
    - [x] Support Vector Machines
        - [x] Support Vector Classifier
        - [x] Support Vector Regression
        - Kernels
            - [x] linear kernel
            - [x] polynomial kernel
            - [x] rbf kernel
    - [x] Neural Networks
        - Losses
            - [x] Mean Squared Error
            - [x] Mean Absolute Error
            - [x] Cross Entropy
            - [x] Binary Cross Entropy
        - Regularizers
            - [x] L1 or Lasso
            - [x] L2 or Ridge or Tikhonov
        - Activations
            - [x] Sigmoid
            - [x] Tanh
            - [x] ReLU
            - [x] LeakyReLU
            - [x] ELU
            - [x] SoftMax
            - [x] SoftPlus
        - Layers
            - [x] Fully Connected
            - [x] Convolutional
            - [x] Max Pooling
            - [x] Avg Pooling
            - [x] Flatten
            - [x] Dropout
            - [ ] Batch Normalization
            - [ ] Recurrent
            - [ ] Long Short-Term Memory (LSTM)
            - [ ] Gated Recurrent Units (GRU)
        - Initializers
            - [x] Xavier or Glorot normal and uniform
            - [x] He normal and uniform

- Jupyters
    - [x] support_vector_machines [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dmeoli/MachineLearningNumericalOptimization/blob/master/support_vector_machines.ipynb)

## License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This software is released under the MIT License. See the [LICENSE](LICENSE) file for details.
