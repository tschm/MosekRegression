import numpy


def __pos(x):
    return max(x, 0)


pos = numpy.vectorize(__pos)


def P_lincone(x):
    return pos(x)


def d_lincone(x):
    return pos((-1) * x)


def P_quadcone(x):
    assert len(x) >= 2
    a = numpy.linalg.norm(x[1:], 2)

    if x[0] >= a:
        return x
    else:
        return (__pos(x[0] + a) / (2 * a)) * numpy.hstack((a, x[1:]))


if __name__ == '__main__':
    print pos(5.0)
    print pos([-5.9])
    print pos([-5.0, 5.0, 0.0, -2.0, 3.0])

    print d_lincone(numpy.array([-2.0, 3.0]))
    print P_quadcone(numpy.array([-2.0, 3.0, 3.0]))