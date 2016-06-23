from distutils.core import setup

version = '0.1'

requires = [
    'neo4jdb-python==0.0.8',
]

test_requires = [
    'nose',
    'coverage',
    'nosexcover',
]

setup(
    name='python-norduniclient',
    version=version,
    packages=['norduniclient'],
    url='https://github.com/NORDUnet/python-norduniclient',
    license='',
    author='Johan Lundberg',
    author_email='lundberg@nordu.net',
    description='Neo4j database client for NORDUnet network inventory',
    install_requires=requires,
    tests_require=test_requires,
)
