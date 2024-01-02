import sys,math
from typing import List, NamedTuple, Dict
from dataclasses import dataclass

# TODO better scoring
# TODO edge movement if running from monsters
# TODO find better path past monsters
# TODO chaae fish off the ma

# Define the data structures as @dataclasses
@dataclass
class Vector:
    x: int
    y: int
    def __str__(self):
         output = "(x:"+str(int(self.x))+",y:"+str(int(self.y))+")"
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
         

@dataclass
class Fish:
    fish_id: int
    pos: Vector
    maxpos: Vector
    minpos: Vector
    speed: Vector
    color: int
    type: int

    def __str__ (self):
         output = "id:"+str(self.fish_id)+" pos:"+str(self.pos.x)+","+str(self.pos.y)+" Max:"+str(self.maxpos.x)+","+str(self.maxpos.y)+" Min:"+str(self.minpos.x)+","+str(self.minpos.y)
         return output

    def centre_pos(self):
         centre_pos = (self.maxpos+self.minpos)/2
         return centre_pos


@dataclass
class Target:
    target_id: int
    value: int
    status: str

@dataclass
class RadarBlip:
    drone_id: int
    fish_id: int
    dir: str

class Drone:
    def __init__ (self,drone_id:int, pos:Vector, emergency: bool,battery: int,scans: List[int],owner: str,speed: Vector = Vector(0,0),avoid_counter: int = 0, avoid_path: Vector=Vector(0,0)):
        self.drone_id = drone_id
        self.pos = pos
        self.emergency = emergency
        self.battery = battery
        self.scans = scans
        self.owner = owner
        self.speed = speed
        self.avoid_counter = avoid_counter
        self.avoid_path = avoid_path


def dot (a : Vector,b :Vector):
     output = (a.x*b.x,a.y*b.y)
     return output
     

    


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

def closest_test():
     print(f"testing closest for 0,0 0,0 1000,1000 0,-1", file=sys.stderr, flush=True)
     ca = closest_approach(Vector(0,0),Vector(0,0),Vector(1000,1000),Vector(0,-1))
     print(f"{ca}", file=sys.stderr, flush=True)

def monsters_in_way(d:Drone,dir:Vector) ->bool:
     trouble = False
     for m in monsters:
        closest_positions = closest_approach(d.pos,dir.unit()*600,m[1],m[2])
        c_dist = dist(closest_positions[0],closest_positions[1])
        if c_dist < 1000:
             trouble = True
             
     return trouble
        
          

def dist(a,b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def new_minmax ():
    # work out the new minx position for all the shoal given the new drone and radar information

    # update based on previous location
    # crop based on radar
    # crop based on min max y

    for cr in shoal:
        # enlarge the min max area based on possible creature speed
        old_min = shoal[cr].minpos
        old_max = shoal[cr].maxpos
        #grow the possible area by the maximum speed in each direction
        new_min= Vector(max(old_min.x - limits[shoal[cr].type+1][2],0),max(old_min.y - limits[shoal[cr].type+1][2],0))
        new_max= Vector(min(old_max.x + limits[shoal[cr].type+1][2],10000),min(old_max.y + limits[shoal[cr].type+1][2],10000))
        #crop the possible area by the limits for each type of fish
        shoal[cr].minpos = Vector(max(0,new_min.x),max(new_min.y,limits[shoal[cr].type+1][0]))
        shoal[cr].maxpos = Vector(min(10000,new_max.x),min(new_max.y,limits[shoal[cr].type+1][1]))
         
    for rb in my_radar_blips:
        # enlarge the min max area based on possible creature speed
        old_min = shoal[rb.fish_id].minpos
        old_max = shoal[rb.fish_id].maxpos
        ref_pos = drone_by_id[rb.drone_id].pos
    
        #crop the possible area by the results of the radar
        if rb.dir[1]=="L":
                new_min.x = min(old_min.x,ref_pos.x)
                new_max.x = min(old_max.x,ref_pos.x)
        if rb.dir[1]=="R":
                new_min.x = max(old_min.x,ref_pos.x)
                new_max.x = max(old_max.x,ref_pos.x)
        if rb.dir[0]=="T":
                new_min.y = min(old_min.y,ref_pos.y)
                new_max.y = min(old_max.y,ref_pos.y)
        if rb.dir[0]=="B":
                new_min.y = max(old_min.y,ref_pos.y)
                new_max.y = max(old_max.y,ref_pos.y)
        #crop the possible area by the limits for each type of fish
        shoal[rb.fish_id].minpos = Vector(max(0,new_min.x),max(new_min.y,limits[shoal[rb.fish_id].type+1][0]))
        shoal[rb.fish_id].maxpos = Vector(min(10000,new_max.x),min(new_max.y,limits[shoal[rb.fish_id].type+1][1]))
        #set the exact position if the fish is visible
        if shoal[rb.fish_id].pos.x != -1:
             shoal[rb.fish_id].maxpos = shoal[rb.fish_id].pos
             shoal[rb.fish_id].minpos = shoal[rb.fish_id].pos
        if rb.fish_id == 15:
            print("Cr:"+str(rb.fish_id)+" "+str(shoal[rb.fish_id]), file=sys.stderr, flush=True)

def current_value(f):
    #set the value of a given fish based on the type and who has already scanned / landed that fish color / type
    return shoal[f].type

def next_move(pos:Vector, target:Vector,speed:int) -> Vector:
     move = target - pos
     unit_move = move.unit()
     next_step = unit_move * speed
     next_step.x = int(next_step.x)
     next_step.y = int(next_step.y)
     move = next_step + pos
     return move

def best_speed(d:Drone) -> int:
     if d.pos.y<2500:
          bspeed = 600
     else:
          bspeed = 600
     return bspeed

def closest_monster(d:Drone):
     prox = 100000
     cm = ''
     for m in monsters:
          if dist(m[1],d.pos)<prox:
               prox = dist(m[1],d.pos)
               cm = m[0]
     return cm

def closest_fish_dist(d:Drone):
    prox = 100000
    for f in shoal:
        if shoal[f].type != -1:
            fdist = dist(drone_by_id[d].pos,shoal[f].centre_pos())
            if fdist<prox:
                prox = fdist
    return prox


## function to help check for overlapping line segments

# Given three collinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'  
def onSegment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False

def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Collinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
          
        # Clockwise orientation 
        return 1
    elif (val < 0): 
          
        # Counterclockwise orientation 
        return 2
    else: 
          
        # Collinear orientation 
        return 0

# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

def edge_move(d:Drone, t:Vector) -> Vector:
    
    # find speed of drone
    dspeed = dist(d.pos,t)

    # find intercept with edge at proposed vector
    right_edge = ((10000,0),(10000,10000))
    left_edge = ((0,0),(0,10000))
    top_edge = ((0,0),(10000,0))
    bottom_edge = ((0,10000),(10000,10000))
    proposed_target = t
    proposed_move = Vector(0,0)

    if doIntersect(right_edge[0],right_edge[1],d.pos,proposed_target):
        #intersects with right edge
        proposed_move.x = 9999-d.pos.x
        proposed_move.y = math.sqrt(dspeed**2-(proposed_move.x)**2)


    if doIntersect(left_edge[0],left_edge[1],d.pos,proposed_target):
        #intersects with left edge
        proposed_move.x = 1-d.pos.x
        proposed_move.y = math.sqrt(dspeed**2-(proposed_move.x)**2)

    if d.pos.y+proposed_move.y>10000:
        proposed_target.y = d.pos.y - proposed_move.y
    else:
        proposed_target.y = d.pos.y + proposed_move.y

    if doIntersect(top_edge[0],top_edge[1],d.pos,proposed_target):
        #intersects with top edge
        proposed_move.y = 1-d.pos.x
        proposed_move.x= math.sqrt(dspeed**2-(proposed_move.y)**2)


    if doIntersect(bottom_edge[0],bottom_edge[1],d.pos,proposed_target):
        #intersects with bottom edge
        proposed_move.y = 9999-d.pos.x
        proposed_move.x = math.sqrt(dspeed**2-(proposed_move.y)**2)

    if d.pos.x+proposed_move.x>10000:
        proposed_target.x = d.pos.x - proposed_move.x
    else:
        proposed_target.x = d.pos.x + proposed_move.x

    return proposed_target

    # find vector that intercepts edge at disrtance = speed

    # find intercept that is closest to original intercept

    # deal with case where bothe are equal

    # propose that intercept as move

    # what about corner cases where its off two sides?
    if d.pos.y>10000:
        #bottom
        pass

    if d.pos.y<0:
        #top
        pass

    if d.pos.x>10000:
        pass

    if d.pos.x<0:
        pass

#given a fish and a dronbe give the best move to chase the fish off the edge
def chase_move(d:Drone, f:Fish) ->Vector:
    pass



def new_targets():
    for rb in my_radar_blips:
        if shoal[rb.fish_id].type != -1:
            targets.append(Target(rb.fish_id,current_value(rb.fish_id),"none"))

# global variables and lists
limits=[(2500,10000,540),(2500,5000,200),(5000,7500,200),(7500,10000,200)]
my_scans: List[int] = []
foe_scans: List[int] = []
drone_by_id: Dict[int, Drone] = {}
foe_drones: List[Drone] = []
visible_fish: Dict[int,Fish] = {}
monsters: List[Fish] = []
my_radar_blips: List[RadarBlip] = []
targets: List[Target] = []
shoal: Dict[int, Fish] = {}
planned_path = Vector(0,0)

def initialise_game():
    

    fish_count = int(input())
    for _ in range(fish_count):
   
        fish_id, color, _type = map(int, input().split())
        new_fish = Fish(fish_id,Vector(-1,-1),Vector(10000,10000),Vector(0,0),Vector(-1,-1),color,_type)
        shoal[fish_id] = new_fish

    for d in range(4):
         new_drone = Drone(d,Vector(-1,-1),False,-1,[],'',Vector(-1,-1),0)
         drone_by_id[d] = new_drone


def initialise_loop():
    my_scans.clear()
    foe_scans.clear()
    foe_drones.clear()
    visible_fish.clear()
    monsters.clear()
    my_radar_blips.clear()
    targets.clear()
    
    

    my_score = int(input())
    foe_score = int(input())

    my_scan_count = int(input())
    for _ in range(my_scan_count):
        fish_id = int(input())
        my_scans.append(fish_id)

    foe_scan_count = int(input())
    for _ in range(foe_scan_count):
        fish_id = int(input())
        foe_scans.append(fish_id)

    my_drone_count = int(input())
    for _ in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = map(int, input().split())
        dpos = Vector(drone_x, drone_y)
        
        #find the old position of the drone if we know it to use to calculate the drone speed
        if drone_id in drone_by_id:
             old_pos = drone_by_id[drone_id].pos
        else:
             old_pos = dpos

        drone_by_id[drone_id].pos = dpos
        drone_by_id[drone_id].emergency = (emergency == '1')
        drone_by_id[drone_id].battery = battery
        drone_by_id[drone_id].owner = "me"
        drone_by_id[drone_id].scans = []
        drone_by_id[drone_id].speed = dpos - old_pos


    foe_drone_count = int(input())
    for _ in range(foe_drone_count):
        drone_id, drone_x, drone_y, dead, battery = map(int, input().split())
        pos = Vector(drone_x, drone_y)
        drone = Drone(drone_id, pos, dead == '1', battery, [],"foe")        
        drone_by_id[drone_id] = drone
        foe_drones.append(drone)
    
    drone_scan_count = int(input())
    for _ in range(drone_scan_count):
        drone_id, fish_id = map(int, input().split())
        drone_by_id[drone_id].scans.append(fish_id)

    visible_fish_count = int(input())
    for _ in range(visible_fish_count):
        fish_id, fish_x, fish_y, fish_vx, fish_vy = map(int, input().split())
        vpos = Vector(fish_x, fish_y)
        vspeed = Vector(fish_vx, fish_vy)
        visible_fish[fish_id] = Fish(fish_id,vpos,vpos,vpos,vspeed,shoal[fish_id].color,shoal[fish_id].type)
        for f in shoal:
             # if we can see thee fish update the pos and speed, if not reset pos to -1
            if f in visible_fish:
                shoal[f].pos=visible_fish[f].pos
                shoal[f].speed= visible_fish[f].speed
            else:
                shoal[f].pos = Vector(-1,-1)
                shoal[f].speed = Vector(-1,-1)

        if shoal[fish_id].type == -1 :
            monsters.append([fish_id,vpos,vspeed])
            print(f"{len(monsters)} Monsters visible", file=sys.stderr, flush=True)
             
    my_radar_blip_count = int(input())
    for _ in range(my_radar_blip_count):
        drone_id, fish_id, dir = input().split()
        drone_id = int(drone_id)
        fish_id = int(fish_id)
        my_radar_blips.append(RadarBlip(drone_id,fish_id,dir))
            
        

# game initialisation

closest_test()

initialise_game()

# game loop

while True:
    
    initialise_loop()
    
    #update position information
    new_minmax()
    
    #create list of targets
    new_targets()


    #for each drone find best target or surface

    #check if there is a monster en route

    #

    
    planned_path = Vector(0,0)
    speed = 600
    for drone in drone_by_id:
        if drone_by_id[drone].owner == "me":
            max_value =0 
            target_vector = Vector(0,0)
            target_fish = -1
            light = 0
            if len(drone_by_id[drone].scans)>=3:
                target_vector = Vector(drone_by_id[drone].pos.x,500)-drone_by_id[drone].pos
                print(f"surface drop off", file=sys.stderr, flush=True)
            elif drone_by_id[drone].avoid_counter>0:
                 target_vector = drone_by_id[drone].avoid_path
                 drone_by_id[drone].avoid_counter -=1
                 if drone_by_id[drone].pos.y <= 2000:
                     drone_by_id[drone].avoid_counter = 0
                 print(f"Still Avoid monsters", file=sys.stderr, flush=True)
            else:
                for t in targets:
                    if t.status != "owned":
                        if t.target_id not in my_scans:
                            if t.target_id not in drone_by_id[drone].scans:
                                if t.value> max_value:
                                    max_value = t.value
                                    target_fish = t.target_id
                                    target_vector = shoal[t.target_id].centre_pos() - drone_by_id[drone].pos
                                    t.status = 'owned'
                if target_fish != -1:
                    print(f"head for a fish {target_fish} at {shoal[target_fish].centre_pos()} going {target_vector}", file=sys.stderr, flush=True)
            planned_path = target_vector.unit()*speed
            # is the target path intercepted by a monster
            if len(monsters) !=0:
                closest_approach_min = 100000
                for m in monsters:
                    ca = closest_approach(drone_by_id[drone].pos,planned_path,m[1],m[2])
                    closest = dist(ca[0],ca[1])
                    if closest < closest_approach_min and ((closest_approach_min<1000 and ca[2]>=0) or (dist(drone_by_id[drone].pos,m[1])<2000)):
                         closest_approach_min = closest
                         monster_to_avoid = m
                         drone_by_id[drone].avoid_counter = 3
                         planned_path = (drone_by_id[drone].pos-shoal[m[0]].pos).unit()*speed
                         drone_by_id[drone].avoid_path = planned_path
                         print(f"Avoid monsters {str(planned_path)}", file=sys.stderr, flush=True)

            
            if dist(Vector(0,0),target_vector)<2000:
                light = 1   
            else:
                light = 0
            
            if closest_fish_dist(drone)<2000:
                light = 1

            planned_target = planned_path + drone_by_id[drone].pos

            print(f"MOVE {int(planned_target.x)} {int(planned_target.y)} {light} {str(drone_by_id[drone].speed)}")
