import numpy as np
import array

from numpy.core.defchararray import count
from setuptools.command.rotate import rotate


class DragonCurve:
    def __init__(self):
        pass

    def generateStartArray(self):
        return [[0, 0], [0, 1]]

    def rotate(self, point: array, rotationPoint: array):
        newPoint = []

        xdiff = rotationPoint[0] - point[0]
        ydiff = rotationPoint[1] - point[1]

        newPoint.append(rotationPoint[0]+ydiff)
        newPoint.append(rotationPoint[1]-xdiff)
        return newPoint

    def calculateMiddle(self, minX, maxX, minY, maxY):
        return [((maxX-minX)/2)+minX, ((maxY-minY)/2)+minY]

    def generateScaler(self, length):
        return 1.5 / length

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
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        for point in reversed(pointsArray):
            if point[0] > maxX:
                maxX = point[0]
            elif point[0] < minX:
                minX = point[0]
            if point[1] > maxY:
                maxY = point[1]
            elif point[1] < minY:
                minY = point[1]
            if point != endpoint:
                newPoint = self.rotate(point, endpoint)
                if newPoint[0] > maxX:
                    maxX = newPoint[0]
                elif newPoint[0] < minX:
                    minX = newPoint[0]
                if newPoint[1] > maxY:
                    maxY = newPoint[1]
                elif newPoint[1] < minY:
                    minY = newPoint[1]
                newPointArray.append(newPoint)

        # scaler
        lenX = maxX - minX
        lenY = maxY - minY
        length = lenY
        if lenX > lenY:
            length = lenX

        return self.generateScaler(length), newPointArray, self.generateVerticesArray(newPointArray), self.calculateMiddle(minX, maxX, minY, maxY)