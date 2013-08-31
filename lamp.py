#!/usr/bin/python

from boxes import *
import math


"""
22x7.5x7cm
D=23cm, d=21cm
d = 8" D = 9"
"""

class RoundedTriangleSettings(Settings):
    absolute_params = {
        "angle" : 60,
        "radius" : 30,
        "r_hole" : None,
        }

class RoundedTriangle(Edge):
    char = "t"
    def __call__(self, length, **kw):
        angle = self.settings.angle
        r = self.settings.radius

        if self.settings.r_hole:
            x = 0.5*(length-2*r)*math.tan(math.radians(angle))
            y =  0.5*(length)
            self.hole(x, y, self.settings.r_hole)

        l = 0.5 * (length-2*r) / math.cos(math.radians(angle))
        self.corner(90-angle, r)
        self.edge(l)
        self.corner(2*angle, r)
        self.edge(l)
        self.corner(90-angle, r)

    def startAngle(self):
        return 90

    def endAngle(self):
        return 90

class Lamp(Boxes):
    def __init__(self):
        Boxes.__init__(self, width=1000, height=1000,
                       thickness=5.0, burn=0.05)
        self.fingerJointSettings = (5, 5) # XXX

        s = RoundedTriangleSettings(self.thickness, angle=72, r_hole=2)
        self.addPart(RoundedTriangle(self, s))


    def side(self, y, h):
        return
        self.fingerJointEdge(y)
        self.corner(90)
        self.fingerJointEdge(h)
        self.roundedTriangle(y, 75, 25)
        self.fingerJointEdge(h)
        self.corner(90)

    def render(self, r, w, x, y, h):
        """
        r : radius of lamp
        w : width of surrounding ring
        x : length box
        y : width box
        h : height box
        """
        self.fingerJointEdge.settings.setValues(self.thickness, finger=5, space=5, relative=False)
        d = 2*(r+w)

        self.roundedPlate(d, d, r, move="right", callback=[
                lambda: self.hole(w, r+w, r),])
        #dist = ((2**0.5)*r-r) / (2**0.5) + 4
        #pos = (w-dist, dist)
        self.roundedPlate(d, d, r, holesMargin=w/2.0) #, callback=[
        #        lambda: self.hole(pos[0], pos[1], 7),])
        self.roundedPlate(d, d, r, move="only left up")

        hole = lambda: self.hole(w, 70, 2)
        self.surroundingWall(d, d, r, 120, top='h', bottom='h', callback=[
                None, hole, None, hole], move="up")

        self.ctx.save()
        self.rectangularWall(x, y, edges="fFfF", holesMargin=5, move="right")
        self.rectangularWall(x, y, edges="fFfF", holesMargin=5, move="right")
        # sides
        self.rectangularWall(y, h, "fftf", move="right")
        self.rectangularWall(y, h, "fftf")
        self.ctx.restore()
        self.rectangularWall(x, y, edges="fFfF", holesMargin=5,
                             move="up only")

        self.rectangularWall(x, h, edges='hFFF', holesMargin=5, move="right")
        self.rectangularWall(x, h, edges='hFFF', holesMargin=5)
        self.ctx.stroke()
        self.surface.finish()


l = Lamp()
l.flexSettings = (3, 5.0, 20.0)
l.render(r=4*25.4, w=20, x=270, y=150, h=100)