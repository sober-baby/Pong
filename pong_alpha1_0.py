# Alpha 1.0 uses imperfect defense

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


class Paddle:
    def __init__(self, pos, size, speed, max_angle,  facing, timeout):
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.facing = facing
        self.max_angle = max_angle
        self.timeout = timeout

    def factor_accelerate(self, factor):
        self.speed = factor*self.speed


    def move(self, enemy_frect, ball_frect, table_size):
        direction = self.move_getter(self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size))
        #direction = timeout(self.move_getter, (self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size)), {}, self.timeout)
        if direction == "up":
            self.frect.move_ip(0, -self.speed)
        elif direction == "down":
            self.frect.move_ip(0, self.speed)

        to_bottom = (self.frect.pos[1]+self.frect.size[1])-table_size[1]

        if to_bottom > 0:
            self.frect.move_ip(0, -to_bottom)
        to_top = self.frect.pos[1]
        if to_top < 0:
            self.frect.move_ip(0, -to_top)

    #never used, no need to read
    def get_face_pts(self):
        return ((self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1]),
                (self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1] + self.frect.size[1]-1)
                )
    #

    def get_angle(self, y):
        center = self.frect.pos[1]+self.size[1]/2
        rel_dist_from_c = ((y-center)/self.size[1])
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        sign = 1-2*self.facing

        return sign*rel_dist_from_c*self.max_angle*math.pi/180

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
    def move(self, paddles, table_size, move_factor):
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

        for paddle in paddles:
            if self.frect.intersect(paddle.frect):
                # 1 is left, 0 is right
                if (paddle.facing == 1 and self.get_center()[0] < paddle.frect.pos[0] + paddle.frect.size[0]/2) or \
                (paddle.facing == 0 and self.get_center()[0] > paddle.frect.pos[0] + paddle.frect.size[0]/2):
                    continue

                c = 0

                while self.frect.intersect(paddle.frect) and not self.frect.get_rect().colliderect(walls_Rects[0]) and not self.frect.get_rect().colliderect(walls_Rects[1]):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)
                    
                    c += 1
                theta = paddle.get_angle(self.frect.pos[1]+.5*self.frect.size[1])

###
                v = self.speed

                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                             math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0]

                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                              math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]
 

                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                if  v[0]*(2*paddle.facing-1) < 1: # ball is not traveling (a) away from paddle (b) at a sufficient speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) # transform y velocity so as to maintain the speed
                    v[0] = (2*paddle.facing-1) # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to increase by *1.2

                #a bit hacky, prevent multiple bounces from accelerating
                #the ball too much
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce, v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle
                #print "transformed speed: ", self.speed
###
                while c > 0 or self.frect.intersect(paddle.frect):
                    #print "move_ip()"
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)
                    #print "ball position forward trace: ", self.frect.pos
                    c -= 1
                #print "pos final: (" + str(self.frect.pos[0]) + "," + str(self.frect.pos[1]) + ")"
                #print "speed x y: ", self.speed[0], self.speed[1]

                moved = 1
                #print "out of paddle, speed: ", self.speed

        # if we didn't take care of not driving the ball into a wall by backtracing above it could have happened that
        # we would end up inside the wall here due to the way we do paddle bounces
        # this happens because we backtrace (c++) using incoming velocity, but correct post-factum (c--) using new velocity
        # the velocity would then be transformed by a wall hit, and the ball would end up on the dark side of the wall

        if not moved:
            self.frect.move_ip(self.speed[0], self.speed[1], move_factor)
            #print "moving "
        #print "poition: ", self.frect.pos


#records the current velocity of the ball
global spvb
spvb = 0,0
#records the last 2 position of the ball
global bpl
bpl = []

global estpx,estpy,iax, iay
estpx,estpy,iax, iay = 0,0,0,0

global testify
testify = 0

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global spvb
    global bpl
    global testify
    global estpx,estpy,iax, iay
    recordp(ball_frect)
    if len(bpl) != 2:
        return None
    curv = findcv(bpl)
    #the folloing is not used becaue the "hit" last for a while
    #if less calculation is needed, consider open and fix this function by making the 2nd loop run for more than 10 times
    judge = idb(spvb,curv)
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
    estpx,estpy = predict_position(spvb,ball_frect)
    iax, iay = predict_hit(spvb,ball_frect)
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


#detect what happened, -1 is paddle bounce, 0 is nothing, 1 is wall bounce
#due to some reason, this is not helping the program to run properly
def idb(last_updated_v, curr_v):
    if last_updated_v == curr_v:
        return 0
    elif last_updated_v[0] * curr_v[0] < 0:
        return -1
    return 1

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


# convert y in any range to [0,280]
def mvir(y):
    while y < 0:
        y+=560
    while y > 560:
        y-=560
    if y>280:
        y = 560 - y
    if y<=280 and y>=0: #just for checking
        return y 


#returns the x,y where the ball will reach, x= {25,415}
def predict_position(pairvelocity,ball_frect):
# actual axis are at 25，415(not sure why)
    spx,spy =  pairvelocity
    if spx == 0:
        return 415, 140
    if spx > 0: #to the right  
        actual_y = (spy/spx)*(415-ball_frect.pos[0]) + ball_frect.pos[1]
        return 415,mvir(actual_y)
    elif spx< 0: # to the left
        actual_y = (spy/spx)*(25-ball_frect.pos[0]) + ball_frect.pos[1]
        return 25,mvir(actual_y)

#这是一个用于预测我方击球后对方回球中位
#考虑到此函数对准确性判断不高,因为击球本身就有误差，且有可能要在后续运算中“预判”
#故选取alpha1.0中的数理判断
def predict_hit(pairvelocity,ball_frect):
    spx,spy =  pairvelocity
    if spx == 0:
        return 415, 140
    if spx > 0: #to the right  
        actual_y = (spy/spx)*(415+390-ball_frect.pos[0]) + ball_frect.pos[1]
        return 25,mvir(actual_y)
    elif spx< 0: # to the left
        actual_y = (spy/spx)*(25-390-ball_frect.pos[0]) + ball_frect.pos[1]
        return 415,mvir(actual_y)

#这是一个用于预测我方击球后对方回球中位
#考虑两者的相似性，顺手写的
#故选取alpha2.0中的模拟判断
#注意@@@ 这个函数没有完成，因为发现没算预判速度，所以比较麻烦...况且如果改predict——acc，全都要修改
#如果需要新预判，请复制predict——acc，并更改返回值
#！请注意，这不是完全模拟判断，而是根据alpha2.0的逻辑写出的预判
#若有需要，请在beta2.0版本进行修改
def predict_hit_acc(pairvelocity,ball_frect):
    pass
#
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

#This following codes are for simulation:::
#######
    #This is for simulation body code
        inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5)
        if inv_move_factor > 0:
            for i in range(inv_move_factor):
                ball.move(paddles, table_size, 1./inv_move_factor)
        else:
            ball.move(paddles, table_size, 1)

"""
def init_game():
    table_size = (440, 280)
    paddle_size = (10, 70)
    ball_size = (15, 15)
    paddle_speed = 1
    max_angle = 45

    paddle_bounce = 1.2
    wall_bounce = 1.00
    dust_error = 0.00
    init_speed_mag = 2
    timeout = 0.0003

    paddles = [Paddle((20, table_size[1]/2), paddle_size, paddle_speed, max_angle,  1, timeout),
               Paddle((table_size[0]-20, table_size[1]/2), paddle_size, paddle_speed, max_angle, 0, timeout)]
    ball = Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag)

    
"""

