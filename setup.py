from setuptools import setup, find_packages

test_requirements = ['pytest']
setup(
    name='nsfval-sdk',
    license='Apache License, Version 2.0',
    version='0.1',
    author='Luís Conceição',
    author_email='lconceicao@ubiwhere.com',
    packages=find_packages(),
    install_requires=['requests', 'pyaml', 'coloredlogs'] + test_requirements,
    test_suite='nsfval-sdk',
)
