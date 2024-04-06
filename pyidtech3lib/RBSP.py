from ctypes import (LittleEndianStructure,
                    c_char, c_float, c_int, c_uint, c_short, c_ubyte, sizeof)
from numpy import array
from pyidtech3lib.Helpers import normalize, avg_ivec3, avg_vec2, avg_vec3


class BSP_HEADER(LittleEndianStructure):
    _fields_ = [
        ("magic_nr", c_char*4),
        ("version_nr", c_int),
    ]


class BSP_ENTITY(LittleEndianStructure):
    _fields_ = [
            ("char", c_char)
    ]


class BSP_SHADER(LittleEndianStructure):
    _fields_ = [
        ("name", c_char * 64),
        ("flags", c_uint),
        ("contents", c_uint),
    ]


class BSP_PLANE(LittleEndianStructure):
    _fields_ = [
        ("normal", c_float * 3),
        ("distance", c_float),
    ]


class BSP_NODE(LittleEndianStructure):
    _fields_ = [
        ("plane", c_int),
        ("children", c_int * 2),
        ("mins", c_int * 3),
        ("maxs", c_int * 3),
    ]


class BSP_LEAF(LittleEndianStructure):
    _fields_ = [
        ("cluster", c_int),
        ("area", c_int),
        ("mins", c_int * 3),
        ("maxs", c_int * 3),
        ("leafface", c_int),
        ("n_leaffaces", c_int),
        ("leafbrush", c_int),
        ("n_leafbrushes", c_int),
    ]


class BSP_LEAF_FACE(LittleEndianStructure):
    _fields_ = [
        ("face", c_int),
    ]


class BSP_LEAF_BRUSH(LittleEndianStructure):
    _fields_ = [
        ("brush", c_int),
    ]


class BSP_MODEL(LittleEndianStructure):
    _fields_ = [
        ("mins", c_float * 3),
        ("maxs", c_float * 3),
        ("face", c_int),
        ("n_faces", c_int),
        ("brush", c_int),
        ("n_brushes", c_int),
    ]


class BSP_BRUSH(LittleEndianStructure):
    _fields_ = [
        ("brushside", c_int),
        ("n_brushsides", c_int),
        ("texture", c_int),
    ]


class BSP_BRUSH_SIDE(LittleEndianStructure):
    _fields_ = [
        ("plane", c_int),
        ("texture", c_int),
        ("face", c_int),
    ]


class BSP_VERTEX(LittleEndianStructure):
    _fields_ = [
        ("position", c_float * 3),
        ("texcoord", c_float * 2),
        ("lm1coord", c_float * 2),
        ("lm2coord", c_float * 2),
        ("lm3coord", c_float * 2),
        ("lm4coord", c_float * 2),
        ("normal", c_float * 3),
        ("color1", c_ubyte * 4),
        ("color2", c_ubyte * 4),
        ("color3", c_ubyte * 4),
        ("color4", c_ubyte * 4),
    ]


class BSP_INDEX(LittleEndianStructure):
    _fields_ = [
        ("offset", c_int),
    ]


class BSP_FOG(LittleEndianStructure):
    _fields_ = [
        ("name", c_char * 64),
        ("brush", c_int),
        ("visibleSide", c_int),
    ]


class BSP_SURFACE(LittleEndianStructure):
    _fields_ = [
        ("texture", c_int),
        ("effect", c_int),
        ("type", c_int),
        ("vertex", c_int),
        ("n_vertexes", c_int),
        ("index", c_int),
        ("n_indexes", c_int),
        ("lm_styles", c_ubyte * 4),
        ("vertex_styles", c_ubyte * 4),
        ("lm_indexes", c_int * 4),
        ("lm_x", c_int * 4),
        ("lm_y", c_int * 4),
        ("lm_width", c_int),
        ("lm_height", c_int),
        ("lm_origin", c_float * 3),
        ("lm_vecs", c_float * 9),
        ("patch_width", c_int),
        ("patch_height", c_int),
    ]


class BSP_LIGHTMAP(LittleEndianStructure):
    _fields_ = [
        ("map", c_ubyte * (128 * 128 * 3)),
    ]


class BSP_LIGHTGRID(LittleEndianStructure):
    _fields_ = [
        ("ambient1", c_ubyte * 3),
        ("ambient2", c_ubyte * 3),
        ("ambient3", c_ubyte * 3),
        ("ambient4", c_ubyte * 3),
        ("direct1", c_ubyte * 3),
        ("direct2", c_ubyte * 3),
        ("direct3", c_ubyte * 3),
        ("direct4", c_ubyte * 3),
        ("styles", c_ubyte * 4),
        ("lat_long", c_ubyte * 2)
    ]


class BSP_VIS(LittleEndianStructure):
    _fields_ = [
        ("bit_set", c_ubyte),
    ]


class BSP_LIGHTGRID_ARRAY(LittleEndianStructure):
    _fields_ = [
        ("index", c_short),
    ]


class BSP_INFO:
    bsp_magic = b'RBSP'
    bsp_version = 1

    lightgrid_size = [64, 64, 128]
    lightgrid_inverse_size = [1.0 / float(lightgrid_size[0]),
                              1.0 / float(lightgrid_size[1]),
                              1.0 / float(lightgrid_size[2])]

    lightmap_size = [128, 128]
    lightmaps = 4
    lightstyles = 4
    use_lightgridarray = True

    lumps = {"entities":         BSP_ENTITY,
             "shaders":          BSP_SHADER,
             "planes":           BSP_PLANE,
             "nodes":            BSP_NODE,
             "leafs":            BSP_LEAF,
             "leaffaces":        BSP_LEAF_FACE,
             "leafbrushes":      BSP_LEAF_BRUSH,
             "models":           BSP_MODEL,
             "brushes":          BSP_BRUSH,
             "brushsides":       BSP_BRUSH_SIDE,
             "drawverts":        BSP_VERTEX,
             "drawindexes":      BSP_INDEX,
             "fogs":             BSP_FOG,
             "surfaces":         BSP_SURFACE,
             "lightmaps":        BSP_LIGHTMAP,
             "lightgrid":        BSP_LIGHTGRID,
             "visdata":          BSP_VIS,
             "lightgridarray":   BSP_LIGHTGRID_ARRAY
             }

    header = BSP_HEADER
    header_size = sizeof(BSP_HEADER)

    lightmap_lumps = ("lightmaps",)

    @classmethod
    def lerp_vertices(
            cls,
            vertex1: BSP_VERTEX,
            vertex2: BSP_VERTEX
            ) -> BSP_VERTEX:

        lerped_vert = BSP_VERTEX()

        vec = normalize(array(vertex1.normal) + array(vertex2.normal))
        lerped_vert.normal[0] = vec[0]
        lerped_vert.normal[1] = vec[1]
        lerped_vert.normal[2] = vec[2]
        lerped_vert.position = avg_vec3(vertex1.position, vertex2.position)
        lerped_vert.texcoord = avg_vec2(vertex1.texcoord, vertex2.texcoord)
        lerped_vert.lm1coord = avg_vec2(vertex1.lm1coord, vertex2.lm1coord)
        lerped_vert.lm2coord = avg_vec2(vertex1.lm2coord, vertex2.lm2coord)
        lerped_vert.lm3coord = avg_vec2(vertex1.lm3coord, vertex2.lm3coord)
        lerped_vert.lm4coord = avg_vec2(vertex1.lm4coord, vertex2.lm4coord)
        lerped_vert.color1 = avg_ivec3(vertex1.color1, vertex2.color1)
        lerped_vert.color2 = avg_ivec3(vertex1.color2, vertex2.color2)
        lerped_vert.color3 = avg_ivec3(vertex1.color3, vertex2.color3)
        lerped_vert.color4 = avg_ivec3(vertex1.color4, vertex2.color4)
        return lerped_vert
