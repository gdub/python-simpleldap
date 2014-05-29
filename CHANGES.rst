=========
Changelog
=========


0.8 - May 28, 2014
==================
* Dropped support for Python 2.5.
* Removed distribute_setup bootstrap file, installation now requires
  setuptools to already be installed.
* #1: Added an ``authenticate`` method for authenticating a given DN and
  password using a bind operation.
* #2: Added the ability to set (and clear) defaults for the ``search`` method.
* #4: Added a ``compare`` method, wrapping ldap's compare, to return boolean
  values instead of 0 and 1.


0.7.1 - July 19, 2012
=====================
* Added tox testing configuration, setup to run against Python 2.5, 2.6,
  and 2.7.
* Converted repo from hg to git.


0.7 - July 10, 2011
===================
* Initial release.
* ``Connection`` class for conveniently creating connections to LDAP servers.
* ``LDAPItem`` class for wrapping LDAP result objects and allowing more
  convenient, dictionary-like access to their contained data.
