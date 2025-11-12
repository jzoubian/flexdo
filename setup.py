from setuptools import setup, find_packages

setup(
    name='flexdo',
    version='0.1.0',
    description='Command-line tool for flexible daily task management',
    author='flexdo',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'flexdo=flexdo.cli:cli',
        ],
    },
    python_requires='>=3.7',
)
