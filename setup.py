from setuptools import setup

with open('README.md', 'r') as description_file:
    long_description = description_file.read()

setup(
    name='cuco',
    version='0.9.0',
    description='Project for making it easier to write configuration files which may be automatically converted into a set of alternative system setups',
    url='https://github.com/zeionara/cuco',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=[
        'cuco',
        'cuco.utils'
    ],
    install_requires=[
        'pyyaml',
        'ruamel.yaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)
