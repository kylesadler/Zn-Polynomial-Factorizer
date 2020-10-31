from itertools import product
from pprint import pformat
import sys

def main():
    coefficients = [1,4,3,0,1,2]

    run(*coefficients)


def run(*coefficients):
    for p in [2,3,5]:
        print(f'\n{p}:\n')
        results = factor(p, coefficients)
        for result in results:
            print(list(result[0]), list(result[1]))


# def factor(coefficients, mod_coefficients):
# TODO make this work with arbitrary ideal mods
def factor(p, coefficients):
    """ coefficients is a list of numbers
        p is a prime integer (also works with non-primes, just saying)
    """
    coefficients = mod(coefficients, p)
    degree = get_degree(coefficients)
    target = polynomial(coefficients)
    seen = {}

    possible = []

    # loop over polynomials
    for coef1 in product(*[range(p)]*(degree+1)):
        coef1 = remove_leading_zeros(coef1)
        degree1 = get_degree(coef1)
        
        if degree1 < 1 or degree1 == degree:
            continue
        
        # if coef1 in seen:
        #     continue
        # else:
        #     seen[coef1] = 1
        # print(degree1)
        # print(coef1, end=" ")

        for coef2 in product(*[range(p)]*(degree - degree1+1)):
            if coef2[0] == 0:
                continue
            
            product = multiply(coef1, coef2, p)
            # print(coef1, coef2, product, coefficients)

            assert len(coefficients) == len(product)
            
            if coefficients == product:
                possible.append((coef1, coef2))
            
            # seen[coef2] = 1


    return [ x for x in possible if is_monic(x[0]) and is_monic(x[1]) ]

def polynomial(*args):
    """ args is list of coefficients corresponding to powers (n, ..., 0) or just the numbers (not a list)
        returns function of polynomial
    """
    if len(args) == 1 and (isinstance(args[0], tuple) or isinstance(args[0], list)):
        args = args[0]

    def p(x):
        
        output = 0
        power = 1

        for arg in args[::-1]:
            output += arg * power
            power *= x

        return output

    return p

def multiply(coef1, coef2, p):
    """ multiplies two sets of coefficients and mods the result by p """
    output = [0]*(len(coef1)+len(coef2)-1)
    for i, a in enumerate(coef1[::-1]):
        for j, b in enumerate(coef2[::-1]):
            output[len(output) - i - j - 1] += a*b

    return mod(output, p)


# utility functions

def remove_leading_zeros(coefficients):
    first_non_zero = next((x for x in coefficients if x != 0), None)
    
    if first_non_zero == None:
        return [0]

    return coefficients[coefficients.index(first_non_zero):]

def get_degree(coefficients):
    """ returns degree of polynomial with given coefficients
        ex: (1,2,3) are the coefficients of x^2 + 2x + 3 which has degree 2
    """
    return len(remove_leading_zeros(coefficients)) - 1

def mod(coefficients, n):
    """ mod coefficients by n """
    return remove_leading_zeros([x % n for x in coefficients])

def is_monic(coefficients):
    return coefficients[0] == 1

if __name__ == "__main__":
    main()