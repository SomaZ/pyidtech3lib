try:
    import numpy

    array = numpy.array
    dot = numpy.dot
    cross = numpy.cross
    sin = numpy.sin
    cos= numpy.cos
    sqrt = numpy.sqrt
    pi = numpy.pi
    deg2rad = numpy.deg2rad
    arccos = numpy.arccos
    linalg = numpy.linalg

except Exception:

    array = None
    dot = None
    cross = None
    sin = None
    cos= None
    sqrt = None
    pi = None
    deg2rad = None
    arccos = None
    linalg = None