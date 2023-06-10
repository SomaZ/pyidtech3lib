from pyidtech3lib.Parsing import *
from pyidtech3lib import ID3Image as Image


def create_white_image():
    image = Image.ID3Image()
    image.name = "$whiteimage"
    image.width = 8
    image.height = 8
    image.num_components = 4
    image.data = [255] * 256
    return image


def get_material_dicts(VFS, import_settings, material_list):

    for shader_path in import_settings.shader_dirs:
        reg = "^" + shader_path + r"(.*?).shader$"
        shader_list = VFS.search(reg)
        if len(shader_list) > 0:
            break

    shader_info = {}

    for shader_file in shader_list:
        shader_bytearray = VFS.get(shader_file)
        lines = shader_bytearray.decode(encoding="latin-1").splitlines()

        current_shader = None
        stage = {}
        attributes = {}
        stages = []
        is_open = 0
        for line in lines:
            # trim line
            line = l_format(line)
            # skip empty lines or comments
            if (l_empty(line) or l_comment(line)):
                continue
            # content
            if (not l_open(line) and not l_close(line)):
                # shader names
                if is_open == 0:
                    if line in material_list:
                        current_shader = line
                # shader attributes
                elif is_open == 1 and current_shader:
                    key, value = parse(line)
                    if key in attributes:
                        attributes[key].append(value)
                    else:
                        attributes[key] = [value]
                # stage info
                elif is_open == 2 and current_shader:
                    key, value = parse(line)
                    # FIXME: multiple tcMods are supported by the game engine
                    stage[key] = value
            # marker open
            elif l_open(line):
                is_open = is_open + 1
            # marker close
            elif l_close(line):
                # close stage
                if is_open == 2 and current_shader:
                    stages.append(stage)
                    stage = {}
                # close material
                elif is_open == 1 and current_shader:
                    if current_shader not in shader_info:
                        shader_info[current_shader] = attributes, stages
                    attributes = {}
                    stages = []
                    current_shader = None
                is_open -= 1
    return shader_info


def get_shader_image_sizes(VFS, import_settings, material_list):

    shader_info = get_material_dicts(VFS, import_settings, material_list)
    image_formats = ("", ".tga", ".png", ".jpg")
    material_sizes = {}
    for shader in shader_info:
        attributes, stages = shader_info[shader]
        if "qer_editorimage" in attributes:
            for fmt in image_formats:
                editor_image = VFS.get(attributes["qer_editorimage"][0]+fmt)
                if editor_image is not None:
                    break
            if editor_image is not None:
                material_sizes[shader.lower()] = (
                    Image.get_image_dimensions_from_bytearray(editor_image))
                continue

        for fmt in image_formats:
            image = VFS.get(shader+fmt)
            if image is not None:
                break
        if image is not None:
            material_sizes[shader.lower()] = (
                Image.get_image_dimensions_from_bytearray(image))
            continue

        for stage in stages:
            if "map" in stage:
                for fmt in image_formats:
                    image = VFS.get(stage["map"]+fmt)
                    if image is not None:
                        break
                if image is not None:
                    material_sizes[shader.lower()] = (
                        Image.get_image_dimensions_from_bytearray(image))
                    break

    return material_sizes
