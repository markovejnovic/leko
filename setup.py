import os
from setuptools import find_packages, setup


def __read(path: str) -> str:
    with open(os.path.abspath(path), 'r') as f:
        return f.read()


setup(
    name="leko",
    version='0.1.0',
    description="Leko is the programmer's notebook.",
    url="https://github.com/markovejnovic/leko/",
    long_description=__read("README.md"),
    long_description_content_type="text/markdown",
    author="author_name",
    packages=find_packages(exclude=["tests", ".github"]),
    package_data={'leko': ['style/**/*']},
    install_requires=[
        'pandoc>=2.3',
        'plumbum>=1.8',
        'ply>=3.11'
    ],
    entry_points={
        "console_scripts": ["leko = leko.__main__:main"]
    },
)
