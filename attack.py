import sys
import time
import logging
import cypari2

from math import gcd
from random import randrange
from sage.all import Integer
from sage.all import inverse_mod

import solving_strategy

logging.basicConfig(filename='attack.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
sys.set_int_max_str_digits(0)
pari = cypari2.Pari()
pari.allocatemem(10000000000)   

Mersenne_numbers_n = [521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839]

def hamming_weight(a):
    """
    Calculate the Hamming weight of an integer.
    :param a: the integer
    :return: the number of non-zero bits in the binary representation of the integer
    """
    count = 0
    while a:
        count += a & 1
        a >>= 1
    return count

def get_number(n, h):
    """
    Generate a random integer with a given number of bits and given Hamming weight.
    :param n: the number of bits
    :param h: the Hamming weight
    :return: the generated random integer
    """
    a = 0
    bit_mask = 1 << (n - 1)
    a |= bit_mask
    for _ in range(h - 1):
        bit_mask = 1 << randrange(n)
        while a & bit_mask:
            bit_mask = 1 << randrange(n)
        a |= bit_mask
    return a

def generate_MLHRSP_instance(n, w, xi1, xi2, af=1):
    """
    Generate a random MLHRSP instances of f, g, and h for a given set of parameters.
    :param n: the number of bits for the integers
    :param w: the Hamming weight for f and g
    :param xi1: the exponential parameter for f
    :param xi2: the exponential parameter for g
    :param af: the achievement factor (default: 1)
    :return: a tuple (f, g, h) containing the generated instance
    """
    p = f = g = h = Integer(1)
    bf = int(n * xi1)
    bg = int(n * xi2 * af)
    logging.info(f"Generating MLHRSP instance with {n}-bit modulus p, {bf}-bit f, {bg}-bit g and Hamming weight {w}...")
    p = 2 ** n - 1
    f = get_number(bf, w)
    g = get_number(bg, w)
    while gcd(f, g) != 1:
        g = get_number(bg, w)
    h = inverse_mod(g, p) * f % p
    return p, f, g, h

def attack_MLHRSP_instance(p, h, xi1, xi2, s=5, strategy="basic"):
    """
    Attack a random MLHRSP instance with given set of parameters.
    :param p: the Mersenne prime
    :param h: the given known parameter
    :param xi1: the exponential parameter for f
    :param xi2: the exponential parameter for g
    :param s: the parameter for controlling lattice construction (default: 5)
    :param strategy: the strategy to use, can be "basic", or "improved" (default: "basic")
    :return: 1 if attack succeeds else 0
    """
    assert strategy == "basic" or strategy == "improved", f"Solving strategy is not defined! Please input a correct strategy name."
    if strategy == "basic":
        logging.info("Using basic solving strategy to find roots...")
        start_time = time.perf_counter()
        fs, gs = solving_strategy.basic_attack(p, h, xi1, xi2, s=s)
        end_time = time.perf_counter()
        test_time = end_time - start_time
    elif strategy == "improved":
        logging.info("Using improved solving strategy to find roots...")
        start_time = time.perf_counter()
        fs, gs = solving_strategy.improved_attack(p, h, xi1, xi2, s=s)
        end_time = time.perf_counter()
        test_time = end_time - start_time
    if fs is not None and gs is not None and fs == f and gs == g:
        logging.info(f"Succeeded!")
        logging.info(f"Found f = {fs}")
        logging.info(f"Found g = {gs}")
        return 1, test_time
    else:
        logging.info(f"Failed!")
        return 0, test_time


assert len(sys.argv) == 1 or 6 <= len(sys.argv) <= 8, f"Wrong arguments! Please check and input suitable parameters."
if len(sys.argv) == 1:
    print(f"Example Mersenne n: {Mersenne_numbers_n}...")
    n = int(input("Input n (choosing from aboves): "))
    w = int(input("Input w (satisfying 4*w^2 < n): "))
    xi1 = float(input("Input xi1 (0 to 1 & xi1+xi2=1): "))
    xi2 = float(input("Input xi2 (0 to 1 & xi1+xi2=1): "))
    s = int(input("Input s (controlling lattices): "))
    test_times = int(input("Input test times (for attacks): "))
    strategy = input("Input type (basic or improved): ")
else:
    n = int(sys.argv[1])
    w = int(sys.argv[2])
    xi1 = float(sys.argv[3])
    xi2 = float(sys.argv[4])
    s = int(sys.argv[5])
    if len(sys.argv) >= 7:
        test_times = int(sys.argv[6])
    else:
        test_times = 5
    if len(sys.argv) == 8:
        strategy = sys.argv[7]
    else:
        strategy = "basic"

logging.info(f"Test with n={n}, w={w}, xi1={xi1}, xi2={xi2}, and s={s} for {test_times} times:")
total_time = 0
results = []

for i in range(test_times):
    p, f, g, h = generate_MLHRSP_instance(n, w, xi1, xi2)
    result, test_time = attack_MLHRSP_instance(p, h, xi1, xi2, s=s, strategy=strategy)
    if result:
        total_time += test_time
        results.append(result)

if len(results) == 0:
    logging.info(f"The success rate for n={n}, w={w}, xi1={xi1}, xi2={xi2} using s={s} and {strategy} strategy is 0%...")
    print(f"The success rate for n={n}, w={w}, xi1={xi1}, xi2={xi2} using s={s} and {strategy} strategy is 0%...")
else:
    logging.info(f"Success rate for n={n}, w={w}, xi1={xi1}, xi2={xi2} using s={s} and {strategy} strategy is {sum(results)/test_times*100}%...")
    print(f"Success rate for n={n}, w={w}, xi1={xi1}, xi2={xi2} using s={s} and {strategy} strategy is {sum(results)/test_times*100}%...")
    avg_time = total_time / len(results)
    print(f"Average time is {avg_time:.3f} seconds...")
