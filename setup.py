# First Party
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webmocket",
    version="0.1.0",
    packages=["webmocket"],
    install_requires=["asgiref==3.3.4", "asyncio==3.4.3", "websockets==8.1"],
    url="https://github.com/ahmetkotan/webmocket",
    license="",
    author="ahmetkotan",
    author_email="ahmtkotan@gmail.com",
    description="Fake websocket server for websocket integration tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
