from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name             = 'resub',
    version          = '1.0.0',
    description      = 'Use regular expressions to perform find-and-replace.',
    long_description = readme,
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-re-sub#readme',
    packages         = ['resub'],
    install_requires = ['chrisapp', 'tqdm'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'resub = resub.__main__:main'
            ]
        }
)
