from setuptools import setup
from os.path import join, dirname

from gdp import __version__  # type: ignore

setup(
    name='gdp',
    version=__version__,
    packages=['gdp', 'gdp.parser'],
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
)
