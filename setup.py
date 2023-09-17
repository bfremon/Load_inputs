import os
from setuptools import setup

setup(
    name = "lib_test",
#    version = "1.0",
    author = "Benoit FREMON",
    author_email = "ben@in.volution.fr",
    description = "Demo of packaging a Python script as DEB",
    long_description = "Demo of packaging a Python script as DEB",
    license = "GPL",
    url = "https://git.volution.fr:4444/pkg_template",
    packages=['lib_test'],
    entry_points = {
        'console_scripts' : ['lib_test = lib_test']
    },
    # data_files = [
    #     ('share/applications/', ['vxlabs-myscript.desktop'])
    # ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"

    ],
)
