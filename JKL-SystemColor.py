import turtle
import random

'''This class creates the object that is stored in the stack.
Saves the position, heading, and width of the turtle'''
class CurrentState:
    def __init__(self,position,orientation,width):
        self.position = position
        self.orientation = orientation
        self.width = width

    def getPosition(self):
        return self.position

    def getHeading(self):
        return self.orientation

    def getWidth(self):
        return self.width

class LSystem:
    def __init__(self,n,d,startX, startY, angle, treeColor, initiator, generator):
        self.startX = startX
        self.startY = startY
        self.angle = angle
        self.treeColor = treeColor #sets the leaf color scheme. If string not an available color scheme, does not draw leaves
        self.step=d #the starting length for the turtle to move forward
        self.startN = n #number of recursive calls
        self.keyList = list(generator.keys())
        self.instructions = self.dolSystem(initiator,n,generator)
        self.draw()
    
    '''Returns a string of drawing instructions.
    The initiator is our starting instructions.
    The generator describes the rules to generate the drawing instructions.
    The rules are a dictionary. The key describes what to replace and and the value is what the key is being replaced with.'''
    def dolSystem(self,string, n, rules):
        if n==0: 
            return string
        else:
            newString = "" #returned string
            for i in range (len(string)): #go through every character in our starting string
                if string[i] in self.keyList: #if the character is in the keyList, it is going to replaced
                    generator = rules[string[i]]
                    if isinstance(generator,list): #if the generator is in the form of a list then choose randomly one of the rules listed
                        num = random.randint(0,len(generator)-1)  
                        replacement = generator[num]
                        for j in range (len(replacement)): #go through every character of the replacement.
                            if replacement[j]=="F": #if character is an F, call and insert insertParameters. Otherwise, insert original symbol
                                newString += self.insertParameters(n)
                            else:
                                newString += replacement[j]
                    else: #if not a list, go through every character of generator.
                        for j in range (len(generator)):
                            if generator[j]=="F": #if character is an F, call and insert insertParameters. Otherwise, insert original symbol
                                newString += self.insertParameters(n)
                            else:
                                newString += generator[j]
                else: #if the character is not in the keylist (+,-,etc.) then just add the character
                    newString += string[i]
            return self.dolSystem(newString,n-1,rules) #recursive call: new String is now our starting string and n = n-1

    '''When the turtle reads F, the turtle moves forward.
    F i also stores the sidelength, or how much the turtle should move forward.
    The branches closer to the trunk should be longer, and branches farther away should be shorter. '''
    def insertParameters(self,n):
        sidelength = int(self.step*(0.65**(self.startN-n))) #the higher the n, the earlier in the recursive call, the longer the sidelength.
        string = "F({})"
        return string.format(sidelength)

    def draw(self):
        numItems=0 #number of items in the stack
        stack = []
        turtle.colormode(255)
        t = turtle.Turtle()
        t.getscreen().screensize(1000,1000)
        t.speed(0)
        t.setheading(90)
        t.penup()
        t.setposition(self.startX,self.startY)
        t.pendown()
        width=40
        for i in range (len(self.instructions)):
            t.pencolor(0,0,0) #set trunk color to black
            if self.instructions[i]=="F":
                #get the sidelength for this step
                number = ""
                number += self.instructions[i+2] 
                if self.instructions[i+3].isdigit(): #assumes that the number will either be 2 digit or less.
                    number += self.instructions[i+3]
                sidelength = int(number)
                
                heading = t.heading()+random.randint(-8,8)
                t.setheading(heading)
                
                '''Many of the artistic elements rely on sidelength.
                If the sidelength greater than 25, add more subtle width change to create smooth branches
                If the sidelength is greater than or equal to 10, add curvature.
                Otherwise, decrease width by x 0.707.
                If the sizelength is less than 3, draw leaves
                '''
                if sidelength >= 25:
                    die= random.randint(0,1)
                    currentWidth = width
                    newWidth =0.707*width
                    numSteps = int(sidelength/3)
                    widthChange = (currentWidth - newWidth)/numSteps
                    theta=0
                    #randomly chooses if curve goes down or up
                    if die ==0:
                        if sidelength < 83:
                           theta=-25
                    if die ==1:
                        if sidelength < 83:
                            theta=25
                    
                    #for each tiny step, curve and increment width
                    for i in range (numSteps):
                        if i< numSteps/3:
                            t.setheading(heading+theta)
                        if i> numSteps/3 and i< 2*numSteps/3:
                            t.setheading(heading+(theta/2))
                        if i> 2*numSteps/3:
                            t.setheading(heading)
                        width = width - widthChange
                        t.pensize(width)
                        t.forward(3)
                        
                elif sidelength >= 10:
                    #for each step curve and then make width smaller
                    t.setheading(heading+(theta/2))
                    t.pensize(width)
                    t.forward(sidelength/2)
                    t.setheading(heading)
                    t.forward(sidelength/2)
                    width=width*0.707
                    
                else:
                    #for each step make width smaller
                    t.pensize(width)
                    t.forward(sidelength)
                    width=width*0.707
                    
                    if sidelength <3: #draw leaves
                        t.shape("circle")
                        #set size of leaf
                        for i in range(random.randint(2,4)):
                            leafWidth=random.randint(3,5)/20
                            leafLength=random.randint(1,2)/20
                            t.shapesize(leafWidth,leafLength,0)
                            t.tilt(random.randint(0,90))
                            #color schemes
                            if self.treeColor=="light green":
                                t.color(random.randint(0,100),random.randint(100,230),0)
                            if self.treeColor == "dark green":
                                t.color(0,random.randint(51,153),random.randint(0,80))
                            if self.treeColor == "autumn red":
                                die = random.randint(0,3)
                                if die == 0:
                                    t.color(random.randint(100,200),0,0) #red orange
                                else:
                                    t.color(255,random.randint(0,140),0)
                            if self.treeColor == "lavendar":
                                green=random.randint(0,170)
                                t.color(140+int(green/3),green,255)
                                
                            if self.treeColor=="purple":
                                t.color(random.randint(52,204),0,random.randint(52,204))
                            
                            t.stamp();
                            
                            
            #turn right
            if self.instructions[i]=="+":
                t.right(random.randint(self.angle-10,self.angle+10))  
                
            #turn left
            if self.instructions[i]=="-":
                t.left(random.randint(self.angle-10,self.angle+10))  
            
            #Save position, heading, and width in stack. Uses CurrentState class
            if self.instructions[i]=="[":
                position= t.position()
                heading = t.heading()
                currentState = CurrentState(position,heading,width)
                stack.append(currentState)
                numItems += 1
            
            #Get and set position, heading, and width from stack. Uses CurrentState class
            if self.instructions[i]=="]":
                newState = stack[numItems-1]
                t.penup()
                t.setposition(newState.getPosition())
                t.setheading(newState.getHeading())
                width = newState.getWidth()
                t.pendown()
                stack.pop()
                numItems -= 1
                
        t.hideturtle()
        t.getscreen().getcanvas().postscript(file="JKL-System.eps")
        

#create tree
tree = LSystem(9,83,0,-340,40,"light green", "X", {"X":["F[+Y]F[-Y]F[+Y]FY","F[-Y]F[+Y]F[-Y]FY"],"Y":["F[+Y]F[-Y]FY","F[-Y]F[+Y]FY","F[+Y][-X]FY","F[+Y][-X]","F[+Y]FY","F[-Y]FY"]})


    
