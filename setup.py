from setuptools import setup, find_packages

setup(
    name='dstools',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docker',
        'click',
        'requests',
        'simple-term-menu',
    ],
    entry_points='''
        [console_scripts]
        dstools=dstools:main
    ''',
)

