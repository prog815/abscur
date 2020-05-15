from setuptools import setup, find_packages
from os.path import join, dirname

import abscur

setup(
    name='abscur',
    version='0.1.21',
    description='Библиотека доступа к данным проекта <Абсолютный курс>',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    author_email='eavprog@gmail.com'
)
