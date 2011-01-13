import math
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

class Square():

    mass = 10.0

    def __init__(self, node):
        self.node = node
        self.clear()

    def fill(self):
        self.filled = True
        self.node.setColor(0.5, 0.5, 0.5)

    def clear(self):
        self.filled = False
        self.force = 0.0
        self.node.setColor(0.1, 0.1, 0.1)

    def update_color(self):
        pass



class Joint():

    force = 0

    def __init__(self, node):
        self.node = node
        


class World(DirectObject):

    size = 10

    cursor_x = 0
    cursor_y = 0

    def __init__(self):

        self.template = loader.loadModel('plane')

        self.background = aspect2d.attachNewNode('background')
        self.background.setColor(0, 0, 0) 
        self.background.setScale(2)                 
        self.template.instanceTo(self.background)      
  
        self.canvas = aspect2d.attachNewNode('canvas')
        self.canvas.setScale(2.0 / self.size)  
        correction = 1.0 / self.size - 1
        self.canvas.setPos(correction, 0, correction)

        self.squares = []
        self.joints = []
        
        for x in range(self.size):
            self.squares.append([])
            for y in range(self.size):
                square_node = self.canvas.attachNewNode('square')
                square_node.setPos(x, 0, y)
                square_node.setColor(0.1, 0.1, 0.1) 
                square_node.setScale(0.8)           
                self.template.instanceTo(square_node)
                self.squares[x].append(Square(square_node))
                
                joint_node = self.canvas.attachNewNode('joint')
                joint_node.setPos(x, 0, y - 0.5)
                joint_node.setColor(0.05, 0.05, 0.05) 
                joint_node.setScale(0.6, 1, 0.2)
                self.template.instanceTo(joint_node)
                self.joints.append(Joint(square_node))

                if x > 0:
                    joint_node = self.canvas.attachNewNode('joint')
                    joint_node.setPos(x - 0.5, 0, y)
                    joint_node.setColor(0.05, 0.05, 0.05) 
                    joint_node.setScale(0.2, 1, 0.6)
                    self.template.instanceTo(joint_node)
                    self.joints.append(Joint(square_node))

        self.cursor = self.canvas.attachNewNode('cursor')
        self.cursor.setColor(0.5, 0, 0)
        self.cursor.setRenderModeWireframe()
        self.template.instanceTo(self.cursor)

        self.accept('arrow_left', self.cursor_left)
        self.accept('arrow_right', self.cursor_right)
        self.accept('arrow_up', self.cursor_up)
        self.accept('arrow_down', self.cursor_down)
        self.accept('space', self.fill)
        self.accept('delete', self.clear)

        taskMgr.add(self.calculate, 'calculate')

    def calculate(self, task):
        
        for x in range(self.size):
            for y in range(self.size):
                if self.squares[x][y].filled:
                                        
                    self.squares[x][y].update_color()
                        
        return task.cont
        
        
    def update_cursor(self):
        self.cursor_x %= self.size
        self.cursor_y %= self.size
        self.cursor.setPos(self.cursor_x, 0, self.cursor_y)

    def cursor_left(self):
        self.cursor_x -= 1
        self.update_cursor()
    def cursor_right(self):
        self.cursor_x += 1
        self.update_cursor()
    def cursor_up(self):
        self.cursor_y += 1
        self.update_cursor()
    def cursor_down(self):
        self.cursor_y -= 1
        self.update_cursor()

    def fill(self):
        self.squares[self.cursor_x][self.cursor_y].fill()

    def clear(self):
        self.squares[self.cursor_x][self.cursor_y].clear()

w = World()
run()
