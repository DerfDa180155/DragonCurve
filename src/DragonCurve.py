import numpy as np
import array

from numpy.core.defchararray import count
from setuptools.command.rotate import rotate


class DragonCurve:
    def __init__(self):
        pass

    def generateStartArray(self):
        return [[0, 0], [0, 1], [1, 1]]

    def rotate(self, point: array, rotationPoint: array):
        newPoint = []

        xdiff = rotationPoint[0] - point[0]
        ydiff = rotationPoint[1] - point[1]

        newPoint.append(rotationPoint[0]+ydiff)
        newPoint.append(rotationPoint[1]-xdiff)
        return newPoint

    def generateScaler(self, pointsArray):
        scaler = 1

        # not working correctly
        for i in range(len(pointsArray)):
            scaler *= 0.8
            #print(scaler)

        return 1

    def generateVerticesArray(self, pointsArray):
        vertexArray = []

        for position in pointsArray:
            # position
            vertexArray.append(position[0])
            vertexArray.append(position[1])
            # color
            vertexArray.append(1)
            vertexArray.append(1)
            vertexArray.append(1)

        vertexArray = np.array(vertexArray, dtype='f4')

        return vertexArray

    def generateNext(self, pointsArray: array):
        newPointArray = pointsArray.copy()
        endpoint = pointsArray[len(pointsArray)-1]
        for point in reversed(pointsArray):
            if point != endpoint:
                newPointArray.append(self.rotate(point, endpoint))

        middle = [0, 0]

        return self.generateScaler(pointsArray), newPointArray, self.generateVerticesArray(newPointArray), middle