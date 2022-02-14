from setuptools import setup, find_packages

setup(
    name='dexter',
    version='1.0.0',
    author='lytos',
    packages=find_packages(),
    entry_points={
            'console_scripts': ['dexter=dexter.main:main']
    }
)
