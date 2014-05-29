from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: System :: Systems Administration :: Authentication/Directory',
    'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
]

setup(
    name="simpleldap",
    version="0.8",
    description="A module that makes simple LDAP usage simple.",
    long_description=open('README.rst').read(),
    keywords="ldap simple simpleldap",
    author="Gary Wilson Jr.",
    author_email="gary@thegarywilson.com",
    url="https://github.com/gdub/python-simpleldap",
    license="MIT",
    packages=["simpleldap"],
    install_requires=["python-ldap"],
    tests_require=["tox", "pytest", "pep8", "python-ldap"],
)
