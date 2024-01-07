import sys,math


class Vector:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
        
    def __str__(self):
         output = "("+str(int(self.x))+","+str(int(self.y))+")"
         return output
    def __repr__(self):
         output = "(x:"+str(int(self.x))+",y:"+str(int(self.y))+")"
         return output
    def __add__(self, value):
         output = Vector(self.x+value.x,self.y+value.y)
         return output
    def __sub__(self, value):
         output = Vector(self.x-value.x,self.y-value.y)
         return output
    def __mul__(self, value):
         output = Vector(self.x*value,self.y*value)
         return output
    def __div__(self, value):
         output= Vector(self.x/value,self.y/value)
         return output
    def __truediv__(self, value):
         output= Vector(self.x/value,self.y/value)
         return output
    def length(self):
         return math.sqrt((self.x**2)+(self.y**2))
    def unit(self):
         vlength = self.length()
         if vlength==0:
            return Vector(0,0)
         else:
            return Vector(self.x/vlength,self.y/vlength)
    def mag(self) ->float:
        magnitude = math.sqrt((self.x*self.x)+(self.y*self.y))
        return magnitude
    
class Line:
    def __init__(self,start:Vector,end:Vector):
        self.start = start
        self.end = end
        
class Polygon:
    def __init__(self,points:list[Vector]):
        self.points = points

class Circle:
    def __init__(self,centre:Vector,radius:int):
        self.centre = centre
        self.radius = radius



def point_in_polygon(polygon, point):
    """
    Raycasting Algorithm to find out whether a point is in a given polygon.
    Performs the even-odd-rule Algorithm to find out whether a point is in a given polygon.
    This runs in O(n) where n is the number of edges of the polygon.
     *
    :param polygon: a list of points of the polygon in neighbouring order
    :param point: a class with attributes x and y
    :return: whether the point is inside the polygon (not on the edge, just turn < into <= and > into >= for that)
    """

    # A point is in a polygon if a line from the point to infinity crosses the polygon an odd number of times
    # For each edge (In this case for each point of the polygon and the previous one)
    inside = False
    start = polygon[0]
    for p in range(len[polygon]):
        end = polygon[p+1]
        if point_left_of_line(point,Line(start,end)):
            # invert inside  
            inside = not inside
        start = end
    # If the number of crossings was odd, the point is in the polygon
    return inside

def point_left_of_line(point:Vector,line:Line)->bool:
    is_left = False
    # true if the point is below the highest point of the line
    if point.y <= max(line.start.y,line.end.y):
        # and above the bottom of the line
        if point.y > min(line.start.y,line.end.y):
            # and to the left of the right most part of the line
            if point.x <= max(line.start.x,line.end.x):
                # check line isnt horizontal
                    if line.start.y != line.end.y:
                    # find x intersection of a horizontal line from the point to infinity on the right
                        x_intersect = (point.y-line.start.y)*(line.end.x-line.start.x) / (line.end.y-line.start.y)+line.start.x
                        # check if the point is on the same line as the edge or to the left of the x intersection
                    if point.x <= x_intersect:
                        is_left = True
    return is_left
                
def point_in_circle(point:Vector,circle:Circle)->bool:
    inside = False
    if dist(point,circle.centre)<circle.radius:
        inside = True
    return inside

def dist(pointA:Vector,pointB:Vector)->float:
    distance = math.sqrt(((pointA.x-pointB.x)**2)+((pointA.y-pointB.y)**2))
    return distance

def dot (a : Vector,b :Vector) -> float:
     output = (a.x*b.x,a.y*b.y)
     return output

class game():
    def __init__(self,turn = 0):
        self.turn = turn
        self.fish_count = int(input())

class Fish:
    def __init__(self,fish_id: int,pos: Vector,maxpos: Vector, minpos: Vector,speed: Vector,color: int,type: int)    
        self.fish_id = fish_id
        self.pos = pos
        self.maxpos = maxpos
        self.minpos = minpos
        self.speed = speed
        self.color = color
        self.type = type
     
    def __str__ (self):
         output = "id:"+str(self.fish_id)+" pos:"+str(self.pos.x)+","+str(self.pos.y)+" Max:"+str(self.maxpos.x)+","+str(self.maxpos.y)+" Min:"+str(self.minpos.x)+","+str(self.minpos.y)
         return output

    def centre_pos(self) -> Vector:
         centre_pos= (self.maxpos+self.minpos)/2
         return centre_pos   

class Monster(Fish):
    def __init__ (self,status:str = 'asleep',target:int = -1):
        self.status = status
        self.target = target

class Target:
    def __init__(self,target_id:int, value:int,status:str):
        self.target_id = target_id
        self.value = value
        self.status = status       
        
class RadarBlip:
    def __init__(self,drone_id:int, fish_id:int,dir:str)
        self.drone_id = drone_id
        self.fish_id = fish_id
        self.dir = dir

class Drone:
    def __init__ (self,drone_id:int, pos:Vector, emergency: bool,battery: int,scans: List[int],owner: str,speed: Vector = Vector(0,0),avoid_counter: int = 0, avoid_path: Vector=Vector(0,0),status:str = 'unknown'):
        self.drone_id = drone_id
        self.pos = pos
        self.emergency = emergency
        self.battery = battery
        self.scans = scans
        self.owner = owner
        self.speed = speed
        self.avoid_counter = avoid_counter
        self.avoid_path = avoid_path
        self.status = status

# given the position and speed of two objects 
# return two position Vectors equal to their locations at closest approach
def closest_approach(pos1 : Vector,speed1: Vector,pos2: Vector,speed2 : Vector) -> List[Vector]:
    # move to origin
    p1 = pos1 - pos1 # (0,0)
    p2 = pos2 - pos1
    # move refernce frame so origin is stationary
    s1 = speed1 - speed1 # (0,0)
    s2 = speed2 - speed1

# equation for point 1 in time is pos1 + t*speed1
# equation for point 2 in time is pos2 + t*speed2
    
# translating to origin
# p1(t) = pos1-pos1 + t*speed1 = t*speed1
# p2(t) = pos2-pos1 + t*speed2 = p2 + t*speed2

# translating so origin is staionary
# p1(t) = t*speed1 - t*speed1 = 0
# p2(t) = p2 + t*(speed2 - speed1) = p2 + s2


# dot product of moving object and perpendicular = 0
# moving object = s2
# perpendicular = p2 + t*s2
# dot(s2,(p2-t*s2) = 0)
# s2.x* p2.x + t*s2.x*s2.x + s2.y*p2.y + ts2.y*s2.y = 0
# s2.x*p2.x + s2.y*2.y = - t*(s2.x^2+s2.y^2)
# so - t = (s2.x*p2.x + s2.y*p2.y) / ( s2.x^2 + s2.y^2)
 
# so position of 1 = pos 1 + t * speed1

    if (s2.x*s2.x+s2.y*s2.y) == 0:
        t=0
    else:
        t = -1* ((s2.x*p2.x)+(s2.y*p2.y))/(s2.x*s2.x+s2.y*s2.y)

    if t>0:
        cpos1 = Vector(int(pos1.x+(t*speed1.x)),int(pos1.y+(t*speed1.y)))
        cpos2 = Vector(int(pos2.x+(t*speed2.x)),int(pos2.y+(t*speed2.y)))
    if t<=0:
        cpos1 = pos1
        cpos2 = pos2
    
    return (cpos1,cpos2,t)
       
# game inititation

g = game()
