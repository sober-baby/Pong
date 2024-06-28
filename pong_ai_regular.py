import math,random

prev_ball_pos = [0,0]
ball_position_list = []

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    pong_ai.team_name = "Aitsuki Nakuru"
    global prev_ball_pos,ball_position_list
    #get centers and change frame
    ball_center = [ball_frect.pos[0] + 7.5, ball_frect.pos[1]]
    paddle_center = [paddle_frect.pos[0] + 5, paddle_frect.pos[1] + 27.5]
    other_center = [other_paddle_frect.pos[0] + 5, other_paddle_frect.pos[1] + 27.5]

    


    recordp(ball_frect)
    if len(ball_position_list) != 2:
        return "up"
    ball_speed = findcv(ball_position_list)

    collide_x= 400
    if ball_speed[0]<0:
        collide_x = 25
    if ball_speed[0] == 0:
        time_re = 1000000
    else:
        time_re = (collide_x - ball_frect.pos[0])/ball_speed[0]



    #move to center if ball is moving away    
    if (paddle_frect.pos[0]==15 and ball_speed[0]>=0)or(paddle_frect.pos[0]==415 and ball_speed[0]<=0):
        if paddle_frect.pos[1] < 105:
            return "down"
        else:
            return "up"

    espected_x_land,espected_y_land, speed_of_hit = predict_position(ball_speed,ball_frect,paddle_frect,table_size)
    ending_est = espected_y_land
    final_pos = espected_x_land,espected_y_land
    bounce_speed = [-speed_of_hit[0], speed_of_hit[1]]
    if length_of_vector(speed_of_hit)!=0:
        bounce_speed=unitwise(bounce_speed)

        found=False
        for i in range(5):

            if i%2==0:
                top=[other_center[0],-i*(280)]
                bot=[other_center[0],265+i*(280)]
            else:
                top=[other_center[0],265+i*(280)]
                bot=[other_center[0],-i*(280)]

            top_end, at=get_ending_est(top,final_pos,bounce_speed)
            bot_end, ab=get_ending_est(bot,final_pos,bounce_speed)

            tt,tb = 10000000, 10000000

            if at!="i":
                vvx,vvy = speed_of_hit
                vt = vvy*math.sin(2*at)-vvx*math.cos(2*at)
                tt = 390/abs(vt) + time_re
            if ab!="i":
                vvx,vvy = speed_of_hit
                vb = vvy*math.sin(2*ab)-vvx*math.cos(2*ab)
                tb = 390/abs(vb) + time_re

            # y -- ysin2-xcos2, xsin2+ycos2
                        
            ot = other_paddle_frect.pos[1]
            ob = 210 - other_paddle_frect.pos[1]

            if ob<=tb and ot<=tt:
                other_pos='middle'
            elif ob>tb:
                other_pos='bottom'
            else:
                other_pos='top'

            if top_end>=27.5 and top_end<=237.5 and bot_end>=27.5 and bot_end<=237.5:
                if other_pos=='middle':
                    if abs(top_end-paddle_center[1])<abs(bot_end-paddle_center[1]):
                        ending_est=top_end
                    else:
                        ending_est=bot_end
                elif other_pos=='bottom':
                    ending_est=top_end
                else:
                    ending_est=bot_end
                found=True
            elif top_end>=27.5 and top_end<=237.5:
                ending_est=top_end
                found=True
            elif bot_end>=27.5 and bot_end<=237.5:
                ending_est=bot_end
                found=True

            if found:
                break
            
        if not found:
            if ending_est>132.5:
                ending_est-=35
            else:
                ending_est+=35
                

    if paddle_center[1] < ending_est:
        return "down"
    else:
        return "up"

def recordp(ball_frect):
    global ball_position_list
    if len(ball_position_list) == 2:
        ball_position_list[0] = ball_position_list[1]
        ball_position_list[1] = ball_frect.pos
    else:
        ball_position_list.append(ball_frect.pos)

def findcv(l):
    return [l[1][0]-l[0][0], l[1][1]-l[0][1]]

def length_of_vector(L):
    re = 0
    for i in L:
        re += i**2
    return math.sqrt(re)

def unitwise(L):
    length_L = length_of_vector(L)
    for i in range(len(L)):
        L[i] = L[i] / length_L
    return L
    
def predict_position(speed,ball_frect,paddle_frect,table_size):
        vx, vy = speed
        re_xpos,re_ypos,re_vx,re_vy = 420,0,vx,vy
        if vx == 0:
            return re_xpos,re_ypos,speed
        elif vx>0:
            re_xpos = 420
        elif vx<0:
            re_xpos = 20
        distance_travel = abs(paddle_frect.pos[0] + paddle_frect.size[0]/2 - ball_frect.pos[0] - ball_frect.size[0]/2)-paddle_frect.size[0]/2-ball_frect.size[0]/2
        time_travel = abs(distance_travel/vx)
        actual_ypos = ball_frect.pos[1] + vy*time_travel
        if actual_ypos>=0 and actual_ypos<= table_size[1]-ball_frect.size[1]:
            re_ypos = actual_ypos
        else:
            if actual_ypos > table_size[1]-ball_frect.size[1]:
                actual_ypos -= (table_size[1]-ball_frect.size[1])
            number_of_reflections = abs(actual_ypos)//abs(table_size[1]-ball_frect.size[1])
            modulus = abs(actual_ypos)%abs(table_size[1]-ball_frect.size[1])
            parity = number_of_reflections%2
            if vy>=0:
                re_ypos = modulus
            else:
                re_ypos = (table_size[1]-ball_frect.size[1]) - modulus
            if parity == 0:
                re_vy = -vy
                re_ypos = (table_size[1]-ball_frect.size[1]) -re_ypos
        return re_xpos,re_ypos,[re_vx,re_vy]

def get_ending_est(target,cur_pos,bounce_speed):
    target_vec=[target[0]-cur_pos[0],target[1]-cur_pos[1]]
    target_vec_mag=math.sqrt(target_vec[0]**2+target_vec[1]**2)
    if target_vec_mag!=0:
        target_vec=[target_vec[0]/target_vec_mag,
                    target_vec[1]/target_vec_mag]
        cos_angle=target_vec[0]*bounce_speed[0]+target_vec[1]*bounce_speed[1]
        angle=math.acos(cos_angle)/math.pi*180
        if angle<=45:
            dis_from_center=angle/45 *35
            if target_vec[1]<bounce_speed[1]:
                return cur_pos[1]+dis_from_center,angle
            else:
                return cur_pos[1]-dis_from_center,angle
    return -1, "i"