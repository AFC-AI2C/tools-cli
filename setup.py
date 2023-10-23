from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dstools',
    version='0.1.0',
    author="Isaac J. Faber",
    author_email="isaacfab@gmail.com",
    description="A simple CLI to start data science dev environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docker',
        'click',
        'requests',
        'simple-term-menu',
    ],
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        dstools=dstools:main
    ''',
)

