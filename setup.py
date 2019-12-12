"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

setup(
    name='panda3d-cefconsole',
    version='0.1.0alpha',
    description='A CEF-based extendable console for Panda3D applictions',
    url='https://github.com/TheCheapestPixels/panda-cefconsole',
    author='TheCheapestPixels',
    author_email='TheCheapestPixels@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='panda3d console',
    packages=find_packages(exclude=['tests', 'examples']),
    package_dir={
        'cefconsole': 'cefconsole',
    },
    package_data={
        'cefconsole': ['templates/*.html'],
    },
    python_requires='>=3.7, <4',
    install_requires=['panda3d', 'cefpanda', 'jinja2'],
    entry_points={
        'console_scripts': [
            'cefconsole_demo = cefconsole.boilerplate:main',
        ],
    },
)
