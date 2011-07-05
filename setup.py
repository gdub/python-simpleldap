from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
    name="python-simpleldap",
    version="0.7",
    description="A module that makes simple LDAP usage simple.",
    keywords="ldap simple simpleldap",
    author="Gary Wilson Jr.",
    author_email="gary.wilson@gmail.com",
    url="https://bitbucket.org/gdub/python-simpleldap/",
    license="MIT",
    py_modules=["simpleldap"],
    install_requires=["python-ldap"],
    use_2to3=True,
)
