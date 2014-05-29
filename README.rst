==============
``simpleldap``
==============


About
=====

A small wrapper around the python-ldap library that provides a more Pythonic
interface for LDAP server connections, LDAP objects, and the common get and
search operations.


Installation
============

Install using pip::

    pip install simpleldap


Examples
========

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

A common method for authenticating users is to connect to an LDAP server using
a service user/account and then attempt a bind operation using the user's
credentials (i.e. DN and password).  The ``authenticate`` method makes this
simple::

    with simpleldap.Connection('directory.example.com') as conn:
        is_valid = conn.authenticate('uid=myuser,dc=directory,dc=example,dc=com', 'password')

.. note::
    The ``authentication`` method does not perform an unbind and does not bind again
    using the original connection's credentials; therefore, any further
    actions following a successful ``authenticate`` call will be performed as
    the authenticated user.

LDAP also offers a feature to compare an attribute's value with a given string.
This can occasionally be more efficient and expressive than grabbing an entire
object from the LDAP store. ``simpleldap`` offers a ``compare`` method for this
feature::

    >>> conn = simpleldap.Connection('directory.example.com')
    >>> user_dn = 'uid=myuser,dc=directory,dc=example,dc=com'
    >>> conn.compare(user_dn, 'cn', 'Joe Smith')
    True

