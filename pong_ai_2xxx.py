import math     
import numpy as np
v2_coord = [[0,0],[0,0]]
prevwin = False
addfac = 35
iterations = 20

def get_angle(frect, newpos, y, v_x):
    '''
    This formula is copied from the original code
    '''

    center = newpos+frect.size[1]/2
    rel_dist_from_c = ((y-center)/frect.size[1])
    rel_dist_from_c = min(0.5, rel_dist_from_c)
    rel_dist_from_c = max(-0.5, rel_dist_from_c)
    if v_x > 0:
        sign = 1-2*0
    else:
        sign = 1-2*1
    # print(sign*rel_dist_from_c*45*math.pi/180)
    return sign*rel_dist_from_c*45*math.pi/180

def predict_speed(table_size, paddle_frect, newpos, predict_y, ball_frect, v_x, v_y, theta=None):
    '''
    Predicts the velocity of a ball after a bounce
    '''

    if v_x > 0:
        # Total y displacement
        effective_width = paddle_frect.pos[0] - 15

    elif v_x < 0:
        effective_width = paddle_frect.pos[0] + paddle_frect.size[0]
    
    effective_height = table_size[1] - 15

    if not v_x == 0:
        y_T = (v_y/v_x) * (effective_width-ball_frect.pos[0])
    else:
        y_T = effective_height/2

    dist_to_bottom = effective_height - ball_frect.pos[1]

    num_collisions = math.floor((y_T-dist_to_bottom)/(table_size[1] - 15))

    if theta == None:
        theta = get_angle(paddle_frect, newpos, predict_y + 0.5*ball_frect.size[1],v_x)

    v = [v_x, v_y]

    # Final vertical velocity can be either upwards or downwards depending on the bounces
    if num_collisions % 2 == 0:   ##Changes made here
        v[1] = -v[1]

    # Essentially a double angle rotation
    v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
         math.sin(theta)*v[0]+math.cos(theta)*v[1]]
    v[0] = -v[0]
    v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
         math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]

    # Boost speed by a constant factor
    v = (v[0]*1.2, v[1]*1.2)

    return v


def iswin_towards_us(table_size, other_paddle_frect,v_x, v_y, x, y,predict_x,predict_y):
    '''
    Will we win??
    '''
    temp = False

    if(v_x == 0):
        return False
    elif v_x < 0:
        # Total y displacement
        effective_width = other_paddle_frect.pos[0] - 15
    elif v_x > 0:
        effective_width = other_paddle_frect.pos[0] + other_paddle_frect.size[0]
    effective_height = table_size[1] - 15
    t = abs((x - effective_width)/v_x)

    # There are three cases to block

    # Case 1: the ball is going to hit the paddle if it stays still
    if other_paddle_frect.pos[1] < predict_y < other_paddle_frect.pos[1] + other_paddle_frect.size[1]:
        temp = False

    # Case 2: top of paddle can reach ball in time if it moves
    elif predict_y < other_paddle_frect.pos[1]:
        if(abs(predict_y - other_paddle_frect.pos[1]) > 2*t + 10):
            temp = True

    # Case 3: bottom of paddle can reach ball in time if it moves
    elif other_paddle_frect.pos[1] + other_paddle_frect.size[1] < predict_y:
        if(abs(predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1]) > 2*t + 5):
            temp = True

    return temp

def iswin_towards_them(table_size, other_paddle_frect,v_x, v_y, x, y,predict_x,predict_y):
    '''
    Will we win??
    '''
    temp = False

    if(v_x == 0):
        return False
    elif v_x > 0:
        # Total y displacement
        effective_width = other_paddle_frect.pos[0] - 15
    elif v_x < 0:
        effective_width = other_paddle_frect.pos[0] + other_paddle_frect.size[0]
    effective_height = table_size[1] - 15
    t = abs((x - effective_width)/v_x)

    # There are three cases to block

    # Case 1: the ball is going to hit the paddle if it stays still
    if other_paddle_frect.pos[1] < predict_y < other_paddle_frect.pos[1] + other_paddle_frect.size[1]:
        temp = False

    # Case 2: top of paddle can reach ball in time if it moves
    elif predict_y < other_paddle_frect.pos[1]:
        if(abs(predict_y - other_paddle_frect.pos[1]) > 2*t + 1):
            temp = True

    # Case 3: bottom of paddle can reach ball in time if it moves
    elif other_paddle_frect.pos[1] + other_paddle_frect.size[1] < predict_y:
        if(abs(predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1]) > 2*t + 1):
            temp = True

    return temp

def collision_predict(table_size, paddle_frect, x, y, v_x, v_y):
    # print(type(paddle_frect))
    if v_x > 0:
        # Total y displacement
        effective_width = paddle_frect.pos[0] - 15
    elif v_x < 0:
        effective_width = paddle_frect.pos[0] + paddle_frect.size[0]
    
    effective_height = table_size[1] - 15
    if(v_x) != 0:
        y_T = (v_y/v_x) * (effective_width-x)
    else:
        y_T = effective_height/2

    dist_to_bottom = effective_height - y

    num_collisions = math.floor((y_T-dist_to_bottom)/(effective_height)) # -15

    y_T = y_T - dist_to_bottom
    if num_collisions % 2 == 1:
        prediction = y_T % effective_height
    else:
        prediction = effective_height - (y_T % effective_height)
    return prediction

def count_bounces(table_size, paddle_frect, x, y, v_x, v_y):
    if v_x > 0:
        effective_width = paddle_frect.pos[0] - 15
    elif v_x < 0:
        effective_width = paddle_frect.pos[0] + paddle_frect.size[0]
    
    effective_height = table_size[1] - 15
    if(v_x) != 0:
        y_T = (v_y/v_x) * (effective_width-x)
    else:
        y_T = effective_height/2

    dist_to_bottom = effective_height - y

    num_collisions = math.floor((y_T-dist_to_bottom)/(effective_height)) # -15

    return abs(num_collisions)

def getspeed(x1,x2,y1,y2):
    return (x2-x1, y2-y1)  # (dx, dy)

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
    
    global addfac, iterations

    # Get velocity
    v2_coord.pop(0)
    v2_coord.append([ball_frect.pos[0],ball_frect.pos[1]])
    v_x, v_y = getspeed(v2_coord[0][0],v2_coord[1][0],v2_coord[0][1],v2_coord[1][1])
    
    # Right Side:
    if paddle_frect.pos[0] > table_size[0]/2:
        
        '''
        BALL COMING TOWARDS US
        '''
        if v_x > 0:

            '''
            WHERE BALL IS GOING TO LAND
            '''
            predict_y = collision_predict(
                table_size,
                paddle_frect,
                ball_frect.pos[0],
                ball_frect.pos[1],
                v_x,v_y)

            predict_x = paddle_frect.pos[0]


            '''
            OPTIMIZATION
            '''
            # Determine where paddle can move to
            t = 1
            if(v_x != 0): t = abs((ball_frect.pos[0] - predict_x)/v_x)
            maxdist = t*2

            # Furthest ball can be hit to the other side, we want to maximize this
            furthest = 0

            # Loop through possible hitting positions
            for i in np.arange(
                            1,
                            min((1+1/iterations)*maxdist, (1+1/iterations)*paddle_frect.size[1]),
                            min(maxdist/iterations, paddle_frect.size[1]/iterations)
                            ):
                ##Check positions to hit at.
                
                '''
                BOTTOM HALF
                '''
                if(predict_y > table_size[1]/2):

                    # Ensure ball doesn't go outside board
                    if(predict_y+ i < table_size[1]):

                        # Velocity after being hit
                        predict_v = predict_speed(table_size, paddle_frect, predict_y-paddle_frect.size[1] +i, predict_y, ball_frect, v_x, v_y)

                        # Where the ball will land on opponent side
                        opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])
                        
                        # Number of collisions when going towards opponent
                        num_collisions = count_bounces(
                            table_size,
                            other_paddle_frect,
                            predict_x,
                            predict_y,
                            predict_v[0], predict_v[1]
                        )

                        # Will we win?
                        is_win = iswin_towards_us(table_size,
                                        other_paddle_frect,
                                        predict_v[0],predict_v[1],
                                        predict_x,predict_y, 
                                        other_paddle_frect.pos[0], 
                                        opponent_predict_y
                                      )
                        current_distance = min(
                                abs(opponent_predict_y - other_paddle_frect.pos[1]),
                                abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1])
                            )

                        # If a win is guaranteed, stop searching.
                        if is_win:
                            addfac = i
                            break

                        # If not, optimize given two conditions:
                        # (1) Distance is farther than any before
                        # (2) There are at most 2 bounces
                        elif(
                            current_distance > furthest 
                            and
                            num_collisions <= 2
                        ):
                            # Change furthest
                            furthest = current_distance

                            # TODO: Condition to only move there sometimes, look into this efficacy
                            if(t > 30):
                                addfac = i
                else:
                    # Doesn't go outside board
                    if predict_y - i > 0:

                        # Velocity after being hit
                        predict_v = predict_speed(table_size, paddle_frect, predict_y-i, predict_y, ball_frect, v_x, v_y)
                        opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])

                        num_collisions = count_bounces(
                            table_size,
                            other_paddle_frect,
                            predict_x,
                            predict_y,
                            predict_v[0], predict_v[1]
                        )
                        
                        is_win = iswin_towards_us(table_size, other_paddle_frect,predict_v[0],predict_v[1],predict_x,predict_y, other_paddle_frect.pos[0], opponent_predict_y)

                        if is_win:
                            addfac = i
                            break

                        elif (
                            min(
                                abs(opponent_predict_y - other_paddle_frect.pos[1]),
                                abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1])
                            ) > furthest
                            and num_collisions <= 2
                        ):
                            furthest = min(abs(opponent_predict_y - other_paddle_frect.pos[1]), abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1]))
                            if(t>30):
                                addfac = i

            # final_opponent_predict_v = predict_speed(
            #     table_size, paddle_frect, predict_y-paddle_frect.size[1] + addfac, predict_y, ball_frect, v_x, v_y)
            # print("INCOMING PREDICT SPEED:", final_opponent_predict_v[0], final_opponent_predict_v[1])

            # final_opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,final_opponent_predict_v[0],final_opponent_predict_v[1])
            # # time_for_ball = (paddle_frect.pos[0]-other_paddle_frect.pos[0]) / final_opponent_predict_y[0]
            # if is_win:
            #     print("I PREDICT A WIN")
            '''
            def iswin_towards_ustable_size, other_paddle_frect,v_x, v_y, x, y,predict_x,predict_y):
            '''

            '''
            if(predict_y > table_size[1]/2):
                predict_v = predict_speed(table_size, paddle_frect, predict_y-paddle_frect.size[1] +20, predict_y, ball_frect, v_x, v_y)
                #predict_v = predict_speed(table_size,paddle_frect,predict_y -paddle_frect.size[1] + 10,predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])
            else:
                predict_v = predict_speed(table_size, paddle_frect, predict_y-20, predict_y, ball_frect, v_x, v_y)
                #predict_v = predict_speed(table_size,paddle_frect,predict_y - 10,predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])
            #print(t)
            '''
            #print(predict_v)
            #print(opponent_predict_y)
            #print(opponent_predict_y)
            #print(furthest)
            #print(addfac)

        else:  #Ball going to other paddle
            # print("OUTGOING SPEED",v_x,v_y)

            opponent_predict_y = collision_predict(table_size,other_paddle_frect,ball_frect.pos[0],ball_frect.pos[1],v_x,v_y)
            opponent_predict_x = other_paddle_frect.pos[0]+other_paddle_frect.size[0]
            #print(opponent_predict_y)
            minpredicty = table_size[1] - 15
            maxpredicty = 0
            t = 1  
            if(v_x != 0):
                t = abs((ball_frect.pos[0] - opponent_predict_x)/v_x)
            maxdist = t*2
            #temp = []
            for i in np.arange(1,min((1+1/iterations)*maxdist, (1+1/iterations)*paddle_frect.size[1]),min(maxdist/iterations, paddle_frect.size[1]/iterations)):
                if(opponent_predict_y > table_size[1]/2): # Bottom half
                    if(opponent_predict_y+ i < table_size[1]): # doesnt go outside board
                        opponent_predict_v = predict_speed(table_size, other_paddle_frect, opponent_predict_y-paddle_frect.size[1] +i, opponent_predict_y, ball_frect, v_x, v_y)
                        #opponent_predict_v = predict_speed(table_size,other_paddle_frect,opponent_predict_y -paddle_frect.size[1] + i,opponent_predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                        #print(opponent_predict_v)  ## THIS PLACE MATTERS BECAUSE V CHANGES BASED ON WHERE IT IS HIT
                        predict_y = collision_predict(table_size,paddle_frect,opponent_predict_x,opponent_predict_y,opponent_predict_v[0],opponent_predict_v[1])
                        if predict_y < minpredicty:
                            minpredicty = predict_y
                        if predict_y > maxpredicty:
                            maxpredicty = predict_y
                else:
                    if(opponent_predict_y - i > 0):
                        opponent_predict_v = predict_speed(table_size, other_paddle_frect, opponent_predict_y-i, opponent_predict_y, ball_frect, v_x, v_y)
                        #opponent_predict_v = predict_speed(table_size,other_paddle_frect,opponent_predict_y - i,opponent_predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                        #print(opponent_predict_v)  ## THIS PLACE MATTERS BECAUSE V CHANGES BASED ON WHERE IT IS HIT
                        predict_y = collision_predict(table_size,paddle_frect,opponent_predict_x,opponent_predict_y,opponent_predict_v[0],opponent_predict_v[1])
                        #print(opponent_predict_v)
                        if predict_y < minpredicty:
                            minpredicty = predict_y
                        if predict_y > maxpredicty:
                            maxpredicty = predict_y
                #temp.append(maxpredicty)
                    #print(predict_y)
            #print(temp)
                ## CAN BE MADE BETTER BY ONLY USING POSITIONS IT CAN REACH
            #print(minpredicty, maxpredicty)
            #print(temp)
            #print(minpredicty,maxpredicty)
            #print(v_x,v_y)
            predict_y = (minpredicty + maxpredicty)//2
            # if(predict_y < table_size[1]/2):
            #     predict_y = table_size[1]/4
            # else:
            #     predict_y = 3*table_size[1]/4
            #print(predict_y)
            #effective_width2 = other_paddle_frect.pos[0] + other_paddle_frect.size[0]
            #t1 = abs((ball_frect.pos[0] - effective_width2)/v_x)
            #print(t1)
            win = iswin_towards_them(table_size, other_paddle_frect,v_x, v_y, ball_frect.pos[0], ball_frect.pos[1],opponent_predict_x,opponent_predict_y)
            if(win == True):
                # print("I'm winning!", ball_frect.pos[0]/table_size[0])
                predict_y = table_size[1]/2
    
    else:
        if v_x < 0:

            predict_y = collision_predict(table_size,paddle_frect,ball_frect.pos[0],ball_frect.pos[1],v_x,v_y)
            predict_x = paddle_frect.pos[0] + paddle_frect.size[0]
            furthest = 0
            #addfac = paddle_frect.size[1]/2
            t = 1  
            if(v_x != 0):
                t = abs((ball_frect.pos[0] - predict_x)/v_x)
            maxdist = t*2

            for i in np.arange(1,min((1+1/iterations)*maxdist, (1+1/iterations)*paddle_frect.size[1]),min(maxdist/iterations, paddle_frect.size[1]/iterations)):
                ##Check positions to hit at.
                if(predict_y > table_size[1]/2): # Bottom half
                    if(predict_y+ i < table_size[1]): # doesnt go outside board

                        # Predict Velocity
                        predict_v = predict_speed(table_size, paddle_frect, predict_y-paddle_frect.size[1] +i, predict_y, ball_frect, v_x, v_y)
                        opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])

                        num_collisions = count_bounces(
                            table_size,
                            other_paddle_frect,
                            predict_x,
                            predict_y,
                            predict_v[0], predict_v[1]
                        )
                        
                        is_win = iswin_towards_us(table_size, other_paddle_frect,predict_v[0],predict_v[1],predict_x,predict_y, other_paddle_frect.pos[0], opponent_predict_y)

                        if is_win:
                            # print(ball_frect.pos[0]/table_size[0])
                            addfac = i
                            break


                        if(
                            min(
                                abs(opponent_predict_y - other_paddle_frect.pos[1]),
                                abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1])
                            ) > furthest
                            and 
                            num_collisions <= 2
                        ):
                            
                            furthest = min(abs(opponent_predict_y - other_paddle_frect.pos[1]), abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1]))
                            if(t > 30):
                                addfac = i

                else:
                    if(predict_y - i > 0): # doesnt go outside board
                        predict_v = predict_speed(table_size, paddle_frect, predict_y-i, predict_y, ball_frect, v_x, v_y)
                        opponent_predict_y = collision_predict(table_size,other_paddle_frect,predict_x,predict_y,predict_v[0],predict_v[1])

                        num_collisions = count_bounces(
                            table_size,
                            other_paddle_frect,
                            predict_x,
                            predict_y,
                            predict_v[0], predict_v[1]
                        )
                        
                        is_win = iswin_towards_us(table_size, other_paddle_frect,predict_v[0],predict_v[1],predict_x,predict_y, other_paddle_frect.pos[0], opponent_predict_y)

                        if is_win:
                            # print(ball_frect.pos[0]/table_size[0])
                            addfac = i
                            break

                        if(
                            min(
                                abs(opponent_predict_y - other_paddle_frect.pos[1]),
                                abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1])
                                ) > furthest
                            and
                            num_collisions <= 2
                            ):
                            
                            furthest = min(abs(opponent_predict_y - other_paddle_frect.pos[1]), abs(opponent_predict_y - other_paddle_frect.pos[1] - other_paddle_frect.size[1]))
                            if(t>30):
                                addfac = i
        else:
            # predict_y = table_size[1]/2
            opponent_predict_y = collision_predict(table_size,other_paddle_frect,ball_frect.pos[0],ball_frect.pos[1],v_x,v_y)
            opponent_predict_x = other_paddle_frect.pos[0]#+other_paddle_frect.size[0]
            #print(opponent_predict_y)
            minpredicty = table_size[1] - 15
            maxpredicty = 0
            t = 1
            if(v_x != 0):  
                t = abs((ball_frect.pos[0] - opponent_predict_x)/v_x)
            maxdist = t*2
            for i in np.arange(1,min((1+1/iterations)*maxdist,(1+1/iterations)*paddle_frect.size[1]),min(maxdist/iterations, paddle_frect.size[1]/iterations)):
                if(opponent_predict_y > table_size[1]/2): # Bottom half
                    if(opponent_predict_y+ i < table_size[1]): # doesnt go outside board
                        opponent_predict_v = predict_speed(table_size, other_paddle_frect, opponent_predict_y-paddle_frect.size[1] +i, opponent_predict_y, ball_frect, v_x, v_y)
                        #opponent_predict_v = predict_speed(table_size,other_paddle_frect,opponent_predict_y -paddle_frect.size[1] + i,opponent_predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                        #print(opponent_predict_v)  ## THIS PLACE MATTERS BECAUSE V CHANGES BASED ON WHERE IT IS HIT
                        predict_y = collision_predict(table_size,paddle_frect,opponent_predict_x,opponent_predict_y,opponent_predict_v[0],opponent_predict_v[1])
                        if predict_y < minpredicty:
                            minpredicty = predict_y
                        if predict_y > maxpredicty:
                            maxpredicty = predict_y
                else:
                    if(opponent_predict_y - i > 0):
                        opponent_predict_v = predict_speed(table_size, other_paddle_frect, opponent_predict_y-i, opponent_predict_y, ball_frect, v_x, v_y)
                        #opponent_predict_v = predict_speed(table_size,other_paddle_frect,opponent_predict_y - i,opponent_predict_y, ball_frect.pos[0], ball_frect.pos[1], v_x, v_y)
                        #print(opponent_predict_v)  ## THIS PLACE MATTERS BECAUSE V CHANGES BASED ON WHERE IT IS HIT
                        predict_y = collision_predict(table_size,paddle_frect,opponent_predict_x,opponent_predict_y,opponent_predict_v[0],opponent_predict_v[1])
                        if predict_y < minpredicty:
                            minpredicty = predict_y
                        if predict_y > maxpredicty:
                            maxpredicty = predict_y
                    #print(predict_y)

                ## CAN BE MADE BETTER BY ONLY USING POSITIONS IT CAN REACH
            #print(minpredicty, maxpredicty)
            #print(temp)
            predict_y = (minpredicty + maxpredicty)//2
            # if(predict_y < table_size[1]/2):
            #     predict_y = table_size[1]/4
            # else:
            #     predict_y = 3*table_size[1]/4
            win = iswin_towards_them(table_size, other_paddle_frect,v_x, v_y, ball_frect.pos[0], ball_frect.pos[1],opponent_predict_x,opponent_predict_y)
            if(win == True):
                predict_y = table_size[1]/2
    #print(v_x, v_y)


    if predict_y > table_size[1] / 2:   #### CHANGES HERE
        if predict_y - paddle_frect.size[1] + addfac > paddle_frect.pos[1]:# +paddle_frect.size[1]-35:    #-2
            return "down"
        else:
            return "up"
    elif predict_y == table_size[1] / 2:
        if predict_y > paddle_frect.pos[1] +paddle_frect.size[1]/2:
            return "down"
        else:
            return "up"
    else: 
        if predict_y - addfac > paddle_frect.pos[1]:
            return "down"
        else:
            return "up"