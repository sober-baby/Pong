# Alpha 1.0 uses imperfect defense
# Alpha 2.0 uses more precise defense
# when not hit ball, it is returned to middle
# only defense, no attack method is considered
# Alpha 2.0 为胜率最低的alpha组
# 相比于alpha1.0 胜率6.2：1， alpha 1.5 胜率5：1
# alpha2.0 对chaser胜率大概在 4：1， 但是更为稳定
# 此版本比较适合娱乐或人工对战

#######
#用于模拟的class
import pygame, sys, time, random, os
from pygame.locals import *
import math

class fRect:
    def __init__(self, pos, size):
        self.pos = (pos[0], pos[1])
        self.size = (size[0], size[1])
    def move(self, x, y):
        return fRect((self.pos[0]+x, self.pos[1]+y), self.size)
    def move_ip(self, x, y, move_factor = 1):
        self.pos = (self.pos[0] + x*move_factor, self.pos[1] + y*move_factor)
    def get_rect(self):
        return Rect(self.pos, self.size)
    def copy(self):
        return fRect(self.pos, self.size)
    def intersect(self, other_frect): # two rectangles intersect iff both x and y projections intersect
        for i in range(2):
            if self.pos[i] < other_frect.pos[i]: # projection of self begins to the left
                if other_frect.pos[i] >= self.pos[i] + self.size[i]:
                    return 0
            elif self.pos[i] > other_frect.pos[i]:
                if self.pos[i] >= other_frect.pos[i] + other_frect.size[i]:
                    return 0
        return 1#self.size > 0 and other_frect.size > 0

class nBall:
    def __init__(self, table_size, size, paddle_bounce, wall_bounce, dust_error, speed, pos):
        self.frect = fRect((pos[0], pos[1]), size)
        self.speed = speed[0], speed[1]
        self.size = size
        self.paddle_bounce = paddle_bounce
        self.wall_bounce = wall_bounce
        self.dust_error = dust_error
        self.prev_bounce = None
    def get_center(self):
        return (self.frect.pos[0] + .5*self.frect.size[0], self.frect.pos[1] + .5*self.frect.size[1])
    def get_speed_mag(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)
    def factor_accelerate(self, factor):
        self.speed = (factor*self.speed[0], factor*self.speed[1])
    def movewall(self, table_size, move_factor):
        moved = 0
        walls_Rects = [Rect((-100, -100), (table_size[0]+200, 100)),
                       Rect((-100, table_size[1]), (table_size[0]+200, 100))]
        for wall_rect in walls_Rects:
            if self.frect.get_rect().colliderect(wall_rect):
                c = 0
                #print "in wall. speed: ", self.speed
                while self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)
                    c += 1 # this basically tells us how far the ball has traveled into the wall
                r1 = 1+2*(random.random()-.5)*self.dust_error
                r2 = 1+2*(random.random()-.5)*self.dust_error
                self.speed = (self.wall_bounce*self.speed[0]*r1, -self.wall_bounce*self.speed[1]*r2)
                while c > 0 or self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)
                    c -= 1 # move by roughly the same amount as the ball had traveled into the wall
                moved = 1
                #print "out of wall, position, speed: ", self.frect.pos, self.speed
        if not moved:
            self.frect.move_ip(self.speed[0], self.speed[1], move_factor)

#records the current velocity of the ball
global spvb
spvb = 0,0
#records the last 2 position of the ball
global bpl
bpl = []

global estpx,estpy
estpx,estpy = 0,0

global testify
testify = 0

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global spvb
    global bpl
    global testify
    global estpx,estpy
    recordp(ball_frect)
    if len(bpl) != 2:
        return None
    curv = findcv(bpl)
    #the folloing is not used becaue the "hit" last for a while
    #if less calculation is needed, consider open and fix this function by making the 2nd loop run for more than 10 times
    # judge = idb(spvb,curv)
    '''
    if judge == -1:
        print("update")
        testify = 0
    '''
    spvb = curv
    '''
    if testify == 0:
        estpx,estpy = predict_position_acc(table_size,spvb,ball_frect)
        testify = 1
    '''
#exist error in wall bounce? almost none with acc_predict 
    estpx,estpy = predict_position_acc(table_size,spvb,ball_frect)
    tesx, tesy = predict_position(spvb,ball_frect)
    ttx,tty = pure_mirror_prediction(spvb,ball_frect)
    print (tesy - estpy)
    print ("pure mirror", tty - estpy)
    #The following function is alpha 1.0
    # estpx,estpy = predict_position(spvb,ball_frect)
    if (estpx == 25 and paddle_frect.pos[0] == 15) or (estpx == 415 and paddle_frect.pos[0] == 415):
        #u need to pick the ball
        #just pick for now, if possible don't move so that it can be improved
    #This is an update from alpha 2.0, for defense purposes, it is created to hit with mid
    #because error in prediction do exist
    #Alpha 2.0 is to be made only make precise defense when hitting to us 
        '''
        if ioin(paddle_frect,estpy)[0]:
            return None
        if not ioin(paddle_frect,estpy)[0]:
            return ioin(paddle_frect,estpy)[1]
            '''
        return ioin(paddle_frect,estpy)[1]
    else:
        # now is back to middle, maybe improve
        return ioin(paddle_frect,140)[1]

#records the last 2 position of the ball
def recordp(ball_frect):
    global bpl
    if len(bpl) == 2:
        bpl[0] = bpl[1]
        bpl[1] = ball_frect.pos
    else:
        bpl.append(ball_frect.pos)

#records the current velocity of the ball
def findcv(l):
    return l[1][0]-l[0][0], l[1][1]-l[0][1]

#returns a tuple indicating whether the paddle is in the given value and centre is up or down
#inidicate which way it should go
def ioin(paddle_frect,ey):
    ty = paddle_frect.pos[1]
    by = ty+paddle_frect.size[1]
    midy = (ty+by)/2
    if ey>=ty and ey<=by:
        if midy == ey:
            return True, None
        elif midy > ey: 
            return True, "up"
        elif midy < ey:
            return False, "down"
    elif ey<ty:
        return False, "up"
    elif ey>by:
        return False, "down"




#returns the x,y where the ball will reach, x= {25,415}
def predict_position_acc(table_size,pairvelocity,ball_frect):
# actual axis are at 440-20-10 and 20+10
# find the accurate landing position based on simulating 
    spx,spy =  pairvelocity
    if spx == 0:
        return 415, 140
    ball = nBall(table_size, (15, 15), 1.2, 1, 0, pairvelocity, ball_frect.pos)
    if spx > 0: #to the right  
        while ball.frect.pos[0] <= 415:
            inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5)
            if inv_move_factor > 0:
                for i in range(inv_move_factor):
                    ball.movewall(table_size, 1./inv_move_factor)
            else:
                ball.movewall(table_size, 1)
        return 415, ball.frect.pos[1]
    elif spx< 0: # to the left
        while ball.frect.pos[0] >= 25:
            inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5)
            if inv_move_factor > 0:
                for i in range(inv_move_factor):
                    ball.movewall(table_size, 1./inv_move_factor)
            else:
                ball.movewall(table_size, 1)
        return 25, ball.frect.pos[1]



# convert y in any range to [0,280]，本函数应该无误
# 球的本身有15*15
# 所以[0, 265]
def mvir(y):
    xx = 265
    yy = 2*xx
    while y < 0:
        y+= yy
    while y > yy:
        y-= yy
    if y>xx:
        y = yy - y
    if y<=xx and y>=0: #just for checking
        return y 


#returns the x,y where the ball will reach, x= {25,415}
#为了确保函数的精确性，这个函数应该做到和模拟一样的效果，即不随墙弹而改变
def predict_position(pairvelocity,ball_frect):
#实际判断落点为x=25,x=415
    spx,spy =  pairvelocity
    if spx == 0:
        return 415, 140
    if spx > 0: #to the right  
        actual_y = (spy/spx)*(415-ball_frect.pos[0]) + ball_frect.pos[1]
        return 415,mvir(actual_y)
    elif spx< 0: # to the left
        actual_y = (spy/spx)*(25-ball_frect.pos[0]) + ball_frect.pos[1]
        return 25,mvir(actual_y)

'''
def pure_mirror_prediction(velo, ball_frect):
    test_bound = 265
    vx, vy, xp, yp = velo[0], velo[1], ball_frect.pos[0], ball_frect.pos[1]
    #equation of line is  y = (vy/vx)(x - xp) + yp 
    # x = (vx/vy)(y-yp) +xp
    if vx == 0:
        return 415, 125
    elif vx >0: # to thr right
        predict_y  = (vy/vx)*(415 - xp) + yp
    else: # to th e left
        predict_y  = (vy/vx)*(25 - xp) + yp
    if predict_y < 0:
            hit_wall_x = (vx/vy)*(0-yp) +xp
            # print(hit_wall_x)
            ball_frect.pos = hit_wall_x,0
            pure_mirror_prediction((vx,-vy),ball_frect)
    elif predict_y > test_bound:
            hit_wall_x = (vx/vy)*(test_bound-yp) +xp
            # print(hit_wall_x)
            ball_frect.pos = hit_wall_x,test_bound
            pure_mirror_prediction((vx,-vy),ball_frect)
    else:
            return predict_y
'''
