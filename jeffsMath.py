import math, random

def overlay(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def deduct(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def enlarge(a, ratio, point = True):
    if point:
        return (a[0] * ratio, a[1] * ratio)
    c = a[:]
    for i in range(len(c)):
        c[i] = c[i]*ratio
    return c

def reduce(a, ratio):
    return [a[i]/ratio for i in range(len(a))]

def rotate(point, angle):
    px, py = point

    qx = math.cos(angle) * px - math.sin(angle) * py
    qy = math.sin(angle) * px + math.cos(angle) * py
    return [qx, qy]

def addto(amount, target):
    for i in range(len(amount)):
        target[i] += amount[i]

def dissolve(magnitude, angle):
    return magnitude * math.cos(angle), magnitude * math.sin(angle)

def toFloat(iterable):
    return [float(a) for a in iterable]

def radarToVec(distance, angle):
    return math.cos(angle)*distance, math.sin(angle)*distance

def getRandom(tuple):
    return random.randint(tuple[0], tuple[1])

def getRandFloat(tuple):
    return random.random()*(tuple[1]-tuple[0])+tuple[0]