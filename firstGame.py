import pygame
import math
import random
from pygame.locals import *
pygame.init()
w,h=640,480
screen =pygame.display.set_mode ((w,h))

#LOAD IMAGES

pygame.display.set_caption('Ha game')
grass=pygame.image.load('resources/images/grass.png')
castle=pygame.image.load('resources/images/castle.png')
player=pygame.image.load('resources/images/dude2.png')
bad=pygame.image.load('resources/images/badguy.png')
bullet=pygame.image.load('resources/images/bullet.png')
health=pygame.image.load('resources/images/health.png')
health_bar=pygame.image.load('resources/images/healthbar.png')
game_over = pygame.image.load("resources/images/gameover.png")
you_win = pygame.image.load("resources/images/youwin.png")
#VARIABLE DECLARATION

#level=1
castle_w=castle.get_width()
level_prob=0.1# can be changed
player_w=player.get_width()
player_h=player.get_height()
bad_w=bad.get_width()
bad_h=bad.get_height()
angle=0
bad_list=[]
player_pos=[100,100]
arrow_list=[]
bad_timer=0
health_value=195#can be changed
#bad guy or no:
def is_bad():
        number=random.randint(1,10)
        if number<=2:
                return True
        else: return False

#generate badguy
def generate_bad(h,bad_h,w,bad_w):
        bad_y=random.randint(0,h-bad_h)
        return [w-bad_w,bad_y]
#checking the coordinates of the arrow

def  in_screen(x,y):
        result=True
        if x<0 or x>w:
                result=False
        if y<0 or y>h:
                result=False
        return result

#init pygame.font
pygame.font.init()
#check 

while True:
        clock=pygame.time.Clock()
        clock.tick(30)
        #print the normal setting
        for y in range(h/grass.get_height()+1):
                for x in range (w/grass.get_width() +1):
                        screen.blit(grass,(x*grass.get_width(),y*grass.get_height()))
        for y in range(h/castle.get_height()):
                screen.blit(castle, (0,20+y*castle.get_height()))
        #print the player
        mouse_pos=pygame.mouse.get_pos()
        angle=360-math.degrees(math.atan2(mouse_pos[1]-player_pos[1]-player_h,mouse_pos[0]-player_pos[0]-player_w))
        rotated_player=pygame.transform.rotate(player,angle)
        rotated_player_pos=[player_pos[0]-rotated_player.get_width()/2,player_pos[1]-rotated_player.get_height()/2]
        screen.blit(rotated_player,rotated_player_pos)
        #print time
        font=pygame.font.Font(None,24)
        time=str(pygame.time.get_ticks()/60000)+':'+str(pygame.time.get_ticks()%60000/1000)
        time_rect=font.render(time,True,(0,0,0))
        screen.blit(time_rect,[550,0])
        #print health
        screen.blit(health_bar,(7,5))
        if health_value>0:
                for i in range(health_value):
                        screen.blit(health,(10+i,8))
        #print the bad guy
        bad_timer+=1
        for bad_pos in bad_list:
                screen.blit(bad,bad_pos)
        
        if bad_timer%5==0:
                for bad_pos in bad_list:
                        bad_pos[0]-=bad_w
                        if bad_pos[0]<60:
                                bad_list.remove(bad_pos)
                                health_value-=5
                        if not in_screen(bad_pos[0],bad_pos[1]):
                                bad_list.remove(bad_pos)
                if bad_timer==20:               
                        if is_bad():
                                bad_list.append(generate_bad(h,bad_h,w,bad_w))
                        bad_timer=0
        #shoot
        for arrow in arrow_list:
                rotated_arrow=pygame.transform.rotate(bullet,arrow[0])
                screen.blit(rotated_arrow,arrow[1])
                arrow_rect=pygame.Rect(arrow[1][1], arrow[1][0],rotated_arrow.get_width(), rotated_arrow.get_height())
                for bad_pos in bad_list:
                        bad_rect=pygame.Rect(bad_pos[1],bad_pos[0],bad_w, bad_h)
                        if bad_rect.colliderect(arrow_rect):
                                bad_list.remove(bad_pos)
                arrow[1][0]+=math.cos(math.radians(360-arrow[0]))*30
                arrow[1][1]+=math.sin(math.radians(360-arrow[0]))*30
                inside=in_screen(arrow[1][0],arrow[1][1])
                if not inside:
                        arrow_list.remove(arrow)
        pygame.display.flip()
        #win_lose condition
        if health_value<0:
                screen.blit(game_over,(0,0))
        if (pygame.time.get_ticks()>60000 and health_value>0):
                screen.blit(you_win,(0,0))

        #event
        for event in pygame.event.get():

                #MOVE
                if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_UP:
                                player_pos[1]-=5
                        elif event.key==pygame.K_DOWN:
                                player_pos[1]+=5
                        elif event.key==pygame.K_LEFT:
                                player_pos[0]-=5
                        elif event.key==pygame.K_RIGHT:
                                player_pos[0]+=5

                #QUIT
                if event.type==pygame.QUIT:
                        pygame.quit()
                        exit(0)

                #SHOOT
                if event.type==pygame.MOUSEBUTTONDOWN:
                        arrow_pos=[rotated_player_pos[0]+rotated_player.get_width()/2,rotated_player_pos[1]+rotated_player.get_height()/2]
                        arrow_list.append([angle,arrow_pos])
                        
                     
