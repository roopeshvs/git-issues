from setuptools import setup

setup(
    name="git-issues",
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        git-issues=cli:cli
    ''',
)