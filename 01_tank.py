#coding:utf-8
import pygame,sys,time
from pygame.locals import *
from random import randint

class TankMain():
    width = 600
    height = 500
    enemy_step = 6
    enemy_speed = 3
    enemy_num = 4
    # enemy_list = []
    enemy_group = pygame.sprite.Group()
    explode_list = []
    my_tank_missle_list = []
    enemy_missle_group = pygame.sprite.Group()
    my_tank = None
    wall = None

    def startGame(self):
        pygame.init()
        # screen object
        screen = pygame.display.set_mode((TankMain.width,TankMain.height),0,32)
        # surface object
        # surf = pygame.Surface((50,50))
        # surf.fill((255,255,255))
        # rect = surf.get_rect()
        pygame.display.set_caption('Tank Game')
        TankMain.my_tank = MyTank(screen,'p1tank')


        for i in range(1,TankMain.enemy_num):
            TankMain.enemy_group.add(EnemyTank(screen,'enemy1'))
            TankMain.enemy_group.add(EnemyTank(screen, 'enemy2'))
            TankMain.enemy_group.add(EnemyTank(screen, 'enemy3'))

        TankMain.wall = Wall(screen,200,300,200,20)

        while True:
            #color RGB(0,0,0)black,(255,255,255)white
            screen.fill((0,0,0))

            for i,text in enumerate(self.write_text(),0):
                screen.blit(text,(0,5+i*15))


            for m in TankMain.my_tank_missle_list:
                if m.live:
                    m.display()
                    m.hit_tank()
                    m.move()
                else:
                    TankMain.my_tank_missle_list.remove(m)

            for m in TankMain.enemy_missle_group:
                if m.live:
                    m.display()
                    # m.hit_tank()
                    m.move()
                else:
                    TankMain.enemy_missle_group.remove(m)

            self.getEvent(TankMain.my_tank,screen)
            # screen.blit(surf,((600-50)//2,(500-50)//2))

            if TankMain.my_tank:
                TankMain.my_tank.hit_enemy_missile()
            if TankMain.my_tank and TankMain.my_tank.live:
                TankMain.my_tank.display()
                TankMain.my_tank.move()
            else:
                pass
                # del(my_tank)
                TankMain.my_tank=None


            TankMain.wall.display()
            TankMain.wall.hit_other()

            for enemy in TankMain.enemy_group:
                enemy.display()
                enemy.enemy_move()
                enemy.enemy_fire()

            for explode in TankMain.explode_list:
                explode.display()
                # explode.step

            time.sleep(0.05)
            #pygame.display.flip()
            pygame.display.update()
    def getEvent(self,my_tank,screen):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.stopGame()
                if event.key == K_n:
                    if not TankMain.my_tank:
                        TankMain.my_tank = MyTank(screen, 'p2tank')
                if my_tank:
                    if event.key == K_UP:
                        my_tank.direction = 'U'
                        # my_tank.move()
                        my_tank.stop = False
                    elif event.key == K_DOWN:
                        my_tank.direction = 'D'
                        # my_tank.move()
                        my_tank.stop = False
                    elif event.key == K_LEFT:
                        my_tank.direction = 'L'
                        # my_tank.move()
                        my_tank.stop = False
                    elif event.key == K_RIGHT:
                        my_tank.direction = 'R'
                        # my_tank.move()
                        my_tank.stop = False
                    elif event.key == K_SPACE:
                        m = my_tank.fire()
                        m.good = True #mytank's missle
                        TankMain.my_tank_missle_list.append(m)
            if event.type == KEYUP:
                if my_tank:
                    if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                         my_tank.stop = True

    def stopGame(self):
        pygame.quit()
        sys.exit()

    def write_text(self):
        myfont = pygame.font.SysFont("simsunnsimsun",12)
        text_sf1 = myfont.render("敌方坦克数量 : %d"%len(TankMain.enemy_group),True,(255,0,0))
        text_sf2 = myfont.render("我方炮弹数量 : %d"%len(TankMain.my_tank_missle_list),True,(255,0,0))
        return text_sf1,text_sf2

class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen =screen
    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)

class Tank(BaseItem):
    #define class attribute, all tank's width & heigh is same
    width=60
    height=60
    def __init__(self,screen,left,top,name):
        super().__init__(screen)
        self.direction='D'
        self.speed = 5
        self.images={}
        self.images['L']=pygame.image.load('img/p1tankL.gif')#ctrl +d or +y
        self.images['R']=pygame.image.load('img/p1tankR.gif')
        self.images['U']=pygame.image.load('img/p1tankU.gif')
        self.images['D']=pygame.image.load('img/p1tankD.gif')
        self.image = self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True
        self.stop=True
        self.load_images(name)
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

    def hit_enemy_missile(self):
        hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_missle_group,False)
        for m in hit_list:
            m.live = False
            TankMain.enemy_missle_group.remove(m)
            self.live=False
            explode = Explode(self.screen,self.rect)
            TankMain.explode_list.append(explode)

    def load_images(self,name):
        self.images['L']=pygame.image.load('img/'+name+'L.gif')#ctrl +d or +y
        self.images['R']=pygame.image.load('img/'+name+'R.gif')
        self.images['U']=pygame.image.load('img/'+name+'U.gif')
        self.images['D']=pygame.image.load('img/'+name+'D.gif')

    def stay(self):
        self.rect.top = self.oldtop
        self.rect.left= self.rect.left

    def move(self):
        if not self.stop:
            self.oldleft = self.rect.left
            self.oldtop = self.rect.top

            if self.direction == 'L':
                 if self.rect.left >0 :
                     self.rect.left -= self.speed
                 else:
                     self.rect.left = 0
            elif self.direction == 'R':
                 if self.rect.right < TankMain.width :
                     self.rect.right += self.speed
                 else:
                     self.rect.right = TankMain.width
            elif self.direction == 'U':
                 if self.rect.top > 0 :
                     self.rect.top -= self.speed
                 else:
                     self.rect.top = 0
            elif self.direction == 'D':
                 if self.rect.bottom < TankMain.height :
                     self.rect.bottom += self.speed
                 else:
                     self.rect.bottom = TankMain.height

    def fire(self):
        m = Missle(self.screen,self)
        return m


class MyTank(Tank):
    def __init__(self,screen,name):
        super().__init__(screen,275,400,name)



class EnemyTank(Tank):
    def __init__(self,screen,name):
        super().__init__(screen,randint(1,5)*100,100,name)
        self.step = TankMain.enemy_step
        self.speed = TankMain.enemy_speed
        # self.images['L']=pygame.image.load('img/enemy1L.gif')#ctrl +d or +y
        # self.images['R']=pygame.image.load('img/enemy1R.gif')
        # self.images['U']=pygame.image.load('img/enemy1U.gif')
        # self.images['D']=pygame.image.load('img/enemy1D.gif')

    def get_random_direction(self):
        r = randint(0,4)
        if r == 0:
            self.stop = True
        elif r == 1:
            self.direction = 'U'
            self.stop = False
        elif r == 2:
            self.direction = 'D'
            self.stop = False
        elif r == 3:
            self.direction = 'L'
            self.stop = False
        elif r == 4:
            self.direction = 'R'
            self.stop = False

    def enemy_fire(self):
        r = randint(0,50)
        if r>45:
            m=self.fire()
            TankMain.enemy_missle_group.add(m)

    def enemy_move(self):
        # print(self.step)
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = TankMain.enemy_step
            else:
                self.move()
                self.step -=1


class Missle(BaseItem):
    width =17
    heigh = 17
    def __init__(self,screen,tank):
        super().__init__(screen)
        self.tank = tank
        self.direction= tank.direction
        self.speed = 12
        self.images={}
        self.images['L']=pygame.image.load('img/tankmissile.gif')#ctrl +d or +y
        self.images['R']=pygame.image.load('img/tankmissile.gif')
        self.images['U']=pygame.image.load('img/tankmissile.gif')
        self.images['D']=pygame.image.load('img/tankmissile.gif')
        # self.images['L']=pygame.image.load('img/enemymissile.gif')#ctrl +d or +y
        # self.images['R']=pygame.image.load('img/enemymissile.gif')
        # self.images['U']=pygame.image.load('img/enemymissile.gif')
        # self.images['D']=pygame.image.load('img/enemymissile.gif')
        self.image = self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=tank.rect.left +(tank.width - self.width)//2 #get int value (//2)
        self.rect.top=tank.rect.top + (tank.height - self.heigh)//2
        self.live=True
        self.good=True
        # self.load_images(name)

    def move(self):
        if self.live:
             if self.direction == 'L':
                 if self.rect.left >0 :
                     self.rect.left -= self.speed
                 else:
                     self.live = False
             elif self.direction == 'R':
                 if self.rect.right < TankMain.width :
                     self.rect.right += self.speed
                 else:
                     self.live = False
             elif self.direction == 'U':
                 if self.rect.top > 0 :
                     self.rect.top -= self.speed
                 else:
                     self.live = False
             elif self.direction == 'D':
                 if self.rect.bottom < TankMain.height :
                     self.rect.bottom += self.speed
                 else:
                     self.live = False

    #mytank's missle,enemytank's missle
    def hit_tank(self):
        if self.good:
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_group,False) #may be hit much tank
            for e in hit_list:
                e.live=False
                TankMain.enemy_group.remove(e)
                self.live=False
                explode = Explode(self.screen,e.rect)
                TankMain.explode_list.append(explode)

class Explode(BaseItem):

    def __init__(self,screen,rect):
        super().__init__(screen)
        self.live=True
        self.images=[]
        for i in range(1,9):
            self.images.append(pygame.image.load('img/blast'+str(i)+'.gif'))
        self.step=0
        self.rect=rect #site is tank's site

    def display(self):
        if self.live:
            if self.step == len(self.images): #display the last picture
                self.live = False
            else:
                self.image=self.images[self.step]
                self.screen.blit(self.image,self.rect)
                self.step +=1
        else:
            return

class Wall(BaseItem):
    def __init__(self,screen,left,top,width,height):
        super().__init__(screen)
        self.color = (255,0,0)
        self.rect = Rect(left,top,width,height)

    def display(self):
        self.screen.fill(self.color,self.rect)

    def hit_other(self):
        if TankMain.my_tank:
            is_hit = pygame.sprite.collide_rect(self,TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()
        if TankMain.enemy_group:
            hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_group,False) #may be hit much tank
            for e in hit_list:
                e.stop = True
                e.stay()
        if TankMain.enemy_missle_group:
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_missle_group, False)
            for em in hit_list:
                em.live = False

game = TankMain()
game.startGame()
