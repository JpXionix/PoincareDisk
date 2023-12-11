import cmath

#change window size to your needs!
screen_x = 800
screen_y = 800

class P_disc:
    """
    A class of static methods for calculations on the pioncaré disc
    """
    @staticmethod
    def translation(z,a):
        """
        input: 
            z = (complex) Point to be translated
            a = (complex) translation vector
        output:  translated Point(complex) z'
        """
        return (z + a) / (1 + a.conjugate() * z)

    @staticmethod    
    def dist(a,b):
        """
        input :
            a,b = Point(complex)
        output: (float)  hyperbolic distance betweent these two points on the pioncare disc 
        """
        delta = abs((a - b) / (1 - b.conjugate() * a))
        return 1/2 * log((1 + delta) /( 1 - delta))
 
    @staticmethod  
    def equilateral_Shape(n,r, circles = False):
        """
        input :
            n = (integer) amount of Edges of the equilateral shape
            r = (float) radius of the cicles to calculate the shape corners
            circles = (boolean) debugging parameter to draw the cicles which are used to calcuated shape corners
        output: (instance of Hyperbolic_Shape) n-shape with equilateral properties on the poincare disc
        """
        global radius
        alpha = radians(float(360/n))
        if circles == True: # debug use , prints cicles to calcuated shape corners
            i = 1
            stroke(0,0,0)
            noFill()
            while i <= n:
                p = interpret_point(complex(cos(i * alpha), sin(i * alpha)) * complex(0,1))
                i += 1
                point(p[0],p[1])
                circle(p[0],p[1],r*2*radius)
                
        d = (abs(complex( cos(2 * alpha), sin(2 * alpha))
            - complex( cos(alpha), sin(alpha))))
        if d <= 2*r: #early check if cicles intersect
            intersections = []
            i = 1
            while i <= n: # calculated intersection with cicle_intersections() for each circlepair
                solutions = cicle_intersections(complex(cos((i+1) * alpha), sin((i+1) * alpha)),r, complex( cos(i * alpha), sin(i * alpha)), r, d)
                if abs(solutions[0]) <= abs(solutions[1]) <= 1: #check which solution is closer to the center
                    intersections.append(solutions[0] * complex(0,1)) # add rotation of 90 degree (gives me inner peace this way)
                elif abs(solutions[1]) <= 1:
                    intersections.append(solutions[1] * complex(0,1))
                else: # None of the solutions are on the unit cicle. Will be true for all pairs, so interupt the whole loop
                    break
                i += 1
            if intersections == []:
                textbox_print("Radius to big!")
                return None
            k = len(intersections)-1
            equilateral = (Hyperbolic_Shape(
                          Hyperbolic_Line(intersections[0],intersections[k])))
            colorlist = [[0,0,255],[0,255,0],[255,0,0],[204,204,0],[157,0,157]]
            while k >= 1:
                picker = k % len(colorlist)
                (equilateral.include(Hyperbolic_Line(
                intersections[k],intersections[k-1],colorlist[picker])))
                k -= 1
            return equilateral
                
        else:
            textbox_print("Radius to small!")
            return None


class Hyperbolic_Line:
    '''
    A class which represents a Line on the Pioncaré Disk
    ''' 
    def __init__(self,a,b, tcolor = [0,0,255], tpath = True):
        """
        input : a = (complex number) A Point on the Line
                b = (complex number) A point on the Line
                tcolor = (3 Element List of Int) represents RBG Code for Line color
                tpath = (boolean) will only draw the path from a to b
        Output: Instance of Hyperbolic_Line
        """
        self.p1 = a
        self.p2 = b
        self.color = tcolor
        self.center = self.calc_center()
        self.path = tpath
        self.drawline()
        
        
    def calc_center(self):
        '''
        calculates the center of the orto-cicle with given points
        '''
        denominator = self.p1 * self.p2.conjugate() - self.p1.conjugate() * self.p2
        if denominator != complex(0,0):
            numerator = (self.p1 * ( 1 + abs(self.p2)**2)
                         - self.p2 * (1 + abs(self.p1)**2 ))
            return numerator/denominator
        else:
            return None
    
    def drawline(self):
        '''
        draws the hyerbolic line
        '''
        if self.center == None: #special case where the line is a euclidian line
            a = interpret_point(self.p1)
            b = interpret_point(self.p2)
            stroke(self.color[0],self.color[1],self.color[2])
            line(a[0],a[1],b[0],b[1])
        else:
            global radius
            r = abs(self.p1 - self.center)
            p = interpret_point(self.center)
            if self.path == True:
                radians1 = cmath.phase(self.p1 - self.center)
                radians2 = cmath.phase(self.p2 - self.center)
            else:
                intersections = cicle_intersections(self.center, r, complex(0,0), 1)
                radians1 = cmath.phase(intersections[0] - self.center) 
                radians2 = cmath.phase(intersections[1] - self.center)
            # check if we got the smaller arc
            if abs( radians1 - radians2) > PI:
                if radians1 < radians2:
                    radians1 += 2*PI
                else:
                    radians2 += 2*PI
            if radians1 > radians2:
                radians1, radians2 = radians2, radians1
            stroke(self.color[0],self.color[1],self.color[2])
            noFill()
            arc(p[0],p[1],r*2*radius,r*2*radius,radians1,radians2)
            
    def mirror(self,z):
        """
        input : z = (complex) point to be mirroed
        output:  (complex) mirroed point z'
        """
        numerator = self.center * z.conjugate() - 1
        denominator =  z.conjugate() - self.center.conjugate() 
        return numerator/denominator
    
    def translate(self, a, tcolor = [255,0,0]):
        """
        input : a = (complex) vector to translate line
        tcolor = (3 Element List of Int) represents RBG Code for Line color the translated line
        output: (instance of Hyperbolic_Line) translated line with vector a
        """
        return Hyperbolic_Line(P_disc.translation(self.p1,a), P_disc.translation(self.p2,a), tcolor, self.path)              

            
class Hyperbolic_Shape:
    '''
    A class filled with instances of Hyberbolic_line to group them into one Shape
    ''' 
    
    def __init__(self,*input):
        """
        input : any Number of instances of Hyberbolic_line
        Output: Instance of Hyperbolic_Shape
        """
        #self.n = 0
        #self.edges = []
        self.lines = []
        shapelist.append(self)
        for l in input:
            self.include(l)
    
    def include(self,l):
        """
        Includes a Hyberbolic_line instance into the Shape
        input : l = Hyberbolic_line instance
        """
        self.lines.append(l)
        #self.edges.extend([l.p1,l.p2])
        #self.n += 1
        
    def tesselation(self,m = 10, ignore_first = False):
        """
        tesselation of the Pioncare Disk with given Shape
        input : m = (int) Loopsteps left until the recursion stops
                ignore_first = (boolean) should be False if called , used to skip the first line of the used shape to stop remirroring already calcaulted and drawn shapes
        """
        if m > 0:
            for l in self.lines:
                if ignore_first == True:
                    ignore_first = False
                    continue
                mirrored = Hyperbolic_Shape(l)
                for j in self.lines:                                                                                                                                                                                                                                         
                    if l != j:
                        mirrored.include(Hyperbolic_Line( l.mirror(j.p1) , l.mirror(j.p2), j.color, j.path))
                        mirrored.tesselation(m-1,True)
                        
  
class Button:
    """
    represent a Menu Button, should only be inherited from, has no action on press
    """
    def __init__(self,x,y,tpic, tpressedpic):
        """
        input : x = (int) x-Position of the Button on a 20x20 grid
                y = (int) y-Position of the Button on a 20x20 grid
                tpic = (processing pic) pictures of the unpressed button allready loaded in load_images()
                tpressedpic = (processing pic) pictures of the pressed button allready loaded in load_images()
        Output: Instance of Button
        """
        global buttonlist
        self.px = float(x)
        self.py = float(y)
        self.pic = tpic
        self.pressed_pic = tpressedpic
        self.pressed = False
        buttonlist.append(self)
        
    def update(self):
        """
        method to draw the button with the right image
        """
        if self.pressed == False:
            image(self.pic, (width/20) * self.px ,(height/20) * self.py, width/20, height/20)
        else:
            image(self.pressed_pic, self.px*width/20, self.py*height/20, width/20 , height/20)
            
    def action(self):
        """
        method to handle the button press
        """
        return "Nothing todo here"
        
    def check(self,pos):
        """
        method to check if a point(mouseclick) is inside this button, so the button can be considers pressed
        input : pos ( 2 Element List of Integer) Position of the Point on the Canvas
        """
        if self.px*(width/20) <= pos[0] < (self.px+1)*(width/20) and self.py*(height/20) <= pos[1] < (self.py+1)*(height/20):
            self.action()
            return True # indicator to break loops
        
class Number_button(Button):
    """
    represent a Number Button
    """
    
    def __init__(self,x,y,tpic, tpressedpic, tnumber):
        """
        for whatever reason super() seems not to work on this jyhton interpreter , so here we go again
        input : same as in Button
                tumber (int) Number associated with this button
        Output: Instance of Number_button
        """
        self.px = x
        self.py = y
        self.pic = tpic
        self.pressed_pic = tpressedpic
        self.number = tnumber
        self.pressed = False
        buttonlist.append(self)
        
    def action(self):
        """
        method to handle the button press , handles animations and calls number_pressed()
        """
        global lastnumberpressed
        lastnumberpressed.pressed = False
        lastnumberpressed.update()
        lastnumberpressed = self
        self.pressed = True
        self.update()
        number_pressed(self.number)
        
class Tool_button(Button):
    
    def __init__(self,x,y,tpic,tpressedpic ,ttool):
        """
        for whatever reason super() seems not to work on this jyhton interpreter , so here we go again
        input : same as in Button
                ttool (int) Number of the Tool associated with this button
        Output: Instance of Tool_button
        """
        self.px = x
        self.py = y
        self.pic = tpic
        self.pressed_pic = tpressedpic
        self.toolnumber = ttool
        self.pressed = False
        buttonlist.append(self)
        
    def action(self):
        """
        method to handle the button press, handles animations,
        checks if the unit cicle need to be redrawn and calls change_mode()
        """
        global lasttoolpressed
        global redraw_lines
        clear_textbox()
        if redraw_lines == True:
            redraw_all()
        lasttoolpressed.pressed = False
        lasttoolpressed.update()
        self.pressed = True
        self.update()
        lasttoolpressed = self
        change_mode(self.toolnumber)
        

# do not change Variables
origin = [screen_x/2, screen_y/2] #origin of the unit cicle
radius = float(min(screen_x,screen_y)) / 2 # radius of the unit cicle
stored = complex(0,0) #stored the last clicked point on the unit circle
clicks = 0 #hold the amounts of clicks
mode = 1 #stores the menu mode
shapelist = [] #list of all hyberbolic shapes
buttonlist = [] #list of all buttons
lastnumberpressed = None #keeps the last number pressed for animation
lasttoolpressed = None #keeps the last tool pressed for animation
selector = 0 #holds which layer is selected
to_be_mirrored = None #holds the line which has to be mirrored
amount = None #holds the amount of interations
redraw_lines = False #keeps track if all lines have to be redrawn on tool change
typing = "" #holds the keyboard inputs
input = "input" #holds the keyboard input after ENTER


def interpret_point(input):
    global radius
    global origin
    '''
    Interpret a complex number z into a touple of R^2 , does a basis change and translate
    its location based on the cicle midpoint "origin" and radius of the cicle
    
    For example if midpoint M(m1,m2) with  radius r, then z = x+iy will be
     mapped to [x*r + m1, y*r + m2]
     
    input: input : complex number or List(2 Elements of floats)
    output: P: List of 2 real numbers forming a point in R^2 or a complex number
    '''
    if type(input) == complex: #from C to R^2
        return [ input.real * radius + origin[0] , input.imag * radius + origin[1]]
    
    elif type(input) == list: #from R^2 to C
        return complex((input[0] - origin[0])/ radius, (input[1] - origin[1])/ radius)
    
    else:
        print("invalid Type")
        return None
    
def cicle_intersections(m1, r1, m2 , r2, d = None):
    """
    function to calculate the intersections of to cicles, optional distance (d) to cut calculations
    m1 = (complex) Midpoint of circle 1
    r1 = (float) radius of Cicle 1
    m2 = (complex) Midpoint of cicle 2
    r2 = (float) Midpoint of cicle 2
    d = (float) parameter for iteral calls with same distance to cut calculations
    return: (list of complex) both intersection of cicle 1 and 2.
    """
    if d == None:
        d = abs(m1 - m2)
    if d <= r1+r2:
        v = (m2 - m1) / d # normalized direction vector M1M2
        nv= complex(- v.imag , v.real) 
        #negative reciprocal of v to get its normal vector
        if r1==r2: #common case, optimated calculation
            t = d/2 # distance from M1 to intersection of M1M2 and P1P2
        else:
            t = (r1**2 - r2**2 + d**2) / (2*d)
        l = sqrt(r1**2 - t**2) # length of the path from P1 to P2
        s = m1 + t * v #move to intersection from M1M2 and P1P2
        return [s + l * nv, s - l * nv] # move up to P1, move down to P2
    else: #sum of radii to small
        return None
        
# Hud functions    
    
def load_images():
    """
    loads in all icon images , this can only happend inside setup() and still needs to be declared to be global so they can be seen in draw().
    else the image have to be loaded each time they should be drawn.
    """ 
    global line_pic
    global line_pic_pressed
    global path_pic
    global path_pic_pressed
    global mirror_pic
    global mirror_pic_pressed
    global transpose_pic
    global transpose_pic_pressed
    global equal_pic
    global equal_pic_pressed
    global tesselate_pic
    global tesselate_pic_pressed
    global select_pic
    global select_pic_pressed
    global screen_pic
    global screen_pic_pressed
    global trash_pic
    global trash_pic_pressed
    global zero_pic
    global zero_pic_pressed
    global one_pic
    global one_pic_pressed
    global two_pic
    global two_pic_pressed
    global three_pic
    global three_pic_pressed
    global four_pic
    global four_pic_pressed
    global five_pic
    global five_pic_pressed
    global six_pic
    global six_pic_pressed
    global seven_pic
    global seven_pic_pressed
    global eight_pic
    global eight_pic_pressed
    global nine_pic  
    global nine_pic_pressed
    line_pic = loadImage("line.png")
    line_pic_pressed = loadImage("line_pressed.png")
    path_pic = loadImage("path.png")
    path_pic_pressed = loadImage("path_pressed.png")
    mirror_pic = loadImage("mirror.png")
    mirror_pic_pressed = loadImage("mirror_pressed.png")
    transpose_pic = loadImage("transpose.png")
    transpose_pic_pressed = loadImage("transpose_pressed.png")
    equal_pic = loadImage("equal.png")
    equal_pic_pressed = loadImage("equal_pressed.png")
    tesselate_pic = loadImage("tesselate.png")
    tesselate_pic_pressed = loadImage("tesselate_pressed.png")
    select_pic = loadImage("select.png")
    select_pic_pressed = loadImage("select_pressed.png")
    screen_pic = loadImage("screen.png")
    screen_pic_pressed = loadImage("screen_pressed.png")
    trash_pic = loadImage("trash.png")
    trash_pic_pressed = loadImage("trash_pressed.png")
    zero_pic = loadImage("0.png")
    zero_pic_pressed = loadImage("0_pressed.png")
    one_pic = loadImage("1.png")
    one_pic_pressed = loadImage("1_pressed.png")
    two_pic = loadImage("2.png")
    two_pic_pressed = loadImage("2_pressed.png")
    three_pic = loadImage("3.png")
    three_pic_pressed = loadImage("3_pressed.png")
    four_pic = loadImage("4.png")
    four_pic_pressed = loadImage("4_pressed.png")
    five_pic = loadImage("5.png")
    five_pic_pressed = loadImage("5_pressed.png")
    six_pic = loadImage("6.png")
    six_pic_pressed = loadImage("6_pressed.png")
    seven_pic = loadImage("7.png")
    seven_pic_pressed = loadImage("7_pressed.png")
    eight_pic = loadImage("8.png")
    eight_pic_pressed = loadImage("8_pressed.png")
    nine_pic = loadImage("9.png")
    nine_pic_pressed = loadImage("9_pressed.png")
    
def setup_hud():
    """
    function to create all Buttons instances for the user Interface
    """
    global lastnumberpressed
    global lasttoolpressed
    B_line = Tool_button(0,0,line_pic,line_pic_pressed,0)
    B_path = Tool_button(1,0,path_pic,path_pic_pressed,1)
    B_mirror = Tool_button(2,0,mirror_pic,mirror_pic_pressed,2)
    B_transpose = Tool_button(3,0,transpose_pic,transpose_pic_pressed,3)
    B_equal = Tool_button(1,1,equal_pic,equal_pic_pressed,4)
    B_tesselate = Tool_button(2,1,tesselate_pic,tesselate_pic_pressed,5)
    B_select = Tool_button(0,2,select_pic,select_pic_pressed,6)
    B_screen = Tool_button(1,2,screen_pic,screen_pic_pressed,7)
    B_trash = Tool_button(0,3,trash_pic,trash_pic_pressed,8)
    #Path Tool is selected on Programm start, fix animation
    lasttoolpressed = B_path
    lasttoolpressed.pressed = True
    
    B_0 = Number_button(16,0,zero_pic,zero_pic_pressed,0)
    B_1 = Number_button(17,0,one_pic,one_pic_pressed,1)
    B_2 = Number_button(18,0,two_pic,two_pic_pressed,2)
    B_3 = Number_button(19,0,three_pic,three_pic_pressed,3)
    B_4 = Number_button(17,1,four_pic,four_pic_pressed,4)
    B_5 = Number_button(18,1,five_pic,five_pic_pressed,5)
    B_6 = Number_button(19,1,six_pic,six_pic_pressed,6)
    B_7 = Number_button(18,2,seven_pic,seven_pic_pressed,7)
    B_8 = Number_button(19,2,eight_pic,eight_pic_pressed,8)
    B_9 = Number_button(19,3,nine_pic,nine_pic_pressed,9)
    #Layer 0 is selected on Programm start, fix animation
    lastnumberpressed = B_0
    lastnumberpressed.pressed = True
    
def update_hud():
    """
    function to draw all buttons in buttonlist
    """
    for button in buttonlist:
        button.update()
    
def clear_textbox():
    """
    function to clear the textbox
    """
    stroke(255,255,255)
    fill(255,255,255)
    rect( 0.5 * width/20 , 18.5* height/20, 3.5 * width/20, height/20, 10)
        
def redraw_all():
    """
    function to redraw all shapes in shapelist. Used for the select , photo and delete mode
    """
    global shapelist
    global raidus
    global origin
    # just in case clear Unit Cicle
    fill(255)
    stroke(255,255,255)
    circle(origin[0], origin[1], 2*radius)
    for s in shapelist:
        for l in s.lines:
            l.drawline()
    redraw_lines = False #set redraw flag off

def interpret_input(input):
    """
    function to interpret the input given. Only numbers are actually used , but takes str for implementation for commands of some sort
    input: input (str) to check
    """
    global selector
    global mode
    is_int = True
    is_float = True
    #check if the string can be converted to int and float
    try:
        int(input)
    except ValueError:
        is_int = False
    try:
        float(input)
    except ValueError:
        is_float = False
    
    if is_float == True and mode == 9: #second instance of equal shape, input via keyboard
        P_disc.equilateral_Shape(selector,abs(float(input)))
    elif is_int == True and mode != 9:
        if int(input) > 9: #number input higher the any Number Button
            lastnumberpressed.pressed = False
            lastnumberpressed.update()
            number_pressed(int(input))
        else:
            for button in buttonlist: #check which button corresponds to given number for animation
                if isinstance(button,Number_button) == True and button.number == int(input):
                    button.action()
                    break
    
def change_mode(n):
    """
    function to react to mode changes , mostly used to give user feedback , but also used to get 1 or 2 click actions
    input: n (int) the number mode to replay to
    """
    global mode
    global shapelist
    #Check for double presses
    if mode == 8 and n==8: #delete button pressed twice: eradicte everything!
        del shapelist
        shapelist = []
        fill(255)
        stroke(255,255,255)
        circle(origin[0], origin[1], 2*radius)  
          
    mode = n
    if mode == 2: #Mirror case
        textbox_print("Mirror which layer?")
    elif mode == 3: #transaltion case
        textbox_print("Move which layer?")
        
    elif mode == 4: #first instance equal shape case
        textbox_print("How many edges?")
        
    elif mode == 5: #tesselation case
        textbox_print("How many iterations?")
        
    elif mode == 6: #selecting case
        textbox_print("Show which layer?")
        
    elif mode == 7: #screenshot without user interface
        #can't overdraw button wuhtout overdrawing the unit circle , so clear the whole canvas
        background(0)
        fill(255)
        stroke(255,255,255)
        circle(origin[0], origin[1], 2*radius)
        redraw_all()
        save("Poincare_disc.png")
        update_hud()
        textbox_print("Photo taken!")
    
    elif mode == 8: #delete case
        textbox_print("Delete which layer?")
        
        
    
def number_pressed(number):
    """
    function to handle number input for modes which uses the number inputs for everything else then layer selection
    input: number (int) the number to act on
    """
    global to_be_mirrored
    global selector
    global mode
    global amount
    selector = number
    # Statecheck , which mode is active?
    if mode == 2: #mirror mode
        if to_be_mirrored == None and len(shapelist) >= selector: #user want this layer to me mirrored
            to_be_mirrored = selector #set layer to be mirrored
            textbox_print("On which layer?")
        elif len(shapelist) >= selector: #user want this layer to be the mirror
            newshape = Hyperbolic_Shape()
            for l in shapelist[to_be_mirrored].lines:
                for j in shapelist[selector].lines:
                    newshape.include( Hyperbolic_Line( j.mirror(l.p1) , j.mirror(l.p2) , l.color, l.path))
            to_be_mirrored = None
            shapelist.append(newshape)
        else:
            textbox_print("Layer is Empty!")
    elif mode == 4: #equal shape mode, n has been selected
        if selector > 2:
            mode = 9 # set to second instance of equal shape
            textbox_print("Radius?")
        else: # errorcatch n<3
            textbox_print("Needs at least 3!")
    elif mode == 5: #tesselation Case
        if amount == None: #get n
            amount = selector
            textbox_print("Which layer?")
        elif len(shapelist) >= selector:
            shapelist[selector].tesselation(amount)
            amount == None
    elif mode == 6: #selecting Case
        global origin
        global radius
        global redraw_lines
        #clear Unit Cicle
        stroke(255,255,255)
        fill(255)
        circle(origin[0], origin[1], 2*radius)
        if len(shapelist) > selector: # check if selected shape exist for error catching
            for l in shapelist[selector].lines:
                l.drawline()
            redraw_lines = True
    elif mode == 8: #Delete Case
        if len(shapelist) > selector: # check if selected shape exist for error catching
            del shapelist[selector].lines
            shapelist[selector].lines = []
            redraw_all()
            
        
def textbox_print(string):
    """
    function to print strings in the textbox
    input: string (string) message to be printed in the textbox
    """
    clear_textbox()
    fill(0,0,0) #change fontcolor to black
    text(string, 0.6*width/20, 18.8*height/20, 3.5*width/20, height/20)        
    
        
    
                 
                    
            
# Processing Functions        

def setup():
    """
    Runs on once on programm start, processing function for setup can only be run here
    """
    global screen_x
    global screen_y 
    global origin
    global radius
    size(screen_x,screen_y)
    textSize(screen_x/55)
    background(0)
    fill(255)
    stroke(255,255,255)
    circle(origin[0], origin[1], 2*radius)
    load_images()
    setup_hud()
    update_hud()
    clear_textbox()
    
def mousePressed():
    """
    Runs on any mouse click, position of the click is stored in "mouseX" and "mouseY"
    """
    global stored
    global clicks
    global selector
    global shapelist
    global mode
    global buttonlist
    if abs(interpret_point([mouseX,mouseY])) <= 1:
        if clicks == 1:
            if mode <= 1:
                while len(shapelist) <= selector:
                    newshape = Hyperbolic_Shape()
                if mode == 0: #draw line
                    shapelist[selector].include(Hyperbolic_Line(stored, interpret_point([mouseX,mouseY]), [0,0,255], False))
                else: #draw path
                    shapelist[selector].include(Hyperbolic_Line(stored, interpret_point([mouseX,mouseY])))
            elif mode == 3 and len(shapelist) >= selector:
                    newshape = Hyperbolic_Shape()
                    for l in shapelist[selector].lines:
                        newshape.include(l.translate(interpret_point([mouseX,mouseY]) - stored, l.color))
                    shapelist.append(newshape)
            elif mode == 9: #draw equal shape
                P_disc.equilateral_Shape(selector,abs(interpret_point([mouseX,mouseY]) - stored))
            clicks = 0
        else:
            stored = interpret_point([mouseX,mouseY])
            clicks +=1
    else: # Button is meant to be pressed , check which one
        for button in buttonlist:
            if button.check([mouseX,mouseY]) == True:
                break
    

        
def keyPressed():
    """
    Runs on any keyboard press , pressed key is automatically stored in "key"
    """
    global input
    global typing
    global selector
    if key == ENTER:
        input = typing
        interpret_input(input)
        typing = ""
    else:
        typing = typing + str(key)
        clear_textbox()
        fill(0,0,0)
        text(str(typing), 0.6* width/20 , 18.8* height/20, 3.5 * width/20, height/20 )
    
        
def draw():
    """
loop function, calls "pressed functions" on its own
    """
    return
