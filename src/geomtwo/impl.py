import geomtwo.msg as gms
import matplotlib.pyplot as plt
import cmath as cm





class Vector:

    def __init__(self, *args, **kwargs):
        if len(args) is 2:
            self._data = complex(*args)
            return
        if len(args) is 1:
            if isinstance(args[0], (self.__class__, gms.Vector)):
                self._data = complex(args[0].x, args[0].y)
                return
            if isinstance(args[0], complex):
                self._data = complex(args[0])
                return
        if len(args) is 0:
            if set(kwargs.keys()) == set(("x", "y")):
                self.__class__.__init__(self, kwargs["x"], kwargs["y"])
                return
            if set(kwargs.keys()) == set(("magnitude", "angle")):
                self.__class__.__init__(self, kwargs["magnitude"]*cm.cos(kwargs["angle"]), kwargs["magnitude"]*cm.sin(kwargs["angle"]))
                return
            if len(kwargs) is 0:
                self.__class__.__init__(self, 0, 0)
                return
        raise ValueError("Constructor arguments for {} not recognized".format(self.__class__.__name__))

    @property
    def message(self):
        return gms.Vector(self.x, self.y)

    def __str__(self):
        string = "{} instance".format(self.__class__.__name__)
        string += "\nx: " + str(self._data.real)
        string += "\ny: " + str(self._data.imag)
        return string

    def draw(self, x0=0., y0=0., **kwargs):
        head_size = 0.1*abs(self._data)
        artist = plt.gca().arrow(x0, y0, self.x, self.y, head_length=head_size, head_width=head_size, **kwargs)
        return artist,

    @property
    def x(self): return self._data.real

    @property
    def y(self): return self._data.imag

    @property
    def complex_number(self):
        return self._data

    @property
    def norm_squared(self):
        return self.x**2 + self.y**2

    @property
    def norm(self):
        return abs(self._data)

    @property
    def vector(self):
        return Vector(self)

    def __add__(self, other):
        return self.__class__(self._data+other._data)

    def __neg__(self):
        return self.__class__(-self._data)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, self.__class__): return self.__class__(self._data*other._data)
        if isinstance(other, (int,float)): return self.__class__(float(other)*self._data)
        raise TypeError()

    def __rmul__(self, other):
        return self.__class__(other*self._data)

    def __div__(self, other):
        return self*(1.0/other)

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def cross(self, other):
        return self.x*other.y-self.y*other.x

    def angle_to(self, other, force_positive=False):
        result = cm.phase(complex(self.dot(other),self.cross(other)))
        if result < 0 and force_positive: result += 2*cm.pi
        return result

    def rotate(self, angle):
        return self.__class__(self._data*cm.rect(1.0, angle))

    def saturate(self, threshold):
        if self.norm > threshold: return self*threshold/self.norm
        return self



if __name__ == "__main__":
    vec = Vector(gms.Vector(x=2,y=3))
    print vec
    vec2 = Vector(x=1,y=2)
    print vec + vec2
    print vec - vec2
    print vec.dot(vec2)
    print 2*vec
    print vec2.angle_to(vec, force_positive=True)
    plt.figure()
    plt.xlim([-5,5])
    plt.ylim([-5,5])
    vec.draw()
    #plt.show()





class Point(Vector):

    def __init__(self, *args, **kwargs):
        if len(args) is 1 and isinstance(args[0], (gms.Point, self.__class__)):
            self.__class__.__init__(self, args[0].x, args[0].y)
            return
        Vector.__init__(self, *args, **kwargs)

    def draw(self, **kwargs):
        return plt.scatter(self.x, self.y, **kwargs),

    def __add__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("You are trying to add {} and {}. One cannot add two {}".format(self, other, self.__class__))
        return Vector.__add__(self, other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self._data - other._data)
        return self + (-other)

    @property
    def message(self):
        return gms.Point(self.x, self.y)

    def __mul__(self, other): raise TypeError
    def __rmul__(self, other): raise TypeError
    def __div__(self, other): raise TypeError
    def dot(self, other): raise TypeError
    def cross(self, other): raise TypeError
    def angle_to(self, other): raise TypeError
    def saturate(self, other): raise TypeError





if __name__ == "__main__":
    pt = Point(gms.Point())
    pt.draw()
    pt2 = Point(2,3)
    (pt-pt2).draw(color="red")
    #plt.show()
    print pt2+vec





class Versor(Vector):

    def __init__(self, *args, **kwargs):
        if len(args) is 2:
            norm = cm.sqrt(args[0]**2+args[1]**2)
            Vector.__init__(self, args[0]/norm, args[1]/norm)
            return
        if len(args) is 1:
            if isinstance(args[0], (gms.Vector, gms.Versor, Vector, Versor)):
                self.__class__.__init__(self, args[0].x, args[0].y)
                return
            if isinstance(args[0], complex):
                self.__class__.__init__(self, args[0].real, args[0].imag)
                return
            if isinstance(args[0], float):
                self.__class__.__init__(self, cm.cos(args[0]), cm.sin(args[0]))
                return
        if len(args) is 0:
            if set(kwargs.keys()) == set(("x", "y")):
                self.__class__.__init__(self, kwargs["x"], kwargs["y"])
                return
            if set(kwargs.keys()) == set(("angle")):
                self.__class__.__init__(self, kwargs["angle"])
                return
            if len(kwargs) is 0:
                self.__class__.__init__(self, 1, 0)
                return
        raise TypeError()

    def serialize(self):
        return gms.Versor(self.x, self.y)

    def __add__(self, other): raise TypeError
    def __sub__(self, other): raise TypeError

    def saturate(self): raise TypeError




if __name__ == "__main__":
    vs2 = Versor(2,4)
    print vs2.norm, vs2.norm_squared
    vs2.draw()





class Transform:

    def __init__(self, *args, **kwargs):
        if len(args) is 2:
            translation, rotation = args
            if isinstance(translation, (Vector, gms.Vector)) and isinstance(rotation, (int,float)):
                self._translation = Vector(translation)
                self._rotation = float(rotation)
                return
        if len(args) is 1:
            if isinstance(args[0], (Transform, gms.Transform)):
                self.__class__.__init__(self, args[0].translation, args[0].rotation)
                return
        if len(args) is 0:
            if set(kwargs.keys()) == set("translation rotation".split()):
                self.__class__.__init__(self, kwargs["translation"], kwargs["rotation"])
                return
            if len(kwargs) is 0:
                self.__class__.__init__(self, Vector(), 0.0)
                return
        raise TypeError()

    def __str__(self):
        string = "{} instance".format(self.__class__.__name__)
        string += "\ntranslation: " + str(self._translation)
        string += "\nrotation: " + str(self._rotation)
        return string

    def __add__(self, other):
        return self.__class__(self._translation+other._translation, self._rotation+other._rotation)

    def __neg__(self):
        return self.__class__(-self._translation, -self._rotation)

    def __sub__(self, other):
        return self + (-other)

    @property
    def translation(self): return self._translation

    @property
    def rotation(self): return self._rotation

    @property
    def message(self): return gms.Transform(self._translation.message, self._rotation)












class Twist:

    def __init__(self, *args, **kwargs):
        if len(args) is 2:
            linear, angular = args
            if isinstance(linear, (Vector, gms.Vector)) and isinstance(angular, (int,float)):
                self._linear = Vector(linear)
                self._angular = float(angular)
                return
        if len(args) is 1:
            if isinstance(args[0], (Twist, gms.Twist)):
                self.__class__.__init__(self, args[0].linear, args[0].angular)
                return
        if len(args) is 0:
            if set(kwargs.keys()) == set("linear angular".split()):
                self.__class__.__init__(self, kwargs["linear"], kwargs["angular"])
                return
            if len(kwargs) is 0:
                self.__class__.__init__(self, Vector(), 0.0)
                return
        raise TypeError()

    def __str__(self):
        string = "{} instance".format(self.__class__.__name__)
        string += "\nlinear: " + str(self._linear)
        string += "\nangular: " + str(self._angular)
        return string

    def __add__(self, other):
        return self.__class__(self._linear+other._linear, self._angular+other._angular)

    def __neg__(self):
        return self.__class__(-self._linear, -self._angular)

    def __sub__(self, other):
        return self + (-other)

    @property
    def linear(self): return self._linear

    @property
    def angular(self): return self._angular

    @property
    def message(self): return gms.Twist(self._linear.message, self._angular)

    def integrate(self, time):
        return Transform( translation=self._linear*time, rotation=self._angular*time )















if __name__ == "__main__":
    tf = Transform()
    print tf
    tf2 = Transform(Vector(1,2), 3)
    print tf - tf2







class Pose:

    def __init__(self, *args, **kwargs):
        if len(args) is 2:
            pos, ori = args
            if isinstance(pos, (Point, gms.Point)) and isinstance(ori, (Versor, gms.Versor)):
                self._position = Point(pos)
                self._orientation = Versor(ori)
                return
        if len(args) is 1:
            if isinstance(args[0], (Pose, gms.Pose)):
                self.__class__.__init__(self, args[0].position, args[0].orientation)
                return
        if len(args) is 0:
            if set(kwargs.keys()) == set("position orientation".split()):
                self.__class__.__init__(self, kwargs["position"], kwargs["orientation"])
                return
            if len(kwargs) is 0:
                self.__class__.__init__(self, Point(), Versor())
                return
        raise TypeError()

    def __str__(self):
        string = "{} instance".format(self.__class__.__name__)
        string += "\nposition: " + str(self._position)
        string += "\norientation: " + str(self._orientation)
        return string

    def draw(self, **kwargs):
        return self._position.draw(**kwargs) + self._orientation.draw(x0=self._position.x, y0=self._position.y, **kwargs)

    @property
    def position(self):
        return self._position

    @property
    def orientation(self):
        return self._orientation

    @property
    def message(self):
        return gms.Pose(self._position.message, self._orientation.message)

    def __add__(self, transform):
        pos = self._position + transform.translation
        ori = self._orientation.rotate( transform.rotation )
        return self.__class__(pos, ori)

    def __sub__(self, transform):
        return self + (-transform)




if __name__ == "__main__":
    ps = Pose()
    ps.draw()














if __name__ == "__main__":
    plt.show()
