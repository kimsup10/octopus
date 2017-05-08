from setuptools import setup, find_packages


def get_requirements(filename='requirements.txt'):
    deps = []
    with open(filename, 'r') as f:
        for pkg in f.readlines():
            if pkg.strip():
                deps.append(pkg)
    return deps


install_requires = get_requirements()
setup(
    name='Octopus',
    version='0.1.0-dev',
    description='Paul, the octopus',
    author=['Hunchul Park', 'Seungsup Kim', 'Jinseong Yu'],
    author_email='huntrax11@ajou.ac.kr',
    url='http://github.com/huntrax11/octopus',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
)
