import math,random
# ARCAEA 5.0
arcaea = []

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    pong_ai.team_name = "Aitsuki Nakuru x Deja vu feat. Ishar-mla"
    global arcaea
    laur = paddle_frect.pos[1] + 27.5
    m1shamo = other_paddle_frect.pos[0] + 5
    
    silent_answer(ball_frect)
    if len(arcaea) != 2:
        return "up"
    pentiment = black_fate(arcaea)

    oblivia= 400
    if pentiment[0]<0:
        oblivia = 25
    if pentiment[0] == 0:
        enchanted_love = 1000000
    else:
        enchanted_love = (oblivia - ball_frect.pos[0])/pentiment[0]

    if (paddle_frect.pos[0]==15 and pentiment[0]>=0)or(paddle_frect.pos[0]==415 and pentiment[0]<=0):
        if paddle_frect.pos[1] < 105:
            return "down"
        else:
            return "up"

    fairytale,inkar_usi, arcahv = esoteric_order(pentiment,ball_frect,paddle_frect,table_size)
    taritsu = inkar_usi
    tempestissimo = fairytale,inkar_usi
    hikari = [-arcahv[0], arcahv[1]]
    if luminous_sky(arcahv)!=0:
        hikari=vicious_labyrinth(hikari)

        testify=False
        for i in range(5):

            if i%2==0:
                overwhelm=[m1shamo,-i*(280)]
                seclusion=[m1shamo,265+i*(280)]
            else:
                overwhelm=[m1shamo,265+i*(280)]
                seclusion=[m1shamo,-i*(280)]

            blue_comet, at=final_verdict(overwhelm,tempestissimo,hikari)
            auxesia, ab=final_verdict(seclusion,tempestissimo,hikari)

            tt,tb = 10000000, 10000000

            if at!="i":
                last_moment,last_eternity = arcahv
                vt = last_eternity*math.sin(2*at)-last_moment*math.cos(2*at)
                tt = 390/abs(vt) + enchanted_love
            if ab!="i":
                last_moment,last_eternity = arcahv
                vb = last_eternity*math.sin(2*ab)-last_moment*math.cos(2*ab)
                tb = 390/abs(vb) + enchanted_love

            # y -- ysin2-xcos2, xsin2+ycos2
                        
            ot = other_paddle_frect.pos[1]
            ob = 210 - other_paddle_frect.pos[1]

            if ob<=tb and ot<=tt:
                defection='alterale'
            elif ob>tb:
                defection='seclusion'
            else:
                defection='overwhelm'

            if blue_comet>=27.5 and blue_comet<=237.5 and auxesia>=27.5 and auxesia<=237.5:
                if defection=='alterale':
                    if abs(blue_comet-laur)<abs(auxesia-laur):
                        taritsu=blue_comet
                    else:
                        taritsu=auxesia
                elif defection=='seclusion':
                    taritsu=blue_comet
                else:
                    taritsu=auxesia
                testify=True
            elif blue_comet>=27.5 and blue_comet<=237.5:
                taritsu=blue_comet
                testify=True
            elif auxesia>=27.5 and auxesia<=237.5:
                taritsu=auxesia
                testify=True

            if testify:
                break
            
        if not testify:
            if taritsu>132.5:
                taritsu-=35
            else:
                taritsu+=35
                

    if laur < taritsu:
        return "down"
    else:
        return "up"

def silent_answer(ball_frect):
    global arcaea
    if len(arcaea) == 2:
        arcaea[0] = arcaea[1]
        arcaea[1] = ball_frect.pos
    else:
        arcaea.append(ball_frect.pos)

def black_fate(l):
    return [l[1][0]-l[0][0], l[1][1]-l[0][1]]

def luminous_sky(L):
    re = 0
    for i in L:
        re += i**2
    return math.sqrt(re)

def vicious_labyrinth(L):
    pure_memory = luminous_sky(L)
    for i in range(len(L)):
        L[i] = L[i] / pure_memory
    return L
    
def esoteric_order(speed,ball_frect,paddle_frect,table_size):
        vx, vy = speed
        re_xpos,re_ypos,re_vx,re_vy = 420,0,vx,vy
        if vx == 0:
            return re_xpos,re_ypos,speed
        elif vx>0:
            re_xpos = 420
        elif vx<0:
            re_xpos = 20
        inifinite_strife = abs(paddle_frect.pos[0] + paddle_frect.size[0]/2 - ball_frect.pos[0] - ball_frect.size[0]/2)-paddle_frect.size[0]/2-ball_frect.size[0]/2
        red_and_blue_and_green = abs(inifinite_strife/vx)
        vexaria = ball_frect.pos[1] + vy*red_and_blue_and_green
        if vexaria>=0 and vexaria<= table_size[1]-ball_frect.size[1]:
            re_ypos = vexaria
        else:
            if vexaria > table_size[1]-ball_frect.size[1]:
                vexaria -= (table_size[1]-ball_frect.size[1])
            sheriruth = abs(vexaria)//abs(table_size[1]-ball_frect.size[1])
            cry_of_viyella= abs(vexaria)%abs(table_size[1]-ball_frect.size[1])
            solitary_dream =sheriruth%2
            if vy>=0:
                re_ypos = cry_of_viyella
            else:
                re_ypos = (table_size[1]-ball_frect.size[1]) - cry_of_viyella
            if solitary_dream == 0:
                re_vy = -vy
                re_ypos = (table_size[1]-ball_frect.size[1]) -re_ypos
        return re_xpos,re_ypos,[re_vx,re_vy]

def final_verdict(kou,small_cloud_sugar_candy,hikari):
    saya=[kou[0]-small_cloud_sugar_candy[0],kou[1]-small_cloud_sugar_candy[1]]
    saya_mag=math.sqrt(saya[0]**2+saya[1]**2)
    if saya_mag!=0:
        saya=[saya[0]/saya_mag,
                    saya[1]/saya_mag]
        loschen_glory_road=saya[0]*hikari[0]+saya[1]*hikari[1]
        glory_road=math.acos(loschen_glory_road)/math.pi*180
        if glory_road<=45:
            paper_witch=glory_road/45 *35
            if saya[1]<hikari[1]:
                return small_cloud_sugar_candy[1]+paper_witch,glory_road
            else:
                return small_cloud_sugar_candy[1]-paper_witch,glory_road
    return -1, "i"