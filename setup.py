from setuptools import find_packages
from setuptools import setup

setup(
    name='pre-commit-hooks',
    description='HMRC\'s pre-commit-hook collection',
    url='https://github.com/hmrc/security-git-hooks',
    version='test2',

    author='Platform Security',

    platforms='linux',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'secrets_filename = pre_commit_hooks.secrets_filename:main',
            'secrets_filecontent = pre_commit_hooks.secrets_filecontent:main',
        ],
    },
)