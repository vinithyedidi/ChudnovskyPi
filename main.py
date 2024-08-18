from decimal import *
import time
import sys

# 100,000,000 digits of pi!


def mul():
    pass


# TODO: implement multithreading
def binary_split(a, b):
    # base case: when a and b are sufficiently close, we can compute directly
    if b == a + 1:
        Pab = -(6*a - 5) * (2*a - 1) * (6*a - 1)
        Qab = Decimal(10939058860032000) * a ** 3
        Rab = Pab * (545140134 * a + 13591409)

    # recursively compute P, Q, R by splitting in half: [a, b] -> [a, m] U [m, b]
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)

        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb

    return Decimal(Pab), Decimal(Qab), Decimal(Rab)


def chudnovsky(n):
    t0 = time.time()
    print('\nStarting binary split...')
    P1n, Q1n, R1n = binary_split(1, n)
    dt = int(time.time() - t0)/60
    print('Binary split complete in %3.2f mins.' % dt)

    t0 = time.time()
    print('\nComputing Chudnovsky sum...')
    try:
        num = (Decimal(426880) * Decimal(10005).sqrt() * Q1n)
        den = (Decimal(13591409) * Q1n + R1n)
        pi = num/den
    except Overflow:
        dt = (time.time() - t0)/60
        print('Chudnovsky sum overflow: %3.2f mins.' % dt, file=sys.stderr)
        print('P = ' + f'{P1n:.3}')
        print('Q = ' + f'{Q1n:.3}')
        print('R = ' + f'{R1n:.3}')
        exit(1)
    dt = (time.time() - t0)/60
    print('Chudnovsky sum complete in %3.2f mins.' % dt)
    return pi


def main():
    # set default settings for Decimal class
    getcontext().prec = 1000001  # number of digits of decimal precision (+1 for the initial 3)
    getcontext().Emax = MAX_EMAX
    n = 500000

    # read reference value to compare our pi with
    print('\nReading reference value...')
    file = open('/Users/vinithyedidi/CodingProjects/Pycharm/AccuratePi/pi_reference/pi_million.txt', 'r')
    real_pi = Decimal(file.read())
    file.close()
    print('Reference value established.')

    # compute pi with Chudnovsky algorithm
    t0 = time.time()
    pi = chudnovsky(n)

    # write to file
    filename = 'my_pi_million.txt'
    print('\nWriting pi value to file: ' + filename + '...')
    file = open('/Users/vinithyedidi/CodingProjects/Pycharm/AccuratePi/' + filename, 'w')
    file.write('{0:f}'.format(real_pi))
    file.close()
    print('Written to file.')

    # Analyze how well we did time-wise and accuracy-wise
    dt = (time.time() - t0) / 60
    error = pi - real_pi
    print('\nTotal time taken: %3.2f mins' % dt)
    print('Error = ' + f'{error:.3}')


if __name__ == '__main__':
    main()
