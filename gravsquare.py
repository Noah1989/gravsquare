import math
import random
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

class Square():

    gravity = -1.0

    joint_left = None
    joint_right = None
    joint_up = None
    joint_down = None

    def __init__(self, node):
        self.node = node
        self.clear()

    def fill(self):
        self.filled = True
        self.node.setColor(0.5, 0.5, 0.5)
        if self.joint_left is not None:
            self.joint_left.connected_right_or_down = True
        if self.joint_up is not None:
            self.joint_up.connected_right_or_down = True
        if self.joint_right is not None:
            self.joint_right.connected_left_or_up = True
        if self.joint_down is not None:
            self.joint_down.connected_left_or_up = True
        

    def clear(self):
        self.filled = False
        self.force = 0.0
        
        if self.joint_left is not None:
            self.joint_left.force = 0.0
            self.joint_left.connected_right_or_down = False
            
        if self.joint_right is not None:
            self.joint_right.force = 0.0
            self.joint_right.connected_left_or_up = False
            
        if self.joint_up is not None:
            self.joint_up.force = 0.0
            self.joint_up.connected_right_or_down = False
            
        if self.joint_down is not None: 
            self.joint_down.force = 0.0
            self.joint_down.connected_left_or_up = False
            
        self.node.setColor(0.1, 0.1, 0.1)
        

    def calculate(self):
        self.force = self.gravity

                
        if self.joint_left is not None:
            self.force -= self.joint_left.force
            
        if self.joint_right is not None:
            self.force += self.joint_right.force
            
        if self.joint_up is not None:
           self.force -= self.joint_up.force
            
        if self.joint_down is not None:
           self.force += self.joint_down.force
                     
                     
        forcable_joints = self.get_forcable_joints()
        if len(forcable_joints) > 0:
            distributed_force = self.force * min (1.9 / len(forcable_joints), 1)
            #for item in forcable_joints:
            #    distributed_force += item[0].force * item[1] * 0.001
            #    item[0].force *= 0.999
            for item in forcable_joints:
                item[0].force -= distributed_force * item[1]
                

        


    def get_forcable_joints(self):
        result = []
        if self.joint_down is not None and self.joint_down.get_is_connected():
            result.append((self.joint_down, 1))
        if self.joint_right is not None and self.joint_right.get_is_connected():
            result.append((self.joint_right, 1))
        if self.joint_up is not None and self.joint_up.get_is_connected():
            result.append((self.joint_up, -1))
        if self.joint_left is not None and self.joint_left.get_is_connected():
            result.append((self.joint_left, -1))            
        return result
    

    def update_color(self):
        self.node.setColor(0.1 * -self.force +0.5, 0.1 * self.force +0.5, 0.5)



class Joint():

    force = 0.0

    is_ground = False
    is_horizontal = False

    connected_left_or_up = False
    connected_right_or_down = False

    def get_is_connected(self):
        return self.is_ground or (self.connected_left_or_up and self.connected_right_or_down)
    
    def __init__(self, node):
        self.node = node

    def update_color(self):
        if not self.get_is_connected():
            self.node.setColor(0.05, 0.05, 0.05)
        else:
            if self.is_horizontal:
                self.node.setColor(0.02 * -self.force +0.2, 0.2, 0.02 * self.force +0.2)
            else:
                self.node.setColor(0.02 * -self.force +0.2, 0.02 * self.force +0.2, 0.2)
        


class World(DirectObject):

    size = 30

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
                square_node.setScale(0.5)           
                self.template.instanceTo(square_node)
                self.squares[x].append(Square(square_node))
                
                joint_node = self.canvas.attachNewNode('joint')
                joint_node.setPos(x, 0, y - 0.5)
                joint_node.setColor(0.05, 0.05, 0.05) 
                joint_node.setScale(0.5, 1, 0.5)
                self.template.instanceTo(joint_node)
                self.joints.append(Joint(joint_node))

                self.squares[x][y].joint_down = self.joints[-1]

                if y > 0:
                    self.squares[x][y-1].joint_up = self.joints[-1]
                else:
                    self.joints[-1].is_ground = True
              
                if x > 0:
                    joint_node = self.canvas.attachNewNode('joint')
                    joint_node.setPos(x - 0.5, 0, y)
                    joint_node.setColor(0.05, 0.05, 0.05) 
                    joint_node.setScale(0.5, 1, 0.5)
                    self.template.instanceTo(joint_node)
                    self.joints.append(Joint(joint_node))
                    self.joints[-1].is_horizontal = True
                  
                    self.squares[x][y].joint_left = self.joints[-1]
                    self.squares[x-1][y].joint_right = self.joints[-1]                

        for x in range(self.size):
            for y in range(self.size):
                if y < self.size / 2:
                    self.squares[x][y].fill()

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
        self.accept('r', self.reset)
        self.accept('d', self.distribute)

        taskMgr.add(self.calculate, 'calculate')


    def calculate(self, task):

        for x in range(self.size):
            for y in range(self.size):
                if self.squares[x][y].filled:
                    self.squares[x][y].calculate()            
                    self.squares[x][y].update_color()

        for joint in self.joints:
            joint.update_color()            
        
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

    def reset(self):
        for joint in self.joints:
            joint.force = 0

    def distribute(self):
        for joint in self.joints:
            joint.force *= 0.9

w = World()
run()
