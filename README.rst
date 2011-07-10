==============
``simpleldap``
==============


About
=====

A small wrapper around the python-ldap library that provides a more Pythonic
interface for LDAP server connections, LDAP objects, and the common get and
search operations.


Example
=======

A quick and easy example using ``simpleldap``::

    >>> import simpleldap
    >>> conn = simpleldap.Connection('directory.example.com')
    >>> user = conn.get("uid=myuser")
    >>> user.dn
    'uid=myuser,dc=directory,dc=example,dc=com'
    >>> user['cn']
    ['Joe Smith', 'Joe M. Smith']
    >>> user.first('cn')
    'Joe Smith'
    >>> conn.close()

The ``Connection`` object can also be used as a context manager, e.g.::

    with simpleldap.Connection('directory.example.com') as conn:
        users = conn.search("(&(givenName=Joe)(sn=Smith))")


Installation
============

Install using pip::

    pip install simpleldap
