from random import randint
from Settings import GRAVITATION

class Bird:
    def __init__(self,num, x, y):
        self.num=num
        self.x = x
        self.y = y
        self.dis=0
        self.x1=x+30
        self.y1=y+20
        self.current_pipe=0
        self.recharh=3
        self.score=0
        self.doing_way=0
        self.allf = GRAVITATION#1.8
        self.f=self.allf
        self.live=True
        self.mi=(self.y1-self.y1)/2
        self.fit=0

    def fitness(self,pipe):
        return self.doing_way-self.distans(pipe)

    def distans(self,pipe):
        return pipe.x2-self.x

    def height(self,pipe):
        return pipe.mid-self.y

    def chek_die(self,height,pipe,cheat=False):
        if not cheat:
            if self.y1 <= height  and self.y>=0:
                if self.x1<pipe.x or self.x>pipe.x2 or self.y >= pipe.y_way_start and self.y1 <= pipe.y_way_end:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def chek_win(self,pipe):
        if self.x>pipe.x2:
            return True
        else:
            False


    def upd_gravity(self,f):
        self.y+=f
        self.y1=self.y+20

    def jump(self,le):
        self.y+=le
        self.y1 = self.y + 20

class Pipe:
    def __init__(self,w,h,s,x,end=0):
        self.width=w
        self.speed=s
        self.x=x
        self.h=h
        self.x2=x+self.width
        self.y_way_start=randint(80,320)
        self.y_way_end=self.y_way_start+h
        self.end=end
        self.mid=self.midc()

    def upd_pipe(self):
        self.x-=self.speed
        self.x2=self.x+self.width

    def midc(self):
        return self.y_way_start+self.h/2

    def pipe_existing(self):
        if self.x>self.end-60:
            return True
        else:
            return False
