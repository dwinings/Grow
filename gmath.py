#Author: Jonathan Haslow-Hall
import math

def distance(recOne, recTwo):
    x1 = recOne.centerx - recTwo.centerx
    x2 = recOne.centery - recTwo.centery
    x1 *= x1
    x2 *= x2
    x1 += x2
    return math.sqrt(x1)
