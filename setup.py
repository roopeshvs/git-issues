from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    'click'
    'requests'
    'tabulate'
    'timeago'
]

setup(
    name='git-issues',
    version='0.1',
    description='Manage all your git issues at one place',
    long_description= long_description,
    author='Roopesh V S',
    author_email='txtmeroopesh@gmail.com',
    url='https://github.com/roopeshvs/git-issues',
    packages=[
        'git-issues',
    ],
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points='''
        [console_scripts]
        git-issues=git-issues.cli:cli
    '''
)