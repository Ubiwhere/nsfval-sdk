from setuptools import setup, find_packages

setup(
    name='nsfval-sdk',
    license='Apache License, Version 2.0',
    version='0.1',
    author='Luís Conceição',
    author_email='lconceicao@ubiwhere.com',
    packages=find_packages(),
    install_requires=['requests', 'pyaml', 'configloader', 'coloredlogs'],
    test_suite='sdk',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
