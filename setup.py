from setuptools import setup

requirements = [
    'click'
    'requests'
    'tabulate'
    'timeago'
]

setup(
    name='git-issues',
    version='0.1',
    description='manage all your git issues at one place',
    author='@roopeshvs',
    author_email='txtmeroopesh@gmail.com',
    url='https://github.com/roopeshvs/git-issues',
    packages=[
        'git-issues',
    ],
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        git-issues=git-issues.cli:cli
    '''
)