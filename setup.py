from setuptools import setup

setup(
    name='pyidtech3lib',
    version='0.0.2',
    author='SomaZ',
    url='https://github.com/SomaZ/pyidtech3lib',
    license='MIT',
    description="A little id tech 3 library to load different kind of bsp files and triangulate bsp surfaces",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['pyidtech3lib'],
    install_requires=[
        'numpy',
    ],
    keywords=['quake3', 'bsp', 'idtech3'],
    classifiers=[
        'License :: MIT License',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)