import pathlib

from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent

setup(
    name='smacc_email',
    packages=find_packages(where=str(here), exclude=('tests',)),
)
