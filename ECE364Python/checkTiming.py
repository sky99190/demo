import time
from os.path import join
from Homography import *

import os
from os.path import join
from glob import glob
import unittest
from random import uniform
from inspect import isclass
from enum import Enum
from scipy.misc import *
import numpy as np
from Homography import *

def transformImage(sourceImageName, targetImageName, TType, effect=None):

    testFolder = "TestImages"
    targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]])

    begin = time.clock()

    sourceImage = imread(join(testFolder, sourceImageName))
    containerImage = imread(join(testFolder, targetImageName))

    transform = TType(sourceImage)
    transform.setupTransformation(targetPoints, effect)

    transform.transformImageOnto(containerImage)

    end = time.clock()
    duration = end - begin

    return duration


def evaluateGrayscaleImages():

    duration = transformImage("knight.png", "WhiteGray.png", Transformation)
    print('Gray No Effect = {:2.2f} sec.'.format(duration))

    for effect in Effect:
        duration = transformImage("knight.png", "WhiteGray.png", Transformation, effect)
        print('Gray {0} = {1:2.2f} sec'.format(effect.name, duration))


def evaluateColorImages():

    duration = transformImage("strange.png", "White.png", ColorTransformation)
    print('Color No Effect = {:2.2f} sec.'.format(duration))

    for effect in Effect:
        duration = transformImage("strange.png", "White.png", ColorTransformation, effect)
        print('Color {0} = {1:2.2f} sec'.format(effect.name, duration))


if __name__ == "__main__":
    evaluateGrayscaleImages()
    print()
    evaluateColorImages()
