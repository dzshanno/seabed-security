import sys,math
from typing import List, NamedTuple, Dict
from dataclasses import dataclass

# TODO better scoring
# TODO edge movement if running from monsters
# TODO find better path past monsters
# TODO chaae fish off the ma

# Define the data structures as @dataclasses

class game():
    def __init__(self,turn = 0):
        self.turn = turn
        
@dataclass
class Vector:
    x: int
    y: int
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
    


class Fish:
    def __init__(self,fish_id: int,pos: Vector,prev_max_pos: Vector,prev_min_pos: Vector,curr_max_pos: Vector,curr_min_pos: Vector,
    next_max_pos: Vector,next_min_pos: Vector, prev_speed: Vector,curr_speed: Vector, next_speed: Vector, color: int,  _type: int, status:str):
        
        self.fish_id = fish_id
        self.pos = pos
        self.prev_max_pos = prev_max_pos
        self.prev_min_pos = prev_min_pos
        self.curr_max_pos = curr_max_pos
        self.curr_min_pos = curr_min_pos
        self.next_max_pos = next_max_pos
        self.next_min_pos = next_min_pos
        self.prev_speed = prev_speed
        self.curr_speed = curr_speed
        self.next_speed = next_speed
        self.color = color
        self.type = _type
        self.status = status
        

    def __str__ (self):
        output = "id:"+str(self.fish_id)+" curr_pos:("+str(self.curr_min_pos.x)+"-"+str(self.curr_max_pos.x)+","
        +str(self.curr_min_pos.y)+"-"+str(self.curr_max_pos.y)+")"
        return output

    def centre_pos(self) -> Vector:
        centre_pos= (self.curr_max_pos+self.curr_min_pos)/2
        return centre_pos
    
    def prev_pos(self) -> Vector:
        prev_pos = (self.prev_max_pos+self.prev_min_pos)/2
        return prev_pos
    
    def curr_pos(self) -> Vector:
        curr_pos = (self.curr_max_pos+self.curr_min_pos)/2
        return curr_pos
    
    def next_pos(self) -> Vector:
        next_pos = (self.next_max_pos+self.next_min_pos)/2
        return next_pos


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
    def __init__ (self,drone_id:int, pos:Vector, emergency: bool,battery: int,scans: List[int],owner: str,speed: Vector = Vector(0,0),avoid_counter: int = 0, avoid_path: Vector=Vector(0,0),status:str = 'unknown',light:bool = False):
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
        self.light = light


class Monster(Fish):
    def __init__ (self,status:str = 'asleep'):
        self.status = status


# general functions

def dot (a : Vector,b :Vector) -> float:
    output = (a.x*b.x,a.y*b.y)
    return output
    
    
def dist(a:Vector,b:Vector)-> float:
    distance = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
    return distance


def score_for_scan(scans:List[int])->int:
        score_to_add = 0
        my_types = [0,0,0]
        my_colors = [0,0,0,0]
        foe_types = [0,0,0]
        foe_colors = [0,0,0,0]
        for ms in my_scans:
            my_types[shoal[ms].type] +=1
            my_colors[shoal[ms].color] +=1
        for fs in foe_scans:
            foe_types[shoal[fs].type] +=1
            foe_colors[shoal[fs].color] +=1
    
        for s in scans:
            if s not in my_scans:
                my_types[shoal[s].type] += 1
                my_colors[shoal[s].color] += 1
                if s not in foe_scans:
                    score_to_add += (shoal[s].type+1)*2
                else:
                    score_to_add += (shoal[s].type+1)
                if my_types[shoal[s].type] == 4 and foe_types[shoal[s].type] <4:
                    score_to_add += 8
                if my_types[shoal[s].type] == 4 and foe_types[shoal[s].type] ==4:
                    score_to_add += 4
                if my_colors[shoal[s].color] == 3 and foe_colors[shoal[s].color] <3:
                    score_to_add += 6
                if my_colors[shoal[s].color] == 3 and foe_colors[shoal[s].color] ==3:
                    score_to_add += 3  
        print(f"scan score t{my_types} c{my_colors}",  file=sys.stderr, flush=True)
        return score_to_add

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


# test functions

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

        
def foe_possible_score(oppo_scan:List) -> int:
    score_matrix = [[0 for x in range(3)] for y in range(4)]
    poss_score = 0
    types = [2,2,2]
    colors = [2,2,2,2]
    live_fish = []
    for rb in my_radar_blips:
        if rb.fish_id not in live_fish and shoal[rb.fish_id].type != -1 :
            live_fish.append(rb.fish_id)
    for cr in shoal:
        if shoal[cr].type != -1:
            cr_score = 0
            cr_type = shoal[cr].type
            cr_color = shoal[cr].color
            if cr not in live_fish:
                cr_score = 0
                types[cr_type] = 0
                colors[cr_color] = 0
            elif cr in oppo_scan:
                cr_score = 1
                types[cr_type] = min(1,types[cr_type])
                colors[cr_color] = min(1,types[cr_type])
            else:
                cr_score = 2
                
            score_matrix[cr_color][cr_type] = cr_score

    for row in range(4):
        for col in range(3):
            poss_score += score_matrix[row][col]*(col+1)

    poss_score += sum(types)*4
    poss_score += sum(colors)*3    

    return poss_score    

def update_fish () ->None:
    # work out the new minx position for all the shoal given the new drone and radar information

    # update based on previous location
    # crop based on radar
    # crop based on min max y
    # crop based on foe drone seeing the fish

    for cr in shoal:
        
        # enlarge the min max area based on possible creature speed
        shoal[cr].prev_min_pos = shoal[cr].curr_min_pos
        shoal[cr].prev_max_pos = shoal[cr].curr_max_pos
        shoal[cr].prev_speed = shoal[cr].curr_speed
        
        #crop the possible area by the limits for each type of fish - held in the limits list
        shoal[cr].curr_min_pos = Vector(max(0,shoal[cr].curr_min_pos.x),max(shoal[cr].curr_min_pos.y,limits[shoal[cr].type+1][0]))
        shoal[cr].curr_max_pos = Vector(min(10000,shoal[cr].curr_max_pos.x),min(shoal[cr].curr_max_pos.y,limits[shoal[cr].type+1][1]))
        
        #crop the possible area by the position of a foe drone if its been seen this turn - held in foe_new_scans
        nscr = []
        for ns in foe_new_scans:
            if ns[1] ==cr:
                nscr.append[ns]
        
        for nsc in nscr:
            light_range = 2000
            shoal[cr].curr_min_pos = Vector(max(shoal[cr].curr_min_pos.x,drone_by_id[nsc[0]].pos.x-light_range), max(shoal[cr].curr_min_pos.y,drone_by_id[nsc[0]].pos.y-2000))
            shoal[cr].curr_max_pos = Vector(min(shoal[cr].curr_max_pos.x,drone_by_id[nsc[0]].pos.x+light_range), min(shoal[cr].curr_max_pos.y,drone_by_id[nsc[0]].pos.y+2000))
        
            # could be less than 2000 if we can work out if the drone light was on or off from the bttery history
            
        
    for rb in my_radar_blips:
        
        curr_min_pos = shoal[rb.fish_id].curr_min_pos
        curr_max_pos = shoal[rb.fish_id].curr_max_pos
        ref_pos = drone_by_id[rb.drone_id].pos
        #crop the possible area by the results of the radar
        if rb.dir[1]=="L":
                curr_min_pos.x = min(curr_min_pos.x,ref_pos.x)
                curr_max_pos.x = min(curr_max_pos.x,ref_pos.x)
        if rb.dir[1]=="R":
                curr_min_pos.x = max(curr_min_pos.x,ref_pos.x)
                curr_max_pos.x = max(curr_max_pos.x,ref_pos.x)
        if rb.dir[0]=="T":
                curr_min_pos.y = min(curr_min_pos.y,ref_pos.y)
                curr_max_pos.y = min(curr_max_pos.y,ref_pos.y)
        if rb.dir[0]=="B":
                curr_min_pos.y = max(curr_min_pos.y,ref_pos.y)
                curr_max_pos.y = max(curr_max_pos.y,ref_pos.y)
        
        #crop the possible area by the limits for each type of fish
        
        shoal[rb.fish_id].curr_min_pos = Vector(max(0,curr_min_pos.x),max(curr_min_pos.y,limits[shoal[rb.fish_id].type+1][0]))
        shoal[rb.fish_id].curr_max_pos = Vector(min(10000,curr_max_pos.x),min(curr_max_pos.y,limits[shoal[rb.fish_id].type+1][1]))
        shoal[rb.fish_id].curr_speed = shoal[rb.fish_id].curr_pos()-shoal[rb.fish_id].prev_pos()
        

def end_of_turn_positions(shoal:Dict[int,Fish]):
    for creature in shoal.values():
        if creature.type == -1:
            monster=creature
            if monster.curr_speed.mag() > 500 or monster.status == "aggressive":
                monster.next_speed = monster.curr_speed.unit()*270
                monster.status = "non-agressive"
            else:
                monster.next_speed = monster.curr_speed
            drone_prox = 100000
            closest_drone = ""
            for drone in drone_by_id.values():
                drone_dist = dist(drone.pos,monster.curr_pos())
                if drone_dist < 800 + (drone.light * 1200):
                    if drone_dist < drone_prox:
                        drone_dost = drone_prox
                        closest_drone = drone
                    # monster into agressive status
                    monster.status = 'Aggressive'
                    # head towards closest drone
                    chase_dir = drone.pos - monster.curr_pos()
                    chase_speed = 540
                    monster.next_speed = chase_dir.unit()*chase_speed
                    monster.next_max_pos = monster.curr_max_pos+monster.next_speed
                    monster.next_min_pos = monster.curr_min_pos+monster.next_speed
                    print(f"hello monster {monster.fish_id}", file=sys.stderr, flush=True)
            
                
            # test for proximity of drones
            # if any within ??? find the closest
            # monster will move towards the closest drone with aggressive speed
            pass
            # if none nearby then continue to move as before
            
        if creature.type in (0,1,2):
            #use current position and speed to predict next position
            creature.next_max_pos = creature.curr_max_pos + creature.curr_speed
            creature.next_min_pos = creature.curr_min_pos + creature.curr_speed
        


def show_game_state():
    print(f"************************************", file=sys.stderr, flush=True)
    print(f"At the start of turn {g.turn}", file=sys.stderr, flush=True)
    print(f"************************************", file=sys.stderr, flush=True)
    for d in drone_by_id:
        if d==0 or d==2:
            print(f"Drone {d} is at {drone_by_id[d].pos}", file=sys.stderr, flush=True)
            print(f"{drone_by_id[d].status}", file=sys.stderr, flush=True)
            print(f"-----------:--------------------------------------", file=sys.stderr, flush=True)
            for cr in visible_fish:
                if shoal[cr].type == -1:
                    print(f"monster {cr} at {shoal[cr].pos} heading {shoal[cr].curr_speed} dist: {int(dist(drone_by_id[d].pos,shoal[cr].curr_pos()))}", file=sys.stderr, flush=True)
            print(f"************************************", file=sys.stderr, flush=True)    

                        
def current_value(f):
    #set the value of a given fish based on the type and who has already scanned / landed that fish color / type
    base_value = shoal[f].type
    fish_value = base_value
    if f not in foe_scans:
        fish_value *= 2

    return base_value

# for a given drone_id return the value of going to the surface
def surface_value(d: int) -> int:
    payload_value = 0
    for s in drone_by_id[d].scans:
        if s not in foe_scans:
            payload_value += (shoal[s].type+1)
            #TODO add value of all color and all type points
        for fd in foe_drones:
            if s in drone_by_id[fd.drone_id].scans:
                payload_value += (shoal[s].type+1)*2


    return payload_value

def drone_time_to_surface(d:int)->int:
    time_to_surface = math.ceil((drone_by_id[d].pos.y-500)/600)
    return time_to_surface

def turns_to_target(pos:Vector,tar:Vector,speed:int) -> int:
    distance = dist(pos,tar)
    turns = math.ceil(distance/speed)
    return turns

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

def closest_target(d:int) ->int:
    prox = 100000
    ct = -1
    for t in targets:
        distance = dist(shoal[t.target_id].curr_pos(),drone_by_id[d].pos)
        if distance <prox:
            prox = distance
            ct = t.target_id
    print(f"Closest Target = {ct} at {int(prox)}", file=sys.stderr, flush=True)       
    return ct


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

def orientation(p:Vector, q:Vector, r:Vector): 
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
    

    #TODO refactor to change d from drone to Vector
    # find speed of drone
    dspeed = dist(d.pos,t)

    # find intercept with edge at proposed vector
    right_edge = (Vector(100001,-1),Vector(100001,100001))
    left_edge = (Vector(-1,-1),Vector(-1,10001))
    top_edge = (Vector(-1,-1),Vector(10001,-1))
    bottom_edge = (Vector(-1,10001),Vector(10001,10001))
    proposed_target = t
    proposed_move = t-d.pos

    if doIntersect(right_edge[0],right_edge[1],d.pos,proposed_target):
        #intersects with right edge
        proposed_move.x = 9999-d.pos.x
        proposed_move.y = math.sqrt(dspeed**2-(proposed_move.x)**2)
        print(f"Avoiding right wall", file=sys.stderr, flush=True)


    if doIntersect(left_edge[0],left_edge[1],d.pos,proposed_target):
        #intersects with left edge
        proposed_move.x = 1-d.pos.x
        proposed_move.y = math.sqrt(dspeed**2-(proposed_move.x)**2)
        print(f"Avoiding left wall", file=sys.stderr, flush=True)

    if d.pos.y+proposed_move.y>10000:
        proposed_target.y = d.pos.y - proposed_move.y
    else:
        proposed_target.y = d.pos.y + proposed_move.y

    if doIntersect(top_edge[0],top_edge[1],d.pos,proposed_target):
        #intersects with top edge
        proposed_move.y = 1-d.pos.y
        proposed_move.x= proposed_move.x
        print(f"Avoiding top", file=sys.stderr, flush=True)


    if doIntersect(bottom_edge[0],bottom_edge[1],d.pos,proposed_target):
        #intersects with bottom edge
        proposed_move.y = 9999-d.pos.y
        proposed_move.x = math.sqrt(dspeed**2-(proposed_move.x)**2)
        print(f"Avoiding bottom", file=sys.stderr, flush=True)

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
#limits holds maximum for x,y and speed of each creature type
limits=[(2500,10000,540),(2500,5000,200),(5000,7500,200),(7500,10000,200)]
my_scans: List[int] = []
foe_scans: List[int] = []
foe_new_scans: List[List] = []
drone_by_id: Dict[int, Drone] = {}
foe_drones: List[Drone] = []
visible_fish: Dict[int,Fish] = {}
my_radar_blips: List[RadarBlip] = []
targets: List[Target] = []
shoal: Dict[int, Fish] = {}
planned_path = Vector(0,0)
my_score = 0
foe_score = 0

def initialise_game():
    
    fish_count = int(input())
    for _ in range(fish_count):

        fish_id, color, _type = map(int, input().split())
        new_fish = Fish(fish_id,Vector(-1,-1),Vector(10000,10000),Vector(0,0),Vector(10000,10000),Vector(0,0),Vector(10000,10000),
                        Vector(0,0),Vector(0,0),Vector(0,0),Vector(0,0),color,_type,"not set")
        shoal[fish_id] = new_fish


    for d in range(4):
        new_drone = Drone(d,Vector(-1,-1),False,-1,[],'',Vector(-1,-1),0)
        drone_by_id[d] = new_drone


def initialise_loop():
    my_scans.clear()
    foe_scans.clear()
    foe_new_scans.clear()
    foe_drones.clear()
    visible_fish.clear()
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
        if fish_id not in drone_by_id[drone_id].scans and drone_by_id[drone_id].owner == 'foe':
            foe_new_scans.append([drone_id,fish_id])

    visible_fish_count = int(input())
    for _ in range(visible_fish_count):
        status = "Not Set"
        fish_id, fish_x, fish_y, fish_vx, fish_vy = map(int, input().split())
        vpos = Vector(fish_x, fish_y)
        vspeed = Vector(fish_vx, fish_vy)
        if vspeed.mag()>500:
            status = "Aggressive"
        elif vspeed.mag()>0:
            status = "swimming"
        else:
            status = "still"
        visible_fish[fish_id] = Fish(fish_id,vpos,vpos-vspeed,vpos-vspeed,vpos,vpos,vpos+vspeed,vpos+vspeed,vspeed,vspeed,vspeed,
                                    shoal[fish_id].color,shoal[fish_id].type,status)

    # if we can see thee fish update the pos and speed, if not reset visible to False
    for f in shoal: 
        if f in visible_fish:
            shoal[f].pos=visible_fish[f].pos
            shoal[f].curr_max_pos = visible_fish[f].pos
            shoal[f].curr_min_pos = visible_fish[f].pos
            shoal[f].curr_speed= visible_fish[f].curr_speed
            shoal[f].visible = True
        else:
            #needs to be updated
            shoal[f].visible = False

    
    my_radar_blip_count = int(input())
    for _ in range(my_radar_blip_count):
        drone_id, fish_id, dir = input().split()
        drone_id = int(drone_id)
        fish_id = int(fish_id)
        my_radar_blips.append(RadarBlip(drone_id,fish_id,dir))
            
        

# game initialisation

g=game()

closest_test()

initialise_game()

# game loop

while True:
    g.turn += 1
    initialise_loop()
    
    #update current position information based on radar and known/estimated 
    update_fish()
    
    #forecast the position of fish, drones and monsters at the end of the turn
    end_of_turn_positions(shoal)
    
    #create list of targets
    new_targets()


    #for each drone find best target or surface

    #check if there is a monster en route

    #
    show_game_state()
    
    planned_path = Vector(0,0)
    speed = 600
    holding_scans = []
    for drone in drone_by_id:
        if drone_by_id[drone].owner == "me":
            for s in drone_by_id[drone].scans:
                holding_scans.append(s)
    
    double_surface_score = score_for_scan(holding_scans) + my_score

    for drone in drone_by_id:
        if drone_by_id[drone].owner == "me":
            max_value =-1000000 
            target_vector = Vector(0,0)
            target_fish = -1
            light = 0
            # criteria for going to surface
            #if there are less than 2 targets remaining
            if len(targets)<5:
                target_vector = Vector(drone_by_id[drone].pos.x,500)-drone_by_id[drone].pos
                drone_by_id[drone].status = "surface drop off"
            else:
                for t in targets:
                    target_value = 0
                    if t.status != "owned":
                        if t.target_id not in my_scans:
                            if t.target_id not in drone_by_id[drone].scans:
                                #distance to target
                                targetd = dist(drone_by_id[drone].pos,shoal[t.target_id].next_pos())
                                target_value -= targetd
                                #target_value += t.value
                                if target_value> max_value: 
                                    max_value = target_value
                                    target_fish = t.target_id
                                    target_vector = shoal[t.target_id].next_pos() - drone_by_id[drone].pos
                                    t.status = 'owned'
                if target_fish != -1:
                    drone_by_id[drone].status = "heading for fish " + str(target_fish) + " at " + str(shoal[target_fish].next_pos())+" min:"+str(shoal[target_fish].next_min_pos.x)+" max:"+str(shoal[target_fish].next_max_pos.x)
            planned_path = target_vector.unit()*speed
            # is the target path intercepted by a monster
                        

            light_check = dist(drone_by_id[drone].pos,shoal[closest_target(drone)].curr_pos())     

            if light_check < 2000:
                light = 1   
            else:
                light = 0

            planned_target = planned_path + drone_by_id[drone].pos
            #planned_target = edge_move(drone_by_id[drone],planned_target)
            my_max_score = foe_possible_score(foe_scans)
            foe_max_score = foe_possible_score(my_scans)
            my_surface_value = surface_value(drone)
            print(f"Max Score {str(my_max_score)} Surface {str(my_surface_value)}", file=sys.stderr, flush=True)
            

            print(f"MOVE {int(planned_target.x)} {int(planned_target.y)} {light} {str(drone_by_id[drone].speed)}")



    