from tkinter import *
from gameObjects import Bird,Pipe
from neural import first_generation,calcul,new_generation
from Settings import JUMP_RANGE,JUMP_RECOVERY,SPEED


class MainInterface:
    def __init__(self):
        self.width=1000
        self.height=500
        self.win=Tk()
        self.win.geometry("{0}x{1}+500+300".format(self.width,self.height))
        self.berds=[Bird(i,self.width/2, self.height/2) for i in range(10)]
        self.game_field=Canvas(self.win,bg="light blue",height=self.height,width=self.width)
        self.game_field.pack(side=BOTTOM)
        #self.win.bind("<space>",self.jump)
        self.first=True
        self.three_pipes = [Pipe(90, 150, 1, self.berds[0].x + self.width / 2), Pipe(90, 150, 1, 1500),Pipe(90, 150, 1, 2000)]
        self.generatiom=0
        self.text_gener = self.game_field.create_text(self.width/2, 300, fill="white", font="Fixedsys 20",text="Generation:" + str(self.generatiom))
        self.speed=SPEED #2
        self.jum_recovery=JUMP_RECOVERY#10 12
        self.draw()
        self.run()

    #MASS
    def upd_text_score(self):
        self.game_field.delete(self.text_gener)
        self.text_gener = self.game_field.create_text(self.width/2, 100, fill="white", font="Fixedsys 20",text="Generation:" + str(self.generatiom))

    def mass_upd_gravity(self):
        for i in self.berds:
            i.upd_gravity(i.f)
            i.doing_way+=1

    def mass_win(self):
        for i in self.berds:
            if i.chek_win(self.three_pipes[i.current_pipe]) and i.chek_die(self.height,self.three_pipes[i.current_pipe]):
                i.score+=1
                i.current_pipe+=1
                if i.current_pipe==3:
                    i.current_pipe=0

    def restart(self):
        self.generatiom+=1
        for i in self.berds:
            print(i.num, "dist:", i.dis, "score:", i.score, "fitness:", i.fit)
            i.f = i.allf
            i.y=self.height/2
            i.y1 = i.y + 20
        self.berds = new_generation(self.berds)
        self.three_pipes = [Pipe(90, 150, 1, self.berds[0].x + self.width / 2), Pipe(90, 150, 1, 1500),
                            Pipe(90, 150, 1, 2000)]
        for i in self.berds:
            i.dis=0
            i.fit=0
            i.doing_way = 0
            i.score=0
            i.current_pipe=0
            i.live=True
        self.update()


    def mass_die(self):
        sombody_alive=False
        for i in self.berds:
            if i.chek_die(self.height,self.three_pipes[i.current_pipe]) and i.live:
                sombody_alive=True
                i.dis+=1
                i.fit=i.fitness(self.three_pipes[i.current_pipe])
            else:
                i.f=0
                i.live=False
        if sombody_alive:
            self.win.after(self.speed, self.run)
        else:
            self.restart()
            self.update()
            self.run()

    def mass_cal(self):
        for i in self.berds:
            if calcul(i.distans(self.three_pipes[i.current_pipe]), i.height(self.three_pipes[i.current_pipe]),i.w01,i.w02,i.distans(self.three_pipes[i.current_pipe]))and i.live:
                if i.recharh >= self.jum_recovery:
                    i.jump(JUMP_RANGE)#-20
                    i.recharh=0
                else:
                    i.recharh+=1

    def run(self):
        if self.first:
            for i in self.berds:
                i.w01,i.w02=first_generation(i.distans(self.three_pipes[i.current_pipe]), i.height(self.three_pipes[i.current_pipe]),i.distans(self.three_pipes[i.current_pipe]))
            self.first=False
        self.mass_cal()
        self.update()
        self.upd_text_score()
        self.mass_upd_gravity()
        self.mass_win()
        self.list_pipe_cheak_exist()
        for i in  self.three_pipes:
            i.upd_pipe()
        self.mass_die()

    def list_pipe_cheak_exist(self):
        for i in range(len(self.three_pipes)):
            if not self.three_pipes[i].pipe_existing():
                if i == 0: self.three_pipes[i] = Pipe(90, 150, 1, self.three_pipes[2].x2+500)
                if i == 1: self.three_pipes[i] = Pipe(90, 150, 1, self.three_pipes[0].x2+500)
                if i == 2: self.three_pipes[i] = Pipe(90, 150, 1, self.three_pipes[1].x2+500)

    #def jump(self,event):
        #self.berds[0].jump(-50)

    def update(self):
        self.clean()
        self.draw()

    def pipe_body_add(self):
        out=[{"Top:":None,"Bottom:":None} for i in range(len(self.three_pipes))]
        for i in range(len(self.three_pipes)):
            out[i]["Top:"]=self.game_field.create_rectangle(self.three_pipes[i].x,0,self.three_pipes[i].x2,self.three_pipes[i].y_way_start,fill="green")
            out[i]["Bottom:"]=self.game_field.create_rectangle(self.three_pipes[i].x,self.three_pipes[i].y_way_end,self.three_pipes[i].x2,self.height,fill="green")
        return out

    def mass_draw_berds(self):
        out=[None for i in range(len(self.berds))]
        for i in self.berds:
            if i.live:
                out[self.berds.index(i)]=self.game_field.create_oval(i.x,i.y,i.x1,i.y1,outline="red",fill="yellow")
        return out

    def draw(self):
        #self.angle_calculate()
        self.game_field.config()
        #self.player_body=self.game_field.create_oval(self.player.x,self.player.y,self.player.x1,self.player.y1,outline="red",fill="yellow")
        self.berds_bodyes=self.mass_draw_berds()
        #self.player_body_visual=self.game_field.create_oval(self.player.x,self.player.y,self.player.x+30,self.player.y+20,fill="yellow",angle=self.visual_angle_n)
        self.pipe_body_list=self.pipe_body_add()

    def clean(self):
        for i in self.berds_bodyes:
            self.game_field.delete(i)
        for i in self.pipe_body_list:
            self.game_field.delete(i["Top:"])
            self.game_field.delete(i["Bottom:"])
