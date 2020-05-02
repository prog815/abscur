from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='abscur',
    version='0.1.4',
    description='Библиотека доступа к данным проекта <Абсолютный курс>',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author_email='eavprog@gmail.com',
    zip_safe=False
)
