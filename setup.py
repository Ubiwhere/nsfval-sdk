from setuptools import setup, find_packages

setup(
    name='nsfval-sdk',
    license='Apache License, Version 2.0',
    version='0.1',
    author='Luís Conceição',
    author_email='lconceicao@ubiwhere.com',
    packages=find_packages(),
    install_requires=['requests_toolbelt', 'requests', 'pyaml'],

    ## TODO: remove - for dev tests only
    entry_points={
        'console_scripts': [
            'sdk=nsfval.sdk.sdk:main',
        ],
    },
)
