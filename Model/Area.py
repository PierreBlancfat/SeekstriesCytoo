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
        return self.xTopLeft==area.xTopLeft and self.yTopLeft==area.yTopLeft and self.xBotRight==area.xBotRight and self.yBotRight==area.yBotRight