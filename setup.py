from setuptools import setup

requirements = [
    'click',
    'certifi',
    'urllib3',
    'chardet',
    'idna',
    'requests',
    'tabulate',
    'timeago'
]

setup(
    name='gitissues',
    version='0.8',
    description='Manage all your git issues at one place',
    author='Roopesh V S',
    author_email='txtmeroopesh@gmail.com',
    url='https://github.com/roopeshvs/git-issues',
    packages=[
        'gitissues',
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
        gitissues=gitissues.cli:cli
    '''
)