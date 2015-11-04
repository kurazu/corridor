import collections
import bpy


Point = collections.namedtuple('Point', ('x', 'y', 'z'))


class Shape(list):

    def __init__(self, x, y, z):
        super().__init__()
        self.names = {}
        self.add(x, y, z, 'start')

    def add(self, x, y, z, name):
        assert name not in self.names
        point = Point(x, y, z)
        self.append(point)
        self.names[name] = point
        return point

    def dx(self, dx, name):
        tail = self[-1]
        return self.add(tail.x + dx, tail.y, tail.z, name)

    def dy(self, dy, name):
        tail = self[-1]
        return self.add(tail.x, tail.y + dy, tail.z, name)

    def dz(self, dz, name):
        tail = self[-1]
        return self.add(tail.x, tail.y, tail.z + dz, name)

    def point_by_name(self, name):
        point = self.names[name]
        return self.index(point)

    def faces(self):
        return [list(range(len(self)))]


objects = []

def mesh(func):
    name = func.__name__
    verts = func()
    faces = verts.faces()
    mesh = bpy.data.meshes.new(name + ' mesh')
    obj = bpy.data.objects.new(name, mesh)
    mesh.from_pydata(verts, [], faces)
    objects.append(obj)
    return obj


def floor_shape(verts):
    verts.dy(3.7, 'north')
    verts.dx(1.95, 'east')
    verts.dy(-0.08 - 1 - 1.66, 'south')
    verts.dx(1.48, 'bathroom')
    verts.dy(-0.96, 'back')
    verts.dx(-3.43, 'west')

def rect(v, dx=None, dy=None, dz=None):
    assert(len(list(filter(None, [dx, dy, dz]))) == 2)
    if dx is None:
        v.dy(dy, 'bottom')
        v.dz(dz, 'east')
        v.dy(-dy, 'top')
        v.dz(-dz, 'west')
    elif dy is None:
        assert(False)
    else:
        assert(False)

@mesh
def floor():
    v = Shape(0, 0, 0)
    floor_shape(v)
    return v


@mesh
def ceiling():
    verts = Shape(0, 0, 2.51)
    floor_shape(verts)
    return verts
    
@mesh
def back_wall():
    verts = Shape(3.43, 0, 0)
    rect(verts, dy=0.96, dz=2.51)
    return verts

@mesh
def outer_wall_left():
    v = Shape(0, 0, 0)
    rect(v, dy=1.43, dz=2.51)
    return v

@mesh
def outer_wall_top():
    v = Shape(0, 1.43, 2.51)
    rect(v, dy=1.0, dz=-0.46)
    return v

@mesh
def outer_wall_right():
    v = Shape(0, 2.43, 0)
    rect(v, dy=1.27, dz=2.51)
    return v

@mesh
def south_wall_left():
    v = Shape(1.95, 0.96, 0)
    rect(v, dy=1.66, dz=2.51)
    return v

@mesh
def south_wall_top():
    v = Shape(1.95, 3.7 - 0.08 - 1.0, 2.05)
    rect(v, dy=1.0, dz=0.46)
    return v

@mesh
def south_wall_right():
    v = Shape(1.95, 3.7 - 0.08, 0)
    rect(v, dy=0.08, dz=2.51)
    return v
    

def main():
    scene = bpy.context.scene
    for obj in objects:
        scene.objects.link(obj)


if __name__ == '__main__':
    main()
