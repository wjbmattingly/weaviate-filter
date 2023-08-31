from setuptools import setup, find_packages

setup(
    name='weaviate_filter',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'weaviate-client',
    ],
    url='https://github.com/wjbmattingly/weaviate-filter',
    license='MIT',
    author='WJB Mattingly',
    description='A package for creating GraphQL filters for Weaviate',
    python_requires='>=3.6',
)
