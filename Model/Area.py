#Class for define and area by the top left point and the bitto right point of it
class Area():

    border = []


    def __init__(self, xTopLeft, yTopLeft, xBotRight, yBotRight):
        self.xTopLeft = xTopLeft
        self.yTopLeft = yTopLeft
        self.xBotRight = xBotRight
        self.yBotRight = yBotRight

    #expend the area if the new point is out of it
    def expend(self, x, y):
        if(x < self.xTopLeft):
            self.xTopLeft = x
        elif(x > self.xBotRight):
            self.xBotRight = x
        elif(y < self.yTopLeft):
            self.yTopLeft = y
        elif(y > self.yBotRight):
            self.yBotRight = y

    def move(self, dx, dy):
        self.xTopLeft += dx
        self.yTopLeft += dy
        self.xBotRight += dx
        self.yBotRight += dy

    def equals(self, area):
        """ indicate if the current area is equal to the area in parameter.
    
        :param area: the area which may be equal to the current area
        :type area: list
        :return: True if the current area is equal to the area in parameter, false else.
        :rtype: bool
        """
        return self.xTopLeft==area.xTopLeft and self.yTopLeft==area.yTopLeft and self.xBotRight==area.xBotRight and self.yBotRight==area.yBotRight
    
    def notContainedIn(self, area):
        """ indicate if the current area is contained in the area in parameter.
    
        :param area: the area which may contain the current area
        :type area: list
        :return: True if the current area is contained in the area in parameter, false else.
        :rtype: bool
        """
        return self.xTopLeft<area.xTopLeft or self.yTopLeft<area.yTopLeft or self.xBotRight>area.xBotRight or self.yBotRight>area.yBotRight
