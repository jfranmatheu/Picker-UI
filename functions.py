from mathutils import Vector
import bpy
from bpy_extras import view3d_utils
import bgl
from mathutils.geometry import area_tri
from math import sqrt, hypot, cos, sin, radians


def get_corner_points_from_bb_relative_to_view(target_obj=None, view='FRONT'):
    if not target_obj:
        return None

    if view == 'FRONT':
        index_points = [3, 6]
    elif view == 'BACK':
        index_points = [1, 4]
    elif view == 'LEFT':
        index_points = [5, 7]
    elif view == 'RIGHT':
        index_points = [2, 0]
    else:
        return None

    bb = target_obj.bound_box
    return [Vector((bb[index_points[0]])), Vector((bb[index_points[1]]))]

def get_regiondata_view3d(context):
    print("GetRegionData::CONTEXT: ", context)
    print("CONTEXT_REGION: ", context.region)
    print("CONTEXT_SPACE_DATA: ", context.space_data)
    if not context or not context.region or not context.space_data:
        print("CONTEXT: ", context)
        context = bpy.context
        print("CONTEXT: ", context)
    return context.region, context.space_data.region_3d

def convert_3d_spacecoords_to_2d_screencoords(context, point):
    print("Convert3dTo2d::CONTEXT: ", context)
    region, region_data = get_regiondata_view3d(context)
    return view3d_utils.location_3d_to_region_2d(region, region_data, point, default=None)

def viewport_screenshot(_x, _y, _width, _height, _name="Screenshot"): #, _useAlpha=True):
    bgl.glDisable(bgl.GL_DEPTH_TEST)
    buffer = bgl.Buffer(bgl.GL_FLOAT, _width * _height * 4)
    bgl.glReadPixels(_x, _y, _width, _height, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)
    img = bpy.data.images.new(_name, _width, _height, alpha=True)
    #img.pixels[:] = buffer
    img.pixels.foreach_set(buffer)
    bgl.glClear(bgl.GL_COLOR_BUFFER_BIT)
    return img

def point_inside_rect(_p, _pos, _size):
    return ((_pos[0] + _size[0]) > _p[0] > _pos[0]) and ((_pos[1] + _size[1]) > _p[1] > _pos[1])

def _point_inside_tri(p, A, B, C): # return bool
   # Calculate area of triangle ABC
   A = area_tri(A, B, C)
   # Calculate area of triangle PBC
   A1 = area_tri(p, B, C)
   # Calculate area of triangle PAC
   A2 = area_tri(A, p, C)
   # Calculate area of triangle PAB
   A3 = area_tri(A, B, p)
   # Check if sum of A1, A2 and A3 is same as A
   return (A == A1 + A2 + A3)

def get_area_tri(_x1, _y1, _x2, _y2, _x3, _y3): # 2D
    return abs((_x1*(_y2-_y3) + _x2*(_y3-_y1)+ _x3*(_y1-_y2))/2)

def point_inside_tri(_x, _y, _x1, _y1, _x2, _y2, _x3, _y3): # return bool
   # Calculate area of triangle ABC
   A = get_area_tri (_x1, _y1, _x2, _y2, _x3, _y3)
   # Calculate area of triangle PBC
   A1 = get_area_tri (_x, _y, _x2, _y2, _x3, _y3)
   # Calculate area of triangle PAC
   A2 = get_area_tri (_x1, _y1, _x, _y, _x3, _y3)
   # Calculate area of triangle PAB
   A3 = get_area_tri (_x1, _y1, _x2, _y2, _x, _y)
   # Check if sum of A1, A2 and A3 is same as A
   return (A == A1 + A2 + A3)

def deselect_all_pose_bones(context):
    for b in context.selected_pose_bones_from_active_object:
        b.bone.select = False

# 2D METHOD
def distance_between(_p1, _p2): # Punto - Punto
    return hypot(_p1[0] - _p2[0], _p1[1] - _p2[1]) # Método 1
    #return math.sqrt((_p1[1] - _p1[0])**2 + (_p2[1] - _p2[0])**2) # Método 2

# 3D METHOD
def distance_point_point_3d(_p1, _p2): # Punto - Punto
    return sqrt((_p1[0] - _p2[0])**2 + (_p1[1] - _p2[1])**2 + (_p1[2] - _p2[2])**2)

def distance_points_plane_3d(_point, _plane_point, _plane_normal):
    # Returns the signed distance between a point and a plane (negative when below the normal)
    return distance_point_to_plane(_point, _plane_point, _plane_normal) # float

def get_nearest_point(_base, _points): # POINTS SHOULD BE VECTORS (2D)
    n = 0
    nearestPoint = None
    for point in _points:
        dist = DistanceBetween(_base, point)
        if  dist < minDist:
            minDist = dist
            nearestPoint = point
        n+=1
    return nearestPoint, minDist # point.co & float

def point_inside_circle(_mousePos, _coords, _radius):
    return distance_between(_mousePos, _coords) < _radius

def rotate_point_around_point(ox, oy, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    # ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return (qx, qy)
