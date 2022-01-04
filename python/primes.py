#!/usr/bin/env python
from collections import defaultdict
from numpy import testing
from typing import Dict, List


def load_primes() -> List[int]:
    with open("PRIMES", "r") as handle:
        primes = []
        for line in handle:
            if line.startswith("#"):
                continue
            else:
                primes.extend(line.split(","))
    return sorted([int(i) for i in primes])


PRIMES = load_primes()
del load_primes


def prime_factorization(value: int) -> List[int]:
    if value == 1:
        return list()
        # raise ValueError("One is not a prime number and is not divisible by any prime number")
    elif value in PRIMES:
        return [
            value,
        ]
    else:
        factors = []
        reduced = value
        for prime in PRIMES:
            if prime > reduced:
                break
            while reduced % prime == 0:
                factors.append(prime)
                reduced //= prime
        if reduced == 1:
            return factors
        else:
            raise ValueError(f"Cannot find prime factors of {value}")


def first_n_primes(number: int) -> List[int]:
    if number <= len(PRIMES):
        return PRIMES[:number]
    else:
        raise ValueError(f"Maximum number of primes is {len(PRIMES)}")


def _count_factors(factors: List[int]) -> Dict:
    """Create a dict of prime -> number of times needed"""
    counted: Dict = defaultdict(lambda: 0)
    for factor in factors:
        counted[factor] += 1
    return dict(counted)


def least_common_multiple(*args) -> int:
    # https://byjus.com/maths/lcm/
    if len(args) == 0:
        raise ValueError("Need at least one number")

    # all the values are the same
    if len(set(args)) == 1:
        return args[0]

    # convert to number of each prime
    args_primed = [_count_factors(prime_factorization(arg)) for arg in set(args)]

    # setup to get the maximum number of each prime
    factors: Dict = defaultdict(lambda: 0)
    for primed in args_primed:
        for factor in primed.keys():
            factors[factor] = max(factors[factor], primed[factor])

    # find the product of all of the primes
    lcm = 1
    for key, value in factors.items():
        for i in range(value):
            lcm *= key

    return lcm


def greatest_common_factor(*args) -> int:
    # https://byjus.com/maths/gcf/
    if len(args) == 0:
        raise ValueError("Need at least one number")

    # all the values are the same
    if len(set(args)) == 1:
        return args[0]

    # convert to number of each prime
    args_primed = [_count_factors(prime_factorization(arg)) for arg in set(args)]

    # collect all primes
    primes = set()
    for primed in args_primed:
        for key in primed.keys():
            primes.add(key)

    # get the list of primes that exist in everything
    primes_reduced = set()
    for prime in primes:
        prime_in_all = True
        for factored in args_primed:
            if prime not in factored:
                prime_in_all = False
        if prime_in_all:
            primes_reduced.add(prime)

    # get the minimum number or primes in everything
    counted: Dict = {}
    for prime in primes_reduced:
        for factored in args_primed:
            if prime in counted:
                counted[prime] = min(counted[prime], factored[prime])
            else:
                counted[prime] = factored[prime]

    # find the product of all of the primes
    gcf = 1
    for key, value in counted.items():
        for i in range(value):
            gcf *= key

    return gcf


def test_prime_factorization():
    # 1 isn't prime
    assert prime_factorization(1) == []

    # check that all the primes are factored as just themselves
    for prime in PRIMES:
        assert prime_factorization(prime) == [prime]

    # check other prime factorizations
    testing.assert_equal(prime_factorization(4), [2, 2])
    testing.assert_equal(prime_factorization(6), [2, 3])
    testing.assert_equal(prime_factorization(8), [2, 2, 2])
    testing.assert_equal(prime_factorization(10), [2, 5])
    testing.assert_equal(prime_factorization(12), [2, 2, 3])
    testing.assert_equal(prime_factorization(14), [2, 7])
    testing.assert_equal(prime_factorization(15), [3, 5])
    testing.assert_equal(prime_factorization(16), [2, 2, 2, 2])
    testing.assert_equal(prime_factorization(18), [2, 3, 3])
    testing.assert_equal(prime_factorization(20), [2, 2, 5])
    testing.assert_equal(prime_factorization(21), [3, 7])
    testing.assert_equal(prime_factorization(22), [2, 11])
    testing.assert_equal(prime_factorization(24), [2, 2, 2, 3])
    testing.assert_equal(prime_factorization(25), [5, 5])
    testing.assert_equal(prime_factorization(26), [2, 13])
    testing.assert_equal(prime_factorization(27), [3, 3, 3])
    testing.assert_equal(prime_factorization(28), [2, 2, 7])
    testing.assert_equal(prime_factorization(30), [2, 3, 5])


def _check_abelian(function, a, b, expected):
    testing.assert_equal(function(a, b), expected)
    testing.assert_equal(function(a, b), function(b, a))


def test_lcm():
    # a number with itself is itself
    for i in range(10):
        testing.assert_equal(least_common_multiple(i), i)
        testing.assert_equal(least_common_multiple(i, i), i)
        testing.assert_equal(least_common_multiple(i, i, i), i)

    # should be abelian
    _check_abelian(least_common_multiple, 16, 20, 80)
    _check_abelian(least_common_multiple, 2, 3, 6)
    _check_abelian(least_common_multiple, 2, 4, 4)

    # for more than 2 numbers
    testing.assert_equal(least_common_multiple(2, 3, 6), 6)
    testing.assert_equal(least_common_multiple(2, 3, 6, 12), 12)


def test_gcf():
    # a number with itself is itself
    for i in range(10):
        testing.assert_equal(greatest_common_factor(i), i)
        testing.assert_equal(greatest_common_factor(i, i), i)
        testing.assert_equal(greatest_common_factor(i, i, i), i)

    # should be abelian
    _check_abelian(greatest_common_factor, 18, 21, 3)
    _check_abelian(greatest_common_factor, 2, 3, 1)
    _check_abelian(greatest_common_factor, 2, 4, 2)

    # for more than 2 numbers
    testing.assert_equal(greatest_common_factor(2, 3, 6), 1)
    testing.assert_equal(greatest_common_factor(2, 4, 12), 2)
    testing.assert_equal(greatest_common_factor(4, 8, 12, 24), 4)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="run the testsuite")
    parser.add_argument(
        "-n",
        "--num",
        default=10,
        type=int,
        help="number of primes to calculate (default=%(default)s)",
    )
    args = parser.parse_args()

    if args.test:
        test_prime_factorization()
        test_lcm()
        test_gcf()
        print("all tests passed")
    else:
        print(" ".join([str(i) for i in first_n_primes(args.num)]))
