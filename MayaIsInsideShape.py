                             #########################
            ####  Investigate in Maya, If a point inside a 2D shape   #####
                             ###  Saeid Afsharnia  ###
                             #########################




# ------------  Editted version of python test based on comments   ----------------#


import maya.cmds as cmds
import statistics
import random


##########################  Utility Functions  ########################



def createShapes(number):
    global shapeList
    shapeList = []
    for i in range(number):
        shapeObj = shape()
        shapeList.append(shapeObj)
        

def createPoints(number):
    global pointList
    global shapeList
    pointList = []
    for i in range(number):
        pointObj = point(shapeList)
        pointList.append(pointObj)


def findMedian():
    global pointList
    medianTempList = []
    for point in pointList:
        hit = point.getTotalHit()
        medianTempList.append(hit)
    medianHitRate = statistics.median(medianTempList)
    print (medianTempList)
    return medianHitRate

def findHitShapes():
    global pointList
    hitShapeTempList = []
    for point in pointList:
        names = point.getShapesHitNames()
        for name in names:
            if name not in hitShapeTempList:
                hitShapeTempList.append(name)
    return hitShapeTempList



def getResults(number):
    createShapes(number)
    createPoints(number)
    print(f'{findHitShapes()} have been hit by total points')
    print ('-----------------------------------------------')
    print (f' The median hit rate : {findMedian()}')



##########################    Start of Code    ###########################


###### Global List ######
shapeList = []


pointList = []


### Class for creating random shapes ###
class shape(object):
    shapeID = 0
    def __init__(self):
        shapeName = ['circle','rectangle','diamond']
        self.shapeID = shape.shapeID+1
        shape.shapeID += 1
        self.dimension = random.uniform(10,100)
        self.look = random.sample(shapeName,1)[0]
        startDiff = (self.dimension)/2
        endDiff = 1000 - (self.dimension)
        self.LocX = random.uniform(startDiff,endDiff)
        self.LocZ = random.uniform(startDiff,endDiff)

        if self.look == 'rectangle':
            self.obj = self._makeRectangle()


        if self.look == 'diamond':
            self.obj = self._makeDiamond()


        if self.look == 'circle':
            self.obj = self._makeCircle()
        

                
        
    def _makeCircle(self):

        obj = cmds.circle( n = f'shape{self.shapeID}',nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=(self.dimension/2) )
        cmds.move(self.LocX,0,self.LocZ)
        return obj[0]
    
    
    
    def _makeDiamond(self):
    
        obj = cmds.circle( n = f'shape{self.shapeID}',nr=(0, 1, 0), c=(0, 0, 0), sections = 4, degree = 1, sw=360, r=(self.dimension/2) )
        cmds.rotate(0,45,0)
        cmds.move(self.LocX,0,self.LocZ)
        return obj[0]


    def _makeRectangle(self):

        obj = cmds.circle( n = f'shape{self.shapeID}', nr=(0, 1, 0), c=(0, 0, 0), sections = 4, degree = 1, sw=360, r=(self.dimension/2) )
        cmds.move(self.LocX,0,self.LocZ)
        return obj[0]


    def getObject(self):
        return self.obj                

 

### Class for creating random point in space ###
class point(object):
    
    def __init__(self,shapes):
        self.pLocX = random.uniform(0,1000)
        self.pLocZ = random.uniform(0,1000)
        self.pointLoc = (self.pLocX, 0, self.pLocZ)
        self.totalHit = 0
        self.shapesHit = []
        self._isInsideShapes(shapes)


    # Test if point is inside a shape      
    def _isInsideShape(self,shape):
        xform = cmds.xform(shape, q=True, bb=True, ws=True)
        
        if self.pointLoc[0]<xform[0] or self.pointLoc[0]>xform[3]:
            result = 0
            return result
        else:
            if self.pointLoc[2]<xform[2] or self.pointLoc[2]>xform[5]:
                result = 0
                return result
                
        
        xPos = random.choice([random.uniform(xform[0]-1, xform[0]-0.1), random.uniform(xform[3]+0.1, xform[3]+1)])
        zPos = random.choice([random.uniform(xform[2]-1, xform[2]-0.1), random.uniform(xform[5]+0.1, xform[5]+1)])

        testCrv = cmds.curve(p=[self.pointLoc, (xPos,0,zPos)], d=1, ws=True)
        
        cmds.scriptEditorInfo(e=True, sw=True)
        outvals = cmds.curveIntersect(testCrv, shape, ch=False, ud=False, tol=0.00001)
        cmds.scriptEditorInfo(e=True, sw=True)
        
        result = None
        if outvals is not None:
            outvals = outvals.split(" ")[:-1]
            length = int(len(outvals)/2)
            if length%2 == 0:
                result = 0
            else:
                result = 1
        else:
            result = 0
        cmds.delete(testCrv)
        
        return result
        

    def _isInsideShapes(self,shapes):
        for shape in shapes:
            result = self._isInsideShape(shape.getObject())
            if result == 1:
                self.shapesHit.append(shape)
                self.totalHit += 1

    def getShapesHit(self):
        return self.shapesHit

    def getShapesHitNames(self):
        tempList = []
        for shape in self.shapesHit:
            tempList.append(shape.getObject())
        return tempList

    def getTotalHit(self):
        return self.totalHit

                



getResults(1000)

