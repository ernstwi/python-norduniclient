from setuptools import setup, find_packages

version = '0.0.1'

requires = [
    'neo4jdb==0.0.8',
]

testing_requires = [
    'nose',
    'coverage',
    'nosexcover',
]

setup(
    name='norduniclient',
    version=version,
    url='https://github.com/NORDUnet/python-norduniclient',
    license='',
    author='Johan Lundberg',
    author_email='lundberg@nordu.net',
    description='Neo4j database client for NORDUnet network inventory',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requires,
    tests_require=testing_requires,
    test_suite="norduniclient",
    extras_require={
        'testing': testing_requires
    }
)
