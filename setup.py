from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

setup(
        name="fabrace-api",
        version="0.0.1",
        packages=find_packages(include=['febraceapi']),
        install_requires=requirements
)
