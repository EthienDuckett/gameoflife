import pyglet
from pyglet.window import key
import math
import time

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(960-350, 200)
        self.frame_rate = 1/60.0
        cursor=pyglet.image.load('resources/cursor.png')
        background=pyglet.image.load('resources/background.png')
        cell=pyglet.image.load('resources/cell.png')
        self.player = pyglet.sprite.Sprite(cursor, x=500, y=200)
        self.living=0

        self.xpos=pyglet.text.Label("X position = "+str(math.floor(self.player.x)), x=400, y=10)
        self.ypos=pyglet.text.Label("Y position = "+str(math.floor(self.player.y)), x=400, y=30)
        self.livingcells=pyglet.text.Label("living: "+str(self.living), x=10, y=30)
        self.deadcells=pyglet.text.Label("dead: "+str(10000-self.living), x=10, y=10)
        self.board = [[1 for i in range(100)] for j in range(100)]
        # self.board[40][40]=0
        self.cell=cell
        self.background=background
        self.pause=True
        # self.start=True
        self.xp1=0
        self.yp1=0
        self.simulation=self.board
        self.livingsim=[[0 for i in range(100)] for j in range(100)]
        self.simulate=False
        self.fake_rate=10
        self.fps=pyglet.text.Label("steps per second: "+str(self.fake_rate), x=100, y=10)
        GameWindow.drawcells(self)

# add a way to make cell be able to teleport to the other side when the go off the screen if the user chooses that option
#
#

    def on_draw(self):
        self.clear()
        # self.player.update()
        self.living=0
        for b in range(0,100):
            for i in range(0,100):
                if self.board[b][i] == 1:
                    self.living+=1
        self.livingcells.draw()
        self.deadcells.draw()
        self.background.blit(0, 100)
        self.fps.draw()
        if self.pause == False:
            self.start=False
            self.simulation=self.board
            time.sleep(1/self.fake_rate)
            if self.pause == False:
                GameWindow.drawcells(self)

        else:
            self.xpos.draw()
            self.ypos.draw()
            self.player.x=self.player.x-self.player.x%6
            self.player.y=self.player.y-(self.player.y+2)%6
            self.player.draw()
            Cells.draw()

    def update(self, dt):
        self.xpos=pyglet.text.Label("X position = "+str(math.floor(self.player.x/6)+1), x=400, y=10)
        self.ypos=pyglet.text.Label("Y position = "+str(math.floor(self.player.y/6)-15), x=400, y=30)
        self.livingcells=pyglet.text.Label("living: "+str(self.living), x=10, y=30)
        self.deadcells=pyglet.text.Label("dead: "+str(10000-self.living), x=10, y=10)
        self.fps=pyglet.text.Label("steps per second: "+str(math.ceil(self.fake_rate)), x=150, y=10)
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.NUM_ADD:
            self.fake_rate+=1
            if self.fake_rate > 60:
                self.fake_rate-=1
            self.fps=pyglet.text.Label("steps per second: "+str(self.fake_rate), x=100, y=10)
        elif symbol == key.NUM_SUBTRACT:
            self.fake_rate-=1
            if self.fake_rate == 0:
                self.fake_rate+=1
            self.fps=pyglet.text.Label("steps per second: "+str(self.fake_rate), x=100, y=10)
        if symbol == key.SPACE:
            if self.pause == True:
                self.pause = False
            else:
                self.pause = True
        if self.pause == True:
            # if not(modifiers and key.MOD_SHIFT):
            if symbol == key.LEFT:
                self.player.x+=-6
            elif symbol == key.RIGHT:
                self.player.x+=6
            elif symbol == key.DOWN:
                self.player.y+=-6
            elif symbol == key.UP:
                self.player.y+=6
            if symbol == key.RCTRL:
                x=self.player.x-self.player.x%6
                y=self.player.y-(self.player.y+2)%6
                x=int(x/6)
                y=int((y-100)/6)
                if y < 0:
                    y=0
                elif y > 99:
                    y=99
                    if x < 0:
                        x=0
                    elif x > 99:
                        x=99
                self.xp1=x
                self.yp1=y
        if symbol == key.EQUAL:
            self.board = [[1 for i in range(100)] for j in range(100)]
            GameWindow.drawcells(self)
        elif symbol == key.MINUS:
            self.board = [[0 for i in range(100)] for j in range(100)]
            GameWindow.drawcells(self)
        if symbol == key.NUM_6:
            self.simulation=self.board
            GameWindow.gennext(self)
            GameWindow.drawcells(self)
        # elif symbol == key.LEFT & modifiers & key.MOD_SHIFT:


    def on_key_release(self, symbol, modifiers):
        if self.pause == True:

            if symbol == key.RCTRL:
                x=self.player.x-self.player.x%6
                y=self.player.y-(self.player.y+2)%6
                x=int(x/6)
                y=int(((y-100)/6))
                yl=0
                ys=0
                ymod=0
                xl=0
                xs=0
                xmod=0
                if y < 0:
                    y=0
                elif y > 99:
                    y=99
                if x < 0:
                    x=0
                elif x > 99:
                    x=99

                if self.yp1>y:
                    yl=self.yp1
                    ys=y
                elif self.yp1<y:
                    yl=y
                    ys=self.yp1

                if self.xp1>x:
                    xl=self.xp1
                    xs=x
                elif self.xp1<x:
                    xl=x
                    xs=self.xp1
                if self.yp1-y == 0:
                    ymod=y
                if self.xp1-x == 0:
                    xmod=x
                for i in range(ys, yl+1):
                    for b in range(xs, xl+1):
                        if self.board[b+xmod][i+ymod] == 1:
                            self.board[b+xmod][i+ymod] = 0
                        else:
                            self.board[b+xmod][i+ymod] = 1
                GameWindow.drawcells(self)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.x=x
        self.playerxmod=0
        self.player.y=y
    def gennext(self):
        area=0
        for b in range(0,100):
            for i in range(0,100):
                self.livingsim[b][i]=self.simulation[b][i]
        for b in range(0,100):
            for i in range(0,100):
                area=0
                if i != 0 and b != 0 and b != 99 and i != 99:
                    area=self.simulation[b][i+1]+self.simulation[b][i-1]+self.simulation[b+1][i+1]+self.simulation[b-1][i]+self.simulation[b+1][i]+self.simulation[b-1][i+1]+self.simulation[b-1][i-1]+self.simulation[b+1][i-1]
                elif i == 0 and b != 0 and b != 99:
                    area=self.simulation[b-1][0]+self.simulation[b+1][0]+self.simulation[b-1][1]+self.simulation[b][1]+self.simulation[b+1][1]
                elif i == 99 and b != 0 and b != 99:
                    area=self.simulation[b-1][99]+self.simulation[b+1][99]+self.simulation[b-1][98]+self.simulation[b][98]+self.simulation[b+1][98]
                elif b == 0 and i != 0 and i != 99:
                    area=self.simulation[0][i+1]+self.simulation[0][i-1]+self.simulation[1][i+1]+self.simulation[1][i-1]+self.simulation[1][i]
                elif b == 99 and i != 0 and i != 99:
                    area=self.simulation[99][i+1]+self.simulation[99][i-1]+self.simulation[98][i+1]+self.simulation[98][i-1]+self.simulation[98][i]
                elif b == 0 and i == 0:
                    area=self.simulation[0][1]+self.simulation[1][0]+self.simulation[1][1]
                elif b == 99 and i == 99:
                    area=self.simulation[99][98]+self.simulation[98][98]+self.simulation[98][99]
                elif b == 0 and i == 99:
                    area=self.simulation[0][98]+self.simulation[1][98]+self.simulation[1][99]
                elif b == 99 and i == 0:
                    area=self.simulation[99][1]+self.simulation[98][1]+self.simulation[98][10]

                if area == 3 and self.simulation[b][i] == 0:
                    self.livingsim[b][i]=1
                elif area > 3:
                    self.livingsim[b][i] = 0
                elif area < 2:
                    self.livingsim[b][i] = 0

        for b in range(0,100):
            for i in range(0,100):
                self.simulation[b][i]=self.livingsim[b][i]
                self.livingsim[b][i]=self.simulation[b][i]


    def drawcells(self):
        if self.pause == False:
            GameWindow.gennext(self)
        global Cells
        Cells=pyglet.graphics.Batch()
        global Cell
        Cell=[]
        if self.simulate == True:
            self.simulation=self.board
            for b in range(0,100):
                for i in range(0,100):
                    if self.simulation[b][i] == 1:
                        Cell.append(pyglet.sprite.Sprite(self.cell, x=b*6+1, y=(i*6+1)+100, batch=Cells))
        else:
            for b in range(0,100):
                for i in range(0,100):
                    if self.board[b][i] == 1:
                        Cell.append(pyglet.sprite.Sprite(self.cell, x=b*6+1, y=(i*6+1)+100, batch=Cells))
                # else:
                #     print("b: "+str(b)+' i: '+str(i))
                    # b*6+1,(i*6+1)+100
        Cells.draw()
if __name__ == "__main__":
    window = GameWindow(601, 701, "Conway's game of life", resizable=False)
    # I am following a tutorial but this makes some sense which is good
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
