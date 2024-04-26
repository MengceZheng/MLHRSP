# Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem

## Introduction

This is a Python implementation of lattice-based attacks proposed in **Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem**[^MLHRSP]. Some underlying functions are based on [Joachim Vandersmissen's crypto-attacks](https://github.com/jvdsn/crypto-attacks).

## Requirements

* [SageMath](https://www.sagemath.org/) with Python 3.9
* [PyCryptodome](https://pycryptodome.readthedocs.io/)

You can check your SageMath Python version using the following command:

```commandline
$ sage -python --version
Python 3.9.0
```

Note: If your SageMath Python version is older than 3.9.0, some features in given scripts might not work.

## Usage

### Step-by-Step Input

To run this attack, you can simply execute the Python file **attack.py** with Sage using `sage -python attack.py` and then input several specific attack parameters:

```commandline
MLHRSP$ sage -python attack.py
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Example Mersenne n: [521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839]...
Input n (choosing from aboves): 521
Input w (satisfying 4*w^2 < n): 10
Input xi1 (0 to 1 & xi1+xi2=1): 0.5
Input xi2 (0 to 1 & xi1+xi2=1): 0.5
Input s (controlling lattices): 5
Input test times (for attacks): 5
Input type (basic or improved): basic
Success rate for n=521, w=10, xi1=0.5, xi2=0.5 using s=5 and basic strategy is 100.0%...
Average time is 0.167 seconds...
```

```commandline
MLHRSP$ sage -python attack.py
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Example Mersenne n: [521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839]...
Input n (choosing from aboves): 521
Input w (satisfying 4*w^2 < n): 10
Input xi1 (0 to 1 & xi1+xi2=1): 0.75
Input xi2 (0 to 1 & xi1+xi2=1): 0.25
Input s (controlling lattices): 7
Input test times (for attacks): 3
Input type (basic or improved): improved
Success rate for n=521, w=10, xi1=0.75, xi2=0.25 using s=7 and improved strategy is 100.0%...
Average time is 0.156 seconds...
```

### One Command Line Input

An alternative way to run the attack with the specific parameters n, h, xi1, xi2, s, and others requires passing them as command line arguments `sage -python attack.py <n> <h> <xi1> <xi2> <s>`. For instance, to run the attack with n = 521, h = 10, xi1 = 0.5, xi2 = 0.5, and s = 5, please run `sage -python attack.py 521 10 0.5 0.5 5`:

```commandline
MLHRSP$ sage -python attack.py 521 10 0.5 0.5 5
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Success rate for n=521, w=10, xi1=0.5, xi2=0.5 using s=5 and basic strategy is 100.0%...
Average time is 0.159 seconds...
```

Additionally, you can input command line arguments `sage -python attack.py <n> <h> <xi1> <xi2> <s> <times> <strategy>`. For instance, to run the attack with n = 521, h = 10, xi1 = 0.75, xi2 = 0.25, and s = 5 for 3 times using improved strategy, please run `sage -python attack.py 521 10 0.75 0.25 5 3 improved`:

```commandline
MLHRSP$ sage -python attack.py 521 10 0.25 0.75 5 3 improved
PARI stack size set to 10000000000 bytes, maximum size set to 10000003072
Success rate for n=521, w=10, xi1=0.25, xi2=0.75 using s=5 and improved strategy is 100.0%...
Average time is 0.119 seconds...
```

## Notes

All the details of the numerical attack experiments are recorded in the `attack.log` file.

[^MLHRSP]: Zheng M., Yan W., "Improved Lattice-Based Attack on Mersenne Low Hamming Ratio Search Problem"
