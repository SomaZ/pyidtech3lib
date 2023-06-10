# pyidtech3lib
Little id tech 3 library to load different kind of bsp files

## Basic Example

This example will print the names of all the used shaders in a bsp file. 

First we create a import_settings instance that holds all the needed information about the file we want to import. 
After that we create the VFS and read the bsp file.
```
import pyidtech3lib

import_settings = pyidtech3lib.Import_Settings(
    file="maps/q3dm1.bsp",
    subdivisions=0,
    base_paths=[
        "D:/Games/Quake3/baseq3/",
    ],
    preset=pyidtech3lib.Preset.EDITING.value,
    front_culling=False,
)

VFS = pyidtech3lib.Q3VFS()
for base_path in import_settings.base_paths:
    VFS.add_base(base_path)
VFS.build_index()

bsp = pyidtech3lib.BSP_READER(VFS, import_settings)

for shader in bsp.lumps["shaders"]:
    print(shader.name)
```

## Install

From source:
```
git clone https://github.com/SomaZ/pyidtech3lib
cd pyidtech3lib
pip install .
```

## Attributions

- Virtual file system support by Alexander @cagelight Sago 
