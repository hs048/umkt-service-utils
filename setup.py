import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='umkt-service-utils',
    version='0.1',
    packages=['umkt_service_utils'],
    description='A line of description',
    long_description=README,
    author='hendra saputra',
    author_email='hs048@umkt.ac.id',
    url='https://github.com/hs048/umkt-service-utils',
    license='MIT',
    install_requires=[
        'Django>=1.6,<1.7',
    ]
)