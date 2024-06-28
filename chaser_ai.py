def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    '''return "up" or "down", depending on which way the paddle should go to
    align its centre with the centre of the ball, assuming the ball will
    not be moving
    
    Arguments:
    paddle_frect: a rectangle representing the coordinates of the paddle
                  paddle_frect.pos[0], paddle_frect.pos[1] is the top-left
                  corner of the rectangle. 
                  paddle_frect.size[0], paddle_frect.size[1] are the dimensions
                  of the paddle along the x and y axis, respectively
    
    other_paddle_frect:
                  a rectangle representing the opponent paddle. It is formatted
                  in the same way as paddle_frect
    ball_frect:   a rectangle representing the ball. It is formatted in the 
                  same way as paddle_frect
    table_size:   table_size[0], table_size[1] are the dimensions of the table,
                  along the x and the y axis respectively
    
    The coordinates look as follows:
    
     0             x
     |------------->
     |
     |             
     |
 y   v
    '''          
    
    if paddle_frect.pos[1]+paddle_frect.size[1]/2 < ball_frect.pos[1]+ball_frect.size[1]/2:
     return "down"
    else:
     return "up"

#records the current velocity of the ball
global spvb
spvb = 0,0
#records the last 2 position of the ball
global bpl
bpl = []


def pong_ai1(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global spvb
    global bpl
    recordp(ball_frect)
    if len(bpl) != 2:
        return None
    curv = findcv(bpl)
    judge = idb(spvb,curv)
    spvb = curv
    #exist error in wall bounce?
    estpx,estpy = predict_position(spvb,ball_frect)
    if (estpx == 30 and paddle_frect.pos[0] == 15) or (estpx == 410 and paddle_frect.pos[0] == 415):
        #u need to pick the ball
        #just pick for now, if possible don't move so that it can be improved
        if ioin(paddle_frect,estpy)[0]:
            return None
        if not ioin(paddle_frect,estpy)[0]:
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


#returns the x,y where the ball will reach, x= {30,410}
def predict_position(pairvelocity,ball_frect):
# actual axis are at 440-20-10 and 20+10
#figure out how sides are changed and how direction is(signs) is found
    spx,spy =  pairvelocity
    if spx == 0:
        return 410, 140
    if spx > 0: #to the right  
        actual_y = (spy/spx)*(410-ball_frect.pos[0]) + ball_frect.pos[1]
        return 410,mvir(actual_y)
    elif spx< 0: # to the left
        actual_y = (spy/spx)*(30-ball_frect.pos[0]) + ball_frect.pos[1]
        return 30,mvir(actual_y)

#框架思路：
    #完美判断落点，出球时取中位
    #击球尽可能往远处击打